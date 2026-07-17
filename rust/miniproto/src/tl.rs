use pyo3::exceptions::{PyMemoryError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::{PyBytes, PyModule};
use pyo3::wrap_pyfunction;

use crate::crypto::detach_if_large;

const TL_VECTOR_CONSTRUCTOR_ID: u32 = 0x1CB5C415;

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
    Ok(())
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
}
