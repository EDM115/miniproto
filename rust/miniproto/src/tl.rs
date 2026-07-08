use pyo3::exceptions::PyValueError;
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
fn tl_encode_int_vector(py: Python<'_>, values: Vec<i32>) -> Vec<u8> {
    detach_if_large(py, values.len() * 4, move || encode_i32_vector(&values))
}

#[pyfunction]
fn tl_decode_int_vector(
    py: Python<'_>,
    data: Vec<u8>,
    offset: usize,
) -> PyResult<(Vec<i32>, usize)> {
    let work_bytes = data.len().saturating_sub(offset);
    detach_if_large(py, work_bytes, move || decode_i32_vector(&data, offset))
}

#[pyfunction]
fn tl_encode_long_vector(py: Python<'_>, values: Vec<i64>) -> Vec<u8> {
    detach_if_large(py, values.len() * 8, move || encode_i64_vector(&values))
}

#[pyfunction]
fn tl_decode_long_vector(
    py: Python<'_>,
    data: Vec<u8>,
    offset: usize,
) -> PyResult<(Vec<i64>, usize)> {
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

fn encode_i32_vector(values: &[i32]) -> Vec<u8> {
    let mut output = Vec::with_capacity(8 + values.len() * 4);
    output.extend_from_slice(&TL_VECTOR_CONSTRUCTOR_ID.to_le_bytes());
    output.extend_from_slice(&(values.len() as i32).to_le_bytes());
    for value in values {
        output.extend_from_slice(&value.to_le_bytes());
    }
    output
}

fn decode_i32_vector(data: &[u8], offset: usize) -> PyResult<(Vec<i32>, usize)> {
    validate_vector_constructor(data, offset)?;
    let count_bytes = read_fixed::<4>(data, offset + 4)?;
    let count = i32::from_le_bytes(count_bytes);
    if count < 0 {
        return Err(PyValueError::new_err("TL vector count cannot be negative"));
    }
    let count = count as usize;
    let mut next_offset = offset + 8;
    let mut values = Vec::with_capacity(count);
    for _ in 0..count {
        let bytes = read_fixed::<4>(data, next_offset)?;
        values.push(i32::from_le_bytes(bytes));
        next_offset += 4;
    }
    Ok((values, next_offset))
}

fn encode_i64_vector(values: &[i64]) -> Vec<u8> {
    let mut output = Vec::with_capacity(8 + values.len() * 8);
    output.extend_from_slice(&TL_VECTOR_CONSTRUCTOR_ID.to_le_bytes());
    output.extend_from_slice(&(values.len() as i32).to_le_bytes());
    for value in values {
        output.extend_from_slice(&value.to_le_bytes());
    }
    output
}

fn decode_i64_vector(data: &[u8], offset: usize) -> PyResult<(Vec<i64>, usize)> {
    validate_vector_constructor(data, offset)?;
    let count_bytes = read_fixed::<4>(data, offset + 4)?;
    let count = i32::from_le_bytes(count_bytes);
    if count < 0 {
        return Err(PyValueError::new_err("TL vector count cannot be negative"));
    }
    let count = count as usize;
    let mut next_offset = offset + 8;
    let mut values = Vec::with_capacity(count);
    for _ in 0..count {
        let bytes = read_fixed::<8>(data, next_offset)?;
        values.push(i64::from_le_bytes(bytes));
        next_offset += 8;
    }
    Ok((values, next_offset))
}

fn validate_vector_constructor(data: &[u8], offset: usize) -> PyResult<()> {
    let bytes = read_fixed::<4>(data, offset)?;
    let constructor_id = u32::from_le_bytes(bytes);
    if constructor_id != TL_VECTOR_CONSTRUCTOR_ID {
        return Err(PyValueError::new_err(format!(
            "expected Vector constructor, got 0x{constructor_id:08x}",
        )));
    }
    Ok(())
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
        let encoded = encode_i32_vector(&int_values);
        assert_eq!(decode_i32_vector(&encoded, 0).unwrap(), (int_values, 24));

        let long_values = vec![-1, 0, 1, 1_i64 << 40];
        let encoded = encode_i64_vector(&long_values);
        assert_eq!(decode_i64_vector(&encoded, 0).unwrap(), (long_values, 40));
    }
}
