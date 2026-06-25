use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

#[pyfunction]
fn native_available() -> bool {
    true
}

#[pyfunction]
fn xor_bytes(left: &[u8], right: &[u8]) -> PyResult<Vec<u8>> {
    if left.len() != right.len() {
        return Err(PyValueError::new_err(
            "xor inputs must have the same length",
        ));
    }

    Ok(left.iter().zip(right.iter()).map(|(a, b)| a ^ b).collect())
}

#[pymodule]
fn _native(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(native_available, m)?)?;
    m.add_function(wrap_pyfunction!(xor_bytes, m)?)?;
    Ok(())
}
