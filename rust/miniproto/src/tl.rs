//! Native primitive and generated fast-path codecs for Telegram's Type Language (TL).
//!
//! The primitive Python-visible `tl_*` functions mirror the pure-Python fallback API. In contrast,
//! `tl_fast_encode` and `tl_fast_decode` are native-only optional accelerators: Python callers
//! receive `None` when a selected generated fast path is unavailable and use their fallback path.
//! They return `ValueError` or `MemoryError` for malformed wire input or failed allocation, release
//! the GIL only for large primitive-vector work and do not expose unsafe Rust operations.
//! Incompatible Python-to-Rust values instead fail during PyO3 conversion with its original
//! `TypeError`, `OverflowError` or source exception before these algorithms run.
//! `generated_tl.rs` is trusted, build-time-generated metadata consumed—not hand-maintained—by
//! this module. Descriptor indices and bit positions are code-generation invariants rather than
//! values validated on every hot-path call.

use pyo3::IntoPyObjectExt;
use pyo3::exceptions::{PyMemoryError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyModule, PyTuple};
use pyo3::wrap_pyfunction;

use crate::crypto::detach_if_large;
use crate::generated_tl::fast_constructor;

/// Constructor identifier serialized before every generic TL `Vector`.
const TL_VECTOR_CONSTRUCTOR_ID: u32 = 0x1CB5C415;
/// Largest byte-string payload representable by TL's three-byte long length prefix.
const MAX_TL_BYTES_LENGTH: usize = 0xFF_FFFF;

/// Wire representation supported by the generated fast-constructor codec.
#[derive(Clone, Copy)]
pub(crate) enum FastWireType {
    /// Signed 32-bit little-endian integer.
    Int,
    /// Signed 64-bit little-endian integer.
    Long,
    /// Unsigned 64-bit little-endian integer.
    UInt64,
    /// TL length-prefixed bytes.
    Bytes,
    /// UTF-8 TL length-prefixed bytes.
    String,
    /// A generic TL vector of signed 64-bit integers.
    VectorLong,
    /// A generated object field supported only while encoding.
    Object,
    /// A constructor id represented by an otherwise fieldless object.
    EmptyObject,
    /// The complete remaining wire suffix.
    Raw,
    /// MTProto's message-container sequence.
    MessageContainer,
}

/// One generated field action used to encode or decode a fast TL constructor.
#[derive(Clone, Copy)]
pub(crate) enum FastFieldSpec {
    /// Reads or writes one flags word in the specified flags group.
    Flags {
        /// Zero-based generated flags-group index.
        group: usize,
    },
    /// Maps a generated boolean value to one bit in a flags word.
    True {
        /// Index of the Python tuple value that supplies or receives this boolean.
        value: usize,
        /// Zero-based generated flags-group index.
        group: usize,
        /// Bit position within `group`.
        bit: u32,
    },
    /// Maps a Python tuple value to a non-flag wire representation.
    Value {
        /// Index of the Python tuple value to encode or populate.
        value: usize,
        /// Wire representation of that tuple value.
        wire_type: FastWireType,
    },
}

/// Generated metadata for one selected TL constructor fast path.
pub(crate) struct FastConstructorSpec {
    /// Constructor id serialized for boxed values.
    pub(crate) constructor_id: u32,
    /// Generated schema name used in validation errors.
    pub(crate) name: &'static str,
    /// Whether this constructor has a native encoder.
    pub(crate) encode: bool,
    /// Whether this constructor has a native decoder.
    pub(crate) decode: bool,
    /// Exact number of Python tuple values expected by the fast path.
    pub(crate) value_count: usize,
    /// Ordered generated field descriptors.
    pub(crate) fields: &'static [FastFieldSpec],
}

/// Registers the fallback-compatible `tl_*` Python functions on `miniproto._native`.
///
/// Returns a PyO3 error if any function cannot be exported.
///
/// # Arguments
///
/// - `m`: The Python extension module receiving the TL callables.
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(tl_encode_int, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_int, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_uint, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_uint, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_long, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_long, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_int128, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_int128, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_int256, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_int256, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_double, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_double, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_string, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_string, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_int_vector, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_int_vector, m)?)?;
    m.add_function(wrap_pyfunction!(tl_encode_long_vector, m)?)?;
    m.add_function(wrap_pyfunction!(tl_decode_long_vector, m)?)?;
    m.add_function(wrap_pyfunction!(tl_fast_encode, m)?)?;
    m.add_function(wrap_pyfunction!(tl_fast_decode, m)?)?;
    Ok(())
}

/// Attempts Python `tl_fast_encode` for a generated constructor.
///
/// `values` must have the generated constructor's exact tuple arity; `boxed` controls whether the
/// constructor id is emitted. Returns `None` if no native encoder exists, encoded bytes on
/// success or a Python exception for incompatible values or generated metadata. PyO3 conversion
/// failures from tuple lookup/extraction propagate as `TypeError`, `OverflowError` or the source
/// Python exception; algorithm and descriptor validation failures intentionally use `ValueError`.
///
/// # Arguments
///
/// - `constructor_id`: Generated TL constructor id selecting a trusted fast-path descriptor.
/// - `values`: Python tuple whose exact arity and value types must match that descriptor.
/// - `boxed`: Whether to serialize the constructor id before its fields.
#[pyfunction]
#[pyo3(signature = (constructor_id, values, boxed=true))]
fn tl_fast_encode(
    constructor_id: u32,
    values: &Bound<'_, PyTuple>,
    boxed: bool,
) -> PyResult<Option<Vec<u8>>> {
    let Some(spec) = fast_constructor(constructor_id).filter(|spec| spec.encode) else {
        return Ok(None);
    };
    if values.len() != spec.value_count {
        return Err(PyValueError::new_err(format!(
            "{} fast encoder expected {} values, got {}",
            spec.name,
            spec.value_count,
            values.len()
        )));
    }
    let mut flags = [0_u32; 4];
    for field in spec.fields {
        if let FastFieldSpec::True { value, group, bit } = *field {
            if group >= flags.len() || bit >= 32 {
                return Err(PyValueError::new_err(
                    "generated TL flag descriptor is invalid",
                ));
            }
            if values.get_item(value)?.extract::<bool>()? {
                flags[group] |= 1_u32 << bit;
            }
        }
    }
    let mut output = Vec::with_capacity(64);
    if boxed {
        output.extend_from_slice(&spec.constructor_id.to_le_bytes());
    }
    for field in spec.fields {
        match *field {
            FastFieldSpec::Flags { group } => {
                let value = *flags
                    .get(group)
                    .ok_or_else(|| PyValueError::new_err("generated TL flag group is invalid"))?;
                output.extend_from_slice(&value.to_le_bytes());
            }
            FastFieldSpec::True { .. } => {}
            FastFieldSpec::Value { value, wire_type } => {
                encode_fast_value(&mut output, &values.get_item(value)?, wire_type)?;
            }
        }
    }
    Ok(Some(output))
}

/// Attempts Python `tl_fast_decode` for a generated constructor at `offset`.
///
/// `boxed` requires and verifies the constructor id. Returns `None` if no native decoder exists,
/// otherwise `(values_tuple, next_offset)`; malformed wire input raises a Python exception. This
/// conversion necessarily holds the GIL to create Python objects. PyO3 conversion errors are
/// propagated unchanged, whereas malformed TL bytes use `ValueError`. Descriptor indices and flag
/// bits come from trusted generated metadata and are not revalidated on every hot-path call.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to construct decoded Python values.
/// - `constructor_id`: Generated TL constructor id selecting a trusted fast-path descriptor.
/// - `data`: TL wire bytes to decode.
/// - `offset`: Byte offset at which this constructor begins.
/// - `boxed`: Whether `data` starts with and must match the constructor id.
#[pyfunction]
#[pyo3(signature = (constructor_id, data, offset=0, boxed=true))]
fn tl_fast_decode(
    py: Python<'_>,
    constructor_id: u32,
    data: &[u8],
    offset: usize,
    boxed: bool,
) -> PyResult<Option<(Py<PyTuple>, usize)>> {
    let Some(spec) = fast_constructor(constructor_id).filter(|spec| spec.decode) else {
        return Ok(None);
    };
    let mut cursor = offset;
    if boxed {
        let actual = u32::from_le_bytes(read_fixed::<4>(data, cursor)?);
        cursor = cursor
            .checked_add(4)
            .ok_or_else(|| PyValueError::new_err("TL offset overflow"))?;
        if actual != spec.constructor_id {
            return Err(PyValueError::new_err(format!(
                "expected constructor 0x{:08x}, got 0x{actual:08x}",
                spec.constructor_id
            )));
        }
    }
    let mut flags = [0_u32; 4];
    let mut values: Vec<Option<Py<PyAny>>> = (0..spec.value_count).map(|_| None).collect();
    for field in spec.fields {
        match *field {
            FastFieldSpec::Flags { group } => {
                if group >= flags.len() {
                    return Err(PyValueError::new_err("generated TL flag group is invalid"));
                }
                flags[group] = u32::from_le_bytes(read_fixed::<4>(data, cursor)?);
                cursor += 4;
            }
            FastFieldSpec::True { value, group, bit } => {
                let group_flags = *flags
                    .get(group)
                    .ok_or_else(|| PyValueError::new_err("generated TL flag group is invalid"))?;
                values[value] = Some((group_flags & (1_u32 << bit) != 0).into_py_any(py)?);
            }
            FastFieldSpec::Value { value, wire_type } => {
                let decoded = decode_fast_value(py, data, &mut cursor, wire_type)?;
                values[value] = Some(decoded);
            }
        }
    }
    let values = values
        .into_iter()
        .enumerate()
        .map(|(index, value)| {
            value.ok_or_else(|| {
                PyValueError::new_err(format!("generated TL value {index} was not decoded"))
            })
        })
        .collect::<PyResult<Vec<_>>>()?;
    Ok(Some((PyTuple::new(py, values)?.unbind(), cursor)))
}

/// Appends one generated field value to a fast-path TL output buffer.
///
/// Returns a Python exception for incompatible Python values, unrepresentable sizes or an
/// encode-only generated object mismatch.
///
/// # Arguments
///
/// - `output`: Destination buffer receiving the encoded field.
/// - `value`: Python value to convert according to `wire_type`.
/// - `wire_type`: Trusted generated representation directive for `value`.
fn encode_fast_value(
    output: &mut Vec<u8>,
    value: &Bound<'_, PyAny>,
    wire_type: FastWireType,
) -> PyResult<()> {
    match wire_type {
        FastWireType::Int => output.extend_from_slice(&value.extract::<i32>()?.to_le_bytes()),
        FastWireType::Long => output.extend_from_slice(&value.extract::<i64>()?.to_le_bytes()),
        FastWireType::UInt64 => output.extend_from_slice(&value.extract::<u64>()?.to_le_bytes()),
        FastWireType::Bytes => append_tl_bytes(output, value.cast::<PyBytes>()?.as_bytes())?,
        FastWireType::String => append_tl_bytes(output, value.extract::<String>()?.as_bytes())?,
        FastWireType::VectorLong => {
            let encoded = encode_i64_vector(&value.extract::<Vec<i64>>()?)?;
            output.extend_from_slice(&encoded);
        }
        FastWireType::Object | FastWireType::EmptyObject | FastWireType::Raw => {
            output.extend_from_slice(value.cast::<PyBytes>()?.as_bytes());
        }
        FastWireType::MessageContainer => {
            let messages = value.extract::<Vec<(i64, i32, Vec<u8>)>>()?;
            let count = i32::try_from(messages.len())
                .map_err(|_| PyValueError::new_err("MTProto container count exceeds int32"))?;
            output.extend_from_slice(&count.to_le_bytes());
            for (msg_id, seq_no, body) in messages {
                let body_len = i32::try_from(body.len())
                    .map_err(|_| PyValueError::new_err("MTProto container body exceeds int32"))?;
                output.extend_from_slice(&msg_id.to_le_bytes());
                output.extend_from_slice(&seq_no.to_le_bytes());
                output.extend_from_slice(&body_len.to_le_bytes());
                output.extend_from_slice(&body);
            }
        }
    }
    Ok(())
}

/// Decodes one generated field from `data`, advancing `cursor` and creating a Python value.
///
/// Returns a Python exception for malformed data or unsupported generated decode types; requires
/// the GIL through `py` because the result is a Python object.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to create the decoded Python value.
/// - `data`: Complete TL input buffer.
/// - `cursor`: Mutable offset advanced past the decoded field.
/// - `wire_type`: Trusted generated representation directive for the field.
fn decode_fast_value(
    py: Python<'_>,
    data: &[u8],
    cursor: &mut usize,
    wire_type: FastWireType,
) -> PyResult<Py<PyAny>> {
    match wire_type {
        FastWireType::Int => {
            let value = i32::from_le_bytes(read_fixed::<4>(data, *cursor)?);
            *cursor += 4;
            value.into_py_any(py)
        }
        FastWireType::Long => {
            let value = i64::from_le_bytes(read_fixed::<8>(data, *cursor)?);
            *cursor += 8;
            value.into_py_any(py)
        }
        FastWireType::UInt64 => {
            let value = u64::from_le_bytes(read_fixed::<8>(data, *cursor)?);
            *cursor += 8;
            value.into_py_any(py)
        }
        FastWireType::Bytes => {
            let (value, next) = decode_tl_bytes_slice(data, *cursor)?;
            *cursor = next;
            Ok(PyBytes::new(py, value).into_any().unbind())
        }
        FastWireType::String => {
            let (value, next) = decode_tl_bytes_slice(data, *cursor)?;
            *cursor = next;
            let value = std::str::from_utf8(value)
                .map_err(|_| PyValueError::new_err("TL string payload is not valid UTF-8"))?;
            value.into_py_any(py)
        }
        FastWireType::VectorLong => {
            let (value, next) = decode_i64_vector(data, *cursor)?;
            *cursor = next;
            Ok(PyTuple::new(py, value)?.into_any().unbind())
        }
        FastWireType::EmptyObject => {
            let constructor_id = u32::from_le_bytes(read_fixed::<4>(data, *cursor)?);
            *cursor += 4;
            constructor_id.into_py_any(py)
        }
        FastWireType::Raw => {
            read_slice(data, *cursor, 0)?;
            let value = PyBytes::new(py, &data[*cursor..]).into_any().unbind();
            *cursor = data.len();
            Ok(value)
        }
        FastWireType::MessageContainer => decode_message_container(py, data, cursor),
        FastWireType::Object => Err(PyValueError::new_err(
            "generated TL object fields are encode-only",
        )),
    }
}

/// Decodes an MTProto message-container field into a Python tuple of `(id, seq_no, body)` tuples.
///
/// Advances `cursor` and returns Python exceptions for truncated, negative, oversized, or
/// unallocatable container contents.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to create the result tuple and bytes objects.
/// - `data`: Complete TL input buffer containing the container.
/// - `cursor`: Mutable offset advanced past every decoded member.
fn decode_message_container(
    py: Python<'_>,
    data: &[u8],
    cursor: &mut usize,
) -> PyResult<Py<PyAny>> {
    let count = i32::from_le_bytes(read_fixed::<4>(data, *cursor)?);
    *cursor += 4;
    if count < 0 {
        return Err(PyValueError::new_err(
            "MTProto container count cannot be negative",
        ));
    }
    let count = usize::try_from(count)
        .map_err(|_| PyValueError::new_err("MTProto container count is invalid"))?;
    let minimum = count
        .checked_mul(16)
        .ok_or_else(|| PyValueError::new_err("MTProto container size overflow"))?;
    read_slice(data, *cursor, minimum)?;
    let mut messages = Vec::new();
    messages
        .try_reserve_exact(count)
        .map_err(|_| PyMemoryError::new_err("failed to allocate MTProto container values"))?;
    for _ in 0..count {
        let msg_id = i64::from_le_bytes(read_fixed::<8>(data, *cursor)?);
        *cursor += 8;
        let seq_no = i32::from_le_bytes(read_fixed::<4>(data, *cursor)?);
        *cursor += 4;
        let body_len = i32::from_le_bytes(read_fixed::<4>(data, *cursor)?);
        *cursor += 4;
        if body_len < 0 {
            return Err(PyValueError::new_err(
                "MTProto container item length is invalid",
            ));
        }
        let body = read_slice(data, *cursor, body_len as usize)?;
        *cursor += body.len();
        messages.push(
            PyTuple::new(
                py,
                [
                    msg_id.into_py_any(py)?,
                    seq_no.into_py_any(py)?,
                    PyBytes::new(py, body).into_any().unbind(),
                ],
            )?
            .into_any()
            .unbind(),
        );
    }
    Ok(PyTuple::new(py, messages)?.into_any().unbind())
}

/// Encodes and appends a bounded TL bytes value, reserving its output atomically.
///
/// Returns `ValueError` above TL's 24-bit limit or `MemoryError` on allocation failure.
///
/// # Arguments
///
/// - `output`: Destination buffer receiving the encoded TL bytes field.
/// - `value`: Raw bytes to prefix and pad.
fn append_tl_bytes(output: &mut Vec<u8>, value: &[u8]) -> PyResult<()> {
    if value.len() > MAX_TL_BYTES_LENGTH {
        return Err(PyValueError::new_err(
            "TL bytes payload exceeds 24-bit length",
        ));
    }
    let encoded = encode_tl_bytes(value);
    output
        .try_reserve(encoded.len())
        .map_err(|_| PyMemoryError::new_err("failed to allocate TL fast-path output"))?;
    output.extend_from_slice(&encoded);
    Ok(())
}

/// Borrows one padded TL bytes payload and returns it with its next aligned offset.
///
/// Returns `ValueError` if the length prefix, payload, padding or offset is malformed.
///
/// # Arguments
///
/// - `data`: Complete TL input buffer.
/// - `offset`: Byte offset at which the TL bytes length prefix starts.
fn decode_tl_bytes_slice(data: &[u8], offset: usize) -> PyResult<(&[u8], usize)> {
    let first = *data
        .get(offset)
        .ok_or_else(|| PyValueError::new_err("TL data ended before bytes length"))?;
    let (length, payload_offset) = if first == 254 {
        let length_bytes = read_slice(data, offset + 1, 3)?;
        (
            u32::from_le_bytes([length_bytes[0], length_bytes[1], length_bytes[2], 0]) as usize,
            offset + 4,
        )
    } else {
        (first as usize, offset + 1)
    };
    let payload = read_slice(data, payload_offset, length)?;
    let next_offset = payload_offset
        .checked_add(length)
        .and_then(|value| value.checked_add((4 - value % 4) % 4))
        .ok_or_else(|| PyValueError::new_err("TL bytes payload offset overflow"))?;
    if next_offset > data.len() {
        return Err(PyValueError::new_err("TL data ended before bytes padding"));
    }
    Ok((payload, next_offset))
}

/// Encodes Python `tl_encode_int(value)` as a four-byte little-endian signed integer.
///
/// # Arguments
///
/// - `value`: Signed 32-bit integer to serialize.
#[pyfunction]
fn tl_encode_int(value: i32) -> Vec<u8> {
    value.to_le_bytes().to_vec()
}

/// Decodes Python `tl_decode_int(data, offset)` and returns `(value, next_offset)` or `ValueError`.
///
/// # Arguments
///
/// - `data`: TL bytes containing a four-byte signed integer.
/// - `offset`: Byte offset at which the integer starts.
#[pyfunction]
fn tl_decode_int(data: &[u8], offset: usize) -> PyResult<(i32, usize)> {
    let bytes = read_fixed::<4>(data, offset)?;
    Ok((i32::from_le_bytes(bytes), offset + 4))
}

/// Encodes Python `tl_encode_uint(value)` as a four-byte little-endian unsigned integer.
///
/// # Arguments
///
/// - `value`: Unsigned 32-bit integer to serialize.
#[pyfunction]
fn tl_encode_uint(value: u32) -> Vec<u8> {
    value.to_le_bytes().to_vec()
}

/// Decodes Python `tl_decode_uint(data, offset)` and returns `(value, next_offset)` or `ValueError`.
///
/// # Arguments
///
/// - `data`: TL bytes containing a four-byte unsigned integer.
/// - `offset`: Byte offset at which the integer starts.
#[pyfunction]
fn tl_decode_uint(data: &[u8], offset: usize) -> PyResult<(u32, usize)> {
    let bytes = read_fixed::<4>(data, offset)?;
    Ok((u32::from_le_bytes(bytes), offset + 4))
}

/// Encodes Python `tl_encode_long(value)` as an eight-byte little-endian signed integer.
///
/// # Arguments
///
/// - `value`: Signed 64-bit integer to serialize.
#[pyfunction]
fn tl_encode_long(value: i64) -> Vec<u8> {
    value.to_le_bytes().to_vec()
}

/// Decodes Python `tl_decode_long(data, offset)` and returns `(value, next_offset)` or `ValueError`.
///
/// # Arguments
///
/// - `data`: TL bytes containing an eight-byte signed integer.
/// - `offset`: Byte offset at which the integer starts.
#[pyfunction]
fn tl_decode_long(data: &[u8], offset: usize) -> PyResult<(i64, usize)> {
    let bytes = read_fixed::<8>(data, offset)?;
    Ok((i64::from_le_bytes(bytes), offset + 8))
}

/// Encodes Python `tl_encode_int128(value)` to 16 little-endian bytes via `int.to_bytes`.
///
/// Python raises if `value` cannot fit the requested unsigned representation.
///
/// # Arguments
///
/// - `value`: Python integer to convert to exactly 16 little-endian bytes.
#[pyfunction]
fn tl_encode_int128(value: &Bound<'_, PyAny>) -> PyResult<Vec<u8>> {
    py_int_to_le_bytes(value, 16)
}

/// Decodes Python `tl_decode_int128(data, offset)` to a Python integer and next offset.
///
/// Returns `ValueError` for truncated input and holds the GIL to construct the Python integer.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to construct the Python integer.
/// - `data`: TL bytes containing a 16-byte integer field.
/// - `offset`: Byte offset at which the fixed-width field starts.
#[pyfunction]
fn tl_decode_int128(py: Python<'_>, data: &[u8], offset: usize) -> PyResult<(Py<PyAny>, usize)> {
    let value = py_int_from_le_bytes(py, read_slice(data, offset, 16)?)?;
    Ok((value, offset + 16))
}

/// Encodes Python `tl_encode_int256(value)` to 32 little-endian bytes via `int.to_bytes`.
///
/// Python raises if `value` cannot fit the requested unsigned representation.
///
/// # Arguments
///
/// - `value`: Python integer to convert to exactly 32 little-endian bytes.
#[pyfunction]
fn tl_encode_int256(value: &Bound<'_, PyAny>) -> PyResult<Vec<u8>> {
    py_int_to_le_bytes(value, 32)
}

/// Decodes Python `tl_decode_int256(data, offset)` to a Python integer and next offset.
///
/// Returns `ValueError` for truncated input and holds the GIL to construct the Python integer.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to construct the Python integer.
/// - `data`: TL bytes containing a 32-byte integer field.
/// - `offset`: Byte offset at which the fixed-width field starts.
#[pyfunction]
fn tl_decode_int256(py: Python<'_>, data: &[u8], offset: usize) -> PyResult<(Py<PyAny>, usize)> {
    let value = py_int_from_le_bytes(py, read_slice(data, offset, 32)?)?;
    Ok((value, offset + 32))
}

/// Encodes Python `tl_encode_double(value)` as eight IEEE-754 little-endian bytes.
///
/// # Arguments
///
/// - `value`: Double-precision value to serialize.
#[pyfunction]
fn tl_encode_double(value: f64) -> Vec<u8> {
    value.to_le_bytes().to_vec()
}

/// Decodes Python `tl_decode_double(data, offset)` and returns `(value, next_offset)` or `ValueError`.
///
/// # Arguments
///
/// - `data`: TL bytes containing an eight-byte double.
/// - `offset`: Byte offset at which the double starts.
#[pyfunction]
fn tl_decode_double(data: &[u8], offset: usize) -> PyResult<(f64, usize)> {
    let bytes = read_fixed::<8>(data, offset)?;
    Ok((f64::from_le_bytes(bytes), offset + 8))
}

/// Encodes Python `tl_encode_bytes(value)` with TL's short/long length prefix and zero padding.
///
/// # Arguments
///
/// - `value`: Bytes to prefix and pad according to TL rules.
#[pyfunction]
fn tl_encode_bytes(value: &[u8]) -> Vec<u8> {
    encode_tl_bytes(value)
}

/// Decodes Python `tl_decode_bytes(data, offset)` and returns bytes plus the next aligned offset.
///
/// Returns `ValueError` for malformed or truncated TL data.
///
/// # Arguments
///
/// - `data`: TL bytes containing one length-prefixed byte field.
/// - `offset`: Byte offset at which the field starts.
#[pyfunction]
fn tl_decode_bytes(data: &[u8], offset: usize) -> PyResult<(Vec<u8>, usize)> {
    decode_tl_bytes(data, offset)
}

/// Encodes Python `tl_encode_string(value)` as UTF-8 TL bytes.
///
/// # Arguments
///
/// - `value`: UTF-8 Rust string to encode as TL bytes.
#[pyfunction]
fn tl_encode_string(value: &str) -> Vec<u8> {
    encode_tl_bytes(value.as_bytes())
}

/// Decodes Python `tl_decode_string(data, offset)` as UTF-8 and returns it with the next offset.
///
/// Returns `ValueError` for malformed TL data or non-UTF-8 payload bytes.
///
/// # Arguments
///
/// - `data`: TL bytes containing one length-prefixed string field.
/// - `offset`: Byte offset at which the field starts.
#[pyfunction]
fn tl_decode_string(data: &[u8], offset: usize) -> PyResult<(String, usize)> {
    let (bytes, new_offset) = decode_tl_bytes(data, offset)?;
    String::from_utf8(bytes)
        .map(|value| (value, new_offset))
        .map_err(|_| PyValueError::new_err("TL string payload is not valid UTF-8"))
}

/// Encodes Python `tl_encode_int_vector(values)` as a generic TL vector of 32-bit integers.
///
/// Large vector encoding releases the GIL; invalid size or allocation raises a Python exception.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach large vector encoding.
/// - `values`: Signed 32-bit values to serialize.
#[pyfunction]
fn tl_encode_int_vector(py: Python<'_>, values: Vec<i32>) -> PyResult<Vec<u8>> {
    let work_bytes = values.len().saturating_mul(4);
    detach_if_large(py, work_bytes, move || encode_i32_vector(&values))
}

/// Decodes Python `tl_decode_int_vector(data, offset)` into values and a next offset.
///
/// The signed Python offset must fit `usize`; large decoding releases the GIL and malformed input
/// returns a Python exception.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach large vector decoding.
/// - `data`: TL bytes containing a generic integer vector.
/// - `offset`: Python-facing signed byte offset that must convert to `usize`.
#[pyfunction]
fn tl_decode_int_vector(
    py: Python<'_>,
    data: Vec<u8>,
    offset: i128,
) -> PyResult<(Vec<i32>, usize)> {
    let offset = normalize_vector_offset(offset)?;
    let work_bytes = data.len().saturating_sub(offset);
    detach_if_large(py, work_bytes, move || decode_i32_vector(&data, offset))
}

/// Encodes Python `tl_encode_long_vector(values)` as a generic TL vector of 64-bit integers.
///
/// Large vector encoding releases the GIL; invalid size or allocation raises a Python exception.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach large vector encoding.
/// - `values`: Signed 64-bit values to serialize.
#[pyfunction]
fn tl_encode_long_vector(py: Python<'_>, values: Vec<i64>) -> PyResult<Vec<u8>> {
    let work_bytes = values.len().saturating_mul(8);
    detach_if_large(py, work_bytes, move || encode_i64_vector(&values))
}

/// Decodes Python `tl_decode_long_vector(data, offset)` into values and a next offset.
///
/// The signed Python offset must fit `usize`; large decoding releases the GIL and malformed input
/// returns a Python exception.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach large vector decoding.
/// - `data`: TL bytes containing a generic long vector.
/// - `offset`: Python-facing signed byte offset that must convert to `usize`.
#[pyfunction]
fn tl_decode_long_vector(
    py: Python<'_>,
    data: Vec<u8>,
    offset: i128,
) -> PyResult<(Vec<i64>, usize)> {
    let offset = normalize_vector_offset(offset)?;
    let work_bytes = data.len().saturating_sub(offset);
    detach_if_large(py, work_bytes, move || decode_i64_vector(&data, offset))
}

/// Borrows `length` bytes at `offset` from a TL buffer.
///
/// Returns `ValueError` rather than panicking if the requested range is not present.
///
/// # Arguments
///
/// - `data`: Complete TL input buffer.
/// - `offset`: Byte offset at which the requested range begins.
/// - `length`: Number of bytes to borrow.
pub(crate) fn read_slice(data: &[u8], offset: usize, length: usize) -> PyResult<&[u8]> {
    data.get(offset..offset.saturating_add(length))
        .ok_or_else(|| {
            PyValueError::new_err("TL data ended before the requested value could be decoded")
        })
}

/// Reads an exactly `N`-byte TL field at `offset`.
///
/// Returns `ValueError` for a truncated buffer; its `expect` is safe after `read_slice` verified
/// the length.
///
/// # Arguments
///
/// - `N`: Compile-time fixed width required by the caller.
/// - `data`: Complete TL input buffer.
/// - `offset`: Byte offset at which the fixed-width field begins.
pub(crate) fn read_fixed<const N: usize>(data: &[u8], offset: usize) -> PyResult<[u8; N]> {
    read_slice(data, offset, N).map(|slice| slice.try_into().expect("slice length checked"))
}

/// Serializes bytes with the TL short/long length prefix and zero alignment padding.
///
/// This internal helper assumes the caller has enforced TL's 24-bit long-length maximum.
///
/// # Arguments
///
/// - `value`: Bytes to length-prefix and pad to a four-byte boundary.
pub(crate) fn encode_tl_bytes(value: &[u8]) -> Vec<u8> {
    let length = value.len();
    let mut output = Vec::with_capacity(length + 8);
    if length <= 253 {
        output.push(length as u8);
    } else {
        output.push(254);
        output.extend_from_slice(&(length as u32).to_le_bytes()[..3]);
    }
    output.extend_from_slice(value);
    while output.len() % 4 != 0 {
        output.push(0);
    }
    output
}

/// Parses and copies one padded TL bytes value, returning it and its next aligned offset.
///
/// Returns `ValueError` for missing length, payload or padding bytes.
///
/// # Arguments
///
/// - `data`: Complete TL input buffer.
/// - `offset`: Byte offset at which the bytes field starts.
pub(crate) fn decode_tl_bytes(data: &[u8], offset: usize) -> PyResult<(Vec<u8>, usize)> {
    let first = *data
        .get(offset)
        .ok_or_else(|| PyValueError::new_err("TL data ended before bytes length"))?;
    let (length, payload_offset) = if first == 254 {
        let length_bytes = read_slice(data, offset + 1, 3)?;
        let length =
            u32::from_le_bytes([length_bytes[0], length_bytes[1], length_bytes[2], 0]) as usize;
        (length, offset + 4)
    } else {
        (first as usize, offset + 1)
    };
    let payload = read_slice(data, payload_offset, length)?.to_vec();
    let mut next_offset = payload_offset + length;
    while next_offset % 4 != 0 {
        next_offset += 1;
    }
    if next_offset > data.len() {
        return Err(PyValueError::new_err("TL data ended before bytes padding"));
    }
    Ok((payload, next_offset))
}

/// Calls Python `int.to_bytes(width, "little")` for fixed-width unsigned TL integer fields.
///
/// Propagates Python conversion exceptions and returns `ValueError` for an unexpected width.
///
/// # Arguments
///
/// - `value`: Python integer exposing `to_bytes`.
/// - `width`: Required serialized width in bytes.
fn py_int_to_le_bytes(value: &Bound<'_, PyAny>, width: usize) -> PyResult<Vec<u8>> {
    let bytes = value
        .call_method1("to_bytes", (width, "little"))?
        .extract::<Vec<u8>>()?;
    if bytes.len() != width {
        return Err(PyValueError::new_err("integer width mismatch"));
    }
    Ok(bytes)
}

/// Calls Python `int.from_bytes(bytes, "little")` while holding the supplied GIL token.
///
/// Returns any exception raised while importing or invoking Python builtins.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to import and invoke Python builtins.
/// - `bytes`: Little-endian bytes to pass to `int.from_bytes`.
fn py_int_from_le_bytes(py: Python<'_>, bytes: &[u8]) -> PyResult<Py<PyAny>> {
    let builtins = PyModule::import(py, "builtins")?;
    let py_bytes = PyBytes::new(py, bytes);
    let value = builtins
        .getattr("int")?
        .call_method1("from_bytes", (py_bytes, "little"))?;
    Ok(value.unbind())
}

/// Serializes signed 32-bit values as a generic boxed TL vector.
///
/// Returns `ValueError` for an unrepresentable count or `MemoryError` on allocation failure.
///
/// # Arguments
///
/// - `values`: Signed 32-bit vector elements to serialize.
fn encode_i32_vector(values: &[i32]) -> PyResult<Vec<u8>> {
    let capacity = checked_vector_capacity(values.len(), 4)?;
    let mut output = Vec::new();
    output
        .try_reserve_exact(capacity)
        .map_err(|_| PyMemoryError::new_err("failed to allocate TL vector"))?;
    output.extend_from_slice(&TL_VECTOR_CONSTRUCTOR_ID.to_le_bytes());
    output.extend_from_slice(&(values.len() as i32).to_le_bytes());
    for value in values {
        output.extend_from_slice(&value.to_le_bytes());
    }
    Ok(output)
}

/// Decodes a generic TL vector of signed 32-bit values at `offset`.
///
/// Returns values with the next offset or Python errors for malformed sizes or allocation failure.
///
/// # Arguments
///
/// - `data`: Complete TL input buffer.
/// - `offset`: Byte offset at which the generic vector begins.
fn decode_i32_vector(data: &[u8], offset: usize) -> PyResult<(Vec<i32>, usize)> {
    let (count, payload_offset, next_offset) = decode_vector_layout(data, offset, 4)?;
    validate_vector_allocation(count, size_of::<i32>())?;
    let mut values = Vec::new();
    values
        .try_reserve_exact(count)
        .map_err(|_| PyMemoryError::new_err("failed to allocate TL vector"))?;
    for bytes in data[payload_offset..next_offset].chunks_exact(4) {
        values.push(i32::from_le_bytes(
            bytes.try_into().expect("vector element width checked"),
        ));
    }
    Ok((values, next_offset))
}

/// Serializes signed 64-bit values as a generic boxed TL vector.
///
/// Returns `ValueError` for an unrepresentable count or `MemoryError` on allocation failure.
///
/// # Arguments
///
/// - `values`: Signed 64-bit vector elements to serialize.
fn encode_i64_vector(values: &[i64]) -> PyResult<Vec<u8>> {
    let capacity = checked_vector_capacity(values.len(), 8)?;
    let mut output = Vec::new();
    output
        .try_reserve_exact(capacity)
        .map_err(|_| PyMemoryError::new_err("failed to allocate TL vector"))?;
    output.extend_from_slice(&TL_VECTOR_CONSTRUCTOR_ID.to_le_bytes());
    output.extend_from_slice(&(values.len() as i32).to_le_bytes());
    for value in values {
        output.extend_from_slice(&value.to_le_bytes());
    }
    Ok(output)
}

/// Decodes a generic TL vector of signed 64-bit values at `offset`.
///
/// Returns values with the next offset or Python errors for malformed sizes or allocation failure.
///
/// # Arguments
///
/// - `data`: Complete TL input buffer.
/// - `offset`: Byte offset at which the generic vector begins.
fn decode_i64_vector(data: &[u8], offset: usize) -> PyResult<(Vec<i64>, usize)> {
    let (count, payload_offset, next_offset) = decode_vector_layout(data, offset, 8)?;
    validate_vector_allocation(count, size_of::<i64>())?;
    let mut values = Vec::new();
    values
        .try_reserve_exact(count)
        .map_err(|_| PyMemoryError::new_err("failed to allocate TL vector"))?;
    for bytes in data[payload_offset..next_offset].chunks_exact(8) {
        values.push(i64::from_le_bytes(
            bytes.try_into().expect("vector element width checked"),
        ));
    }
    Ok((values, next_offset))
}

/// Validates a generic vector header and returns its count, payload start and next offset.
///
/// Returns `ValueError` for a wrong constructor, negative/excessive count or arithmetic overflow.
/// The subtraction used to calculate remaining bytes cannot underflow: the preceding checked
/// header slice exists only when `payload_offset <= data.len()`. This function has no panic path
/// for externally supplied `data`; its `expect` calls follow exact-width checked slices.
///
/// # Arguments
///
/// - `data`: Complete TL input buffer.
/// - `offset`: Byte offset at which the vector constructor id starts.
/// - `element_width`: Nonzero byte width of one decoded element; callers use 4 or 8. A zero width
///   would panic in the remaining-bytes division and is therefore an internal precondition.
fn decode_vector_layout(
    data: &[u8],
    offset: usize,
    element_width: usize,
) -> PyResult<(usize, usize, usize)> {
    let payload_offset = offset
        .checked_add(8)
        .ok_or_else(|| PyValueError::new_err("TL vector header offset overflow"))?;
    let header = data.get(offset..payload_offset).ok_or_else(|| {
        PyValueError::new_err("TL data ended before the requested value could be decoded")
    })?;
    let constructor_id = u32::from_le_bytes(header[..4].try_into().expect("header width checked"));
    if constructor_id != TL_VECTOR_CONSTRUCTOR_ID {
        return Err(PyValueError::new_err(format!(
            "expected Vector constructor, got 0x{constructor_id:08x}",
        )));
    }
    let count = i32::from_le_bytes(header[4..].try_into().expect("header width checked"));
    if count < 0 {
        return Err(PyValueError::new_err("TL vector count cannot be negative"));
    }
    let count = count as usize;
    let remaining = data.len() - payload_offset;
    if count > remaining / element_width {
        return Err(PyValueError::new_err(
            "vector count exceeds remaining payload",
        ));
    }
    let payload_length = count
        .checked_mul(element_width)
        .ok_or_else(|| PyValueError::new_err("TL vector payload length overflow"))?;
    let next_offset = payload_offset
        .checked_add(payload_length)
        .ok_or_else(|| PyValueError::new_err("TL vector payload offset overflow"))?;
    Ok((count, payload_offset, next_offset))
}

/// Converts the Python-facing signed offset to a safe Rust index.
///
/// Returns `ValueError` for negative or unrepresentable offsets.
///
/// # Arguments
///
/// - `offset`: Python-facing signed byte offset to convert.
fn normalize_vector_offset(offset: i128) -> PyResult<usize> {
    usize::try_from(offset).map_err(|_| {
        PyValueError::new_err("TL data ended before the requested value could be decoded")
    })
}

/// Checks that a decoded vector's requested allocation fits the platform's `isize` limit.
///
/// Returns `ValueError` before allocation on overflow or an excessive capacity.
///
/// # Arguments
///
/// - `count`: Number of vector elements requested by decoded wire data.
/// - `element_width`: Byte width of one element used for capacity calculation.
fn validate_vector_allocation(count: usize, element_width: usize) -> PyResult<()> {
    let capacity = count
        .checked_mul(element_width)
        .ok_or_else(|| PyValueError::new_err("TL vector capacity overflow"))?;
    if capacity > isize::MAX as usize {
        return Err(PyValueError::new_err("TL vector capacity overflow"));
    }
    Ok(())
}

/// Computes encoder capacity including the eight-byte TL vector header.
///
/// Returns `ValueError` when the count cannot fit signed TL `int` or the capacity is excessive.
///
/// # Arguments
///
/// - `count`: Number of vector elements to encode.
/// - `element_width`: Byte width of one serialized element.
fn checked_vector_capacity(count: usize, element_width: usize) -> PyResult<usize> {
    if count > i32::MAX as usize {
        return Err(PyValueError::new_err("vector count exceeds i32 limit"));
    }
    let capacity = count
        .checked_mul(element_width)
        .and_then(|payload_length| payload_length.checked_add(8))
        .ok_or_else(|| PyValueError::new_err("TL vector capacity overflow"))?;
    if capacity > isize::MAX as usize {
        return Err(PyValueError::new_err("TL vector capacity overflow"));
    }
    Ok(capacity)
}

/// Unit tests for TL primitives, vectors and generated native fast paths.
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    /// Checks fixed-width integer codec round-trips.
    fn integers_roundtrip() {
        let int = tl_encode_int(-123456);
        assert_eq!(tl_decode_int(&int, 0).unwrap(), (-123456, 4));
        let uint = tl_encode_uint(0xf1234567);
        assert_eq!(tl_decode_uint(&uint, 0).unwrap(), (0xf1234567, 4));
        let long = tl_encode_long(-123456789012345678);
        assert_eq!(tl_decode_long(&long, 0).unwrap(), (-123456789012345678, 8));
    }

    #[test]
    /// Checks short TL bytes and strings round-trip with four-byte padding.
    fn bytes_and_string_roundtrip_with_padding() {
        let encoded = encode_tl_bytes(b"telegram");
        assert_eq!(encoded.len() % 4, 0);
        assert_eq!(
            decode_tl_bytes(&encoded, 0).unwrap(),
            (b"telegram".to_vec(), 12)
        );

        let encoded = tl_encode_string("telegram");
        assert_eq!(
            tl_decode_string(&encoded, 0).unwrap(),
            ("telegram".to_string(), 12)
        );
    }

    #[test]
    /// Checks the three-byte TL long-length header with a payload above 253 bytes.
    fn large_bytes_header_roundtrips() {
        let payload = vec![7; 300];
        let encoded = encode_tl_bytes(&payload);
        assert_eq!(encoded[0], 254);
        assert_eq!(decode_tl_bytes(&encoded, 0).unwrap(), (payload, 304));
    }

    #[test]
    /// Checks 32-bit and 64-bit generic vector round-trips.
    fn vectors_roundtrip() {
        let int_values = vec![-1, 0, 1, 2];
        let encoded = encode_i32_vector(&int_values).unwrap();
        assert_eq!(decode_i32_vector(&encoded, 0).unwrap(), (int_values, 24));

        let long_values = vec![-1, 0, 1, 1_i64 << 40];
        let encoded = encode_i64_vector(&long_values).unwrap();
        assert_eq!(decode_i64_vector(&encoded, 0).unwrap(), (long_values, 40));
    }

    #[test]
    /// Ensures vector decoders reject counts exceeding the available payload.
    fn vector_decoders_reject_counts_exceeding_remaining_payload() {
        Python::initialize();
        let mut encoded = TL_VECTOR_CONSTRUCTOR_ID.to_le_bytes().to_vec();
        encoded.extend_from_slice(&2_i32.to_le_bytes());
        encoded.extend_from_slice(&[0; 7]);
        assert!(
            decode_i32_vector(&encoded, 0)
                .unwrap_err()
                .to_string()
                .contains("vector count exceeds remaining payload")
        );

        let mut encoded = TL_VECTOR_CONSTRUCTOR_ID.to_le_bytes().to_vec();
        encoded.extend_from_slice(&2_i32.to_le_bytes());
        encoded.extend_from_slice(&[0; 15]);
        assert!(
            decode_i64_vector(&encoded, 0)
                .unwrap_err()
                .to_string()
                .contains("vector count exceeds remaining payload")
        );
    }

    #[test]
    /// Ensures encoder and decoder allocation limits reject overflowing capacities.
    fn vector_capacity_rejects_i32_count_overflow() {
        Python::initialize();
        assert!(
            checked_vector_capacity(i32::MAX as usize + 1, 4)
                .unwrap_err()
                .to_string()
                .contains("vector count exceeds i32 limit")
        );
        assert!(
            validate_vector_allocation(usize::MAX, 8)
                .unwrap_err()
                .to_string()
                .contains("TL vector capacity overflow")
        );
    }

    #[test]
    /// Ensures vector decoders return the offset before unrelated trailing bytes.
    fn vector_decoders_preserve_trailing_bytes() {
        let prefix = b"pre";
        let int_values = vec![-2, 0, 3];
        let encoded = encode_i32_vector(&int_values).unwrap();
        let mut data = prefix.to_vec();
        data.extend_from_slice(&encoded);
        data.extend_from_slice(b"trailing");
        assert_eq!(
            decode_i32_vector(&data, prefix.len()).unwrap(),
            (int_values, prefix.len() + encoded.len())
        );

        let long_values = vec![-(1_i64 << 40), 0, 1_i64 << 40];
        let encoded = encode_i64_vector(&long_values).unwrap();
        let mut data = prefix.to_vec();
        data.extend_from_slice(&encoded);
        data.extend_from_slice(b"trailing");
        assert_eq!(
            decode_i64_vector(&data, prefix.len()).unwrap(),
            (long_values, prefix.len() + encoded.len())
        );
    }

    #[test]
    /// Guards the generated fast-path table's expected unique-constructor count.
    fn generated_fast_path_table_has_thirty_unique_constructors() {
        assert_eq!(crate::generated_tl::FAST_CONSTRUCTORS.len(), 30);
        let mut ids = crate::generated_tl::FAST_CONSTRUCTORS
            .iter()
            .map(|spec| spec.constructor_id)
            .collect::<Vec<_>>();
        ids.sort_unstable();
        ids.dedup();
        assert_eq!(ids.len(), 30);
    }

    #[test]
    /// Exercises generated fast encode/decode paths for upload parts and long vectors.
    fn generated_upload_part_and_vector_service_roundtrip() {
        Python::initialize();
        Python::attach(|py| {
            let values = PyTuple::new(
                py,
                [
                    0x0102_0304_0506_0708_i64.into_py_any(py).unwrap(),
                    7_i32.into_py_any(py).unwrap(),
                    PyBytes::new(py, b"part").into_any().unbind(),
                ],
            )
            .unwrap();
            let encoded = tl_fast_encode(0xb304_a621, &values, true).unwrap().unwrap();
            assert_eq!(&encoded[..4], &0xb304_a621_u32.to_le_bytes());
            let (decoded, offset) = tl_fast_decode(py, 0xb304_a621, &encoded, 0, true)
                .unwrap()
                .unwrap();
            let decoded = decoded.bind(py);
            assert_eq!(offset, encoded.len());
            assert_eq!(
                decoded.get_item(0).unwrap().extract::<i64>().unwrap(),
                0x0102_0304_0506_0708
            );
            assert_eq!(decoded.get_item(1).unwrap().extract::<i32>().unwrap(), 7);
            assert_eq!(
                decoded.get_item(2).unwrap().extract::<Vec<u8>>().unwrap(),
                b"part"
            );

            let msg_ids = PyTuple::new(py, [-1_i64, 2_i64, 1_i64 << 40]).unwrap();
            let values = PyTuple::new(py, [msg_ids.into_any().unbind()]).unwrap();
            let encoded = tl_fast_encode(0x62d6_b459, &values, true).unwrap().unwrap();
            let (decoded, offset) = tl_fast_decode(py, 0x62d6_b459, &encoded, 0, true)
                .unwrap()
                .unwrap();
            let decoded = decoded.bind(py);
            assert_eq!(offset, encoded.len());
            assert_eq!(
                decoded.get_item(0).unwrap().extract::<Vec<i64>>().unwrap(),
                vec![-1, 2, 1_i64 << 40]
            );
        });
    }

    #[test]
    /// Ensures generated decoding rejects wrong constructors, truncation and overflowing offsets.
    fn generated_fast_decoder_rejects_wrong_constructor_and_truncation() {
        Python::initialize();
        Python::attach(|py| {
            let wrong = 0_u32.to_le_bytes();
            assert!(
                tl_fast_decode(py, 0x62d6_b459, &wrong, 0, true)
                    .unwrap_err()
                    .to_string()
                    .contains("expected constructor")
            );
            let truncated = 0x62d6_b459_u32.to_le_bytes();
            assert!(tl_fast_decode(py, 0x62d6_b459, &truncated, 0, true).is_err());
            assert!(tl_fast_decode(py, 0xf35c_6d01, &[], usize::MAX, false).is_err());
        });
    }
}
