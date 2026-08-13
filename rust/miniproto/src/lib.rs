use pyo3::prelude::*;
use pyo3::types::PyModule;

mod crypto;
mod generated_tl;
mod mtproto;
mod tl;
mod transport;

#[pymodule]
fn _native(m: &Bound<'_, PyModule>) -> PyResult<()> {
    crypto::register(m)?;
    mtproto::register(m)?;
    tl::register(m)?;
    transport::register(m)?;
    Ok(())
}
