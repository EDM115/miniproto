use pyo3::IntoPyObjectExt;
use pyo3::exceptions::{PyMemoryError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyModule, PyTuple};
use pyo3::wrap_pyfunction;

use crate::crypto::detach_if_large;
use crate::generated_tl::fast_constructor;

const TL_VECTOR_CONSTRUCTOR_ID: u32 = 0x1CB5C415;
const MAX_TL_BYTES_LENGTH: usize = 0xFF_FFFF;

#[derive(Clone, Copy)]
pub(crate) enum FastWireType {
    Int,
    Long,
    UInt64,
    Bytes,
    String,
    VectorLong,
    Object,
    EmptyObject,
    Raw,
    MessageContainer,
}

#[derive(Clone, Copy)]
pub(crate) enum FastFieldSpec {
    Flags {
        group: usize,
    },
    True {
        value: usize,
        group: usize,
        bit: u32,
    },
    Value {
        value: usize,
        wire_type: FastWireType,
    },
}

pub(crate) struct FastConstructorSpec {
    pub(crate) constructor_id: u32,
    pub(crate) name: &'static str,
    pub(crate) encode: bool,
    pub(crate) decode: bool,
    pub(crate) value_count: usize,
    pub(crate) fields: &'static [FastFieldSpec],
}

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

#[pyfunction]
fn tl_encode_int(value: i32) -> Vec<u8> {
    value.to_le_bytes().to_vec()
}

#[pyfunction]
fn tl_decode_int(data: &[u8], offset: usize) -> PyResult<(i32, usize)> {
    let bytes = read_fixed::<4>(data, offset)?;
    Ok((i32::from_le_bytes(bytes), offset + 4))
}

#[pyfunction]
fn tl_encode_uint(value: u32) -> Vec<u8> {
    value.to_le_bytes().to_vec()
}

#[pyfunction]
fn tl_decode_uint(data: &[u8], offset: usize) -> PyResult<(u32, usize)> {
    let bytes = read_fixed::<4>(data, offset)?;
    Ok((u32::from_le_bytes(bytes), offset + 4))
}

#[pyfunction]
fn tl_encode_long(value: i64) -> Vec<u8> {
    value.to_le_bytes().to_vec()
}

#[pyfunction]
fn tl_decode_long(data: &[u8], offset: usize) -> PyResult<(i64, usize)> {
    let bytes = read_fixed::<8>(data, offset)?;
    Ok((i64::from_le_bytes(bytes), offset + 8))
}

#[pyfunction]
fn tl_encode_int128(value: &Bound<'_, PyAny>) -> PyResult<Vec<u8>> {
    py_int_to_le_bytes(value, 16)
}

#[pyfunction]
fn tl_decode_int128(py: Python<'_>, data: &[u8], offset: usize) -> PyResult<(Py<PyAny>, usize)> {
    let value = py_int_from_le_bytes(py, read_slice(data, offset, 16)?)?;
    Ok((value, offset + 16))
}

#[pyfunction]
fn tl_encode_int256(value: &Bound<'_, PyAny>) -> PyResult<Vec<u8>> {
    py_int_to_le_bytes(value, 32)
}

#[pyfunction]
fn tl_decode_int256(py: Python<'_>, data: &[u8], offset: usize) -> PyResult<(Py<PyAny>, usize)> {
    let value = py_int_from_le_bytes(py, read_slice(data, offset, 32)?)?;
    Ok((value, offset + 32))
}

#[pyfunction]
fn tl_encode_double(value: f64) -> Vec<u8> {
    value.to_le_bytes().to_vec()
}

#[pyfunction]
fn tl_decode_double(data: &[u8], offset: usize) -> PyResult<(f64, usize)> {
    let bytes = read_fixed::<8>(data, offset)?;
    Ok((f64::from_le_bytes(bytes), offset + 8))
}

#[pyfunction]
fn tl_encode_bytes(value: &[u8]) -> Vec<u8> {
    encode_tl_bytes(value)
}

#[pyfunction]
fn tl_decode_bytes(data: &[u8], offset: usize) -> PyResult<(Vec<u8>, usize)> {
    decode_tl_bytes(data, offset)
}

#[pyfunction]
fn tl_encode_string(value: &str) -> Vec<u8> {
    encode_tl_bytes(value.as_bytes())
}

#[pyfunction]
fn tl_decode_string(data: &[u8], offset: usize) -> PyResult<(String, usize)> {
    let (bytes, new_offset) = decode_tl_bytes(data, offset)?;
    String::from_utf8(bytes)
        .map(|value| (value, new_offset))
        .map_err(|_| PyValueError::new_err("TL string payload is not valid UTF-8"))
}

#[pyfunction]
fn tl_encode_int_vector(py: Python<'_>, values: Vec<i32>) -> PyResult<Vec<u8>> {
    let work_bytes = values.len().saturating_mul(4);
    detach_if_large(py, work_bytes, move || encode_i32_vector(&values))
}

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

#[pyfunction]
fn tl_encode_long_vector(py: Python<'_>, values: Vec<i64>) -> PyResult<Vec<u8>> {
    let work_bytes = values.len().saturating_mul(8);
    detach_if_large(py, work_bytes, move || encode_i64_vector(&values))
}

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

pub(crate) fn read_slice(data: &[u8], offset: usize, length: usize) -> PyResult<&[u8]> {
    data.get(offset..offset.saturating_add(length))
        .ok_or_else(|| {
            PyValueError::new_err("TL data ended before the requested value could be decoded")
        })
}

pub(crate) fn read_fixed<const N: usize>(data: &[u8], offset: usize) -> PyResult<[u8; N]> {
    read_slice(data, offset, N).map(|slice| slice.try_into().expect("slice length checked"))
}

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

fn py_int_to_le_bytes(value: &Bound<'_, PyAny>, width: usize) -> PyResult<Vec<u8>> {
    let bytes = value
        .call_method1("to_bytes", (width, "little"))?
        .extract::<Vec<u8>>()?;
    if bytes.len() != width {
        return Err(PyValueError::new_err("integer width mismatch"));
    }
    Ok(bytes)
}

fn py_int_from_le_bytes(py: Python<'_>, bytes: &[u8]) -> PyResult<Py<PyAny>> {
    let builtins = PyModule::import(py, "builtins")?;
    let py_bytes = PyBytes::new(py, bytes);
    let value = builtins
        .getattr("int")?
        .call_method1("from_bytes", (py_bytes, "little"))?;
    Ok(value.unbind())
}

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

fn normalize_vector_offset(offset: i128) -> PyResult<usize> {
    usize::try_from(offset).map_err(|_| {
        PyValueError::new_err("TL data ended before the requested value could be decoded")
    })
}

fn validate_vector_allocation(count: usize, element_width: usize) -> PyResult<()> {
    let capacity = count
        .checked_mul(element_width)
        .ok_or_else(|| PyValueError::new_err("TL vector capacity overflow"))?;
    if capacity > isize::MAX as usize {
        return Err(PyValueError::new_err("TL vector capacity overflow"));
    }
    Ok(())
}

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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn integers_roundtrip() {
        let int = tl_encode_int(-123456);
        assert_eq!(tl_decode_int(&int, 0).unwrap(), (-123456, 4));
        let uint = tl_encode_uint(0xf1234567);
        assert_eq!(tl_decode_uint(&uint, 0).unwrap(), (0xf1234567, 4));
        let long = tl_encode_long(-123456789012345678);
        assert_eq!(tl_decode_long(&long, 0).unwrap(), (-123456789012345678, 8));
    }

    #[test]
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
    fn large_bytes_header_roundtrips() {
        let payload = vec![7; 300];
        let encoded = encode_tl_bytes(&payload);
        assert_eq!(encoded[0], 254);
        assert_eq!(decode_tl_bytes(&encoded, 0).unwrap(), (payload, 304));
    }

    #[test]
    fn vectors_roundtrip() {
        let int_values = vec![-1, 0, 1, 2];
        let encoded = encode_i32_vector(&int_values).unwrap();
        assert_eq!(decode_i32_vector(&encoded, 0).unwrap(), (int_values, 24));

        let long_values = vec![-1, 0, 1, 1_i64 << 40];
        let encoded = encode_i64_vector(&long_values).unwrap();
        assert_eq!(decode_i64_vector(&encoded, 0).unwrap(), (long_values, 40));
    }

    #[test]
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
