//! Bundled PyO3 acceleration module for [`miniproto`](https://pypi.org/project/miniproto/).
//!
//! Python imports this crate as `miniproto._native` for cryptography, encrypted MTProto envelopes, selected TL codecs and TCP framing. Python wrappers select these functions or their fallbacks per operation.

use pyo3::prelude::*;
use pyo3::types::PyModule;

/// Registers cryptographic Python callables.
mod crypto;
/// Generated TL constructor metadata and field specifications.
///
/// This generated module is deliberately not hand-maintained.
mod generated_tl;
/// Registers encrypted MTProto message-envelope callables.
mod mtproto;
/// Registers primitive and generated fast-path TL codec callables.
mod tl;
/// Registers TCP transport framing callables and the stateful codec class.
mod transport;

/// Initializes Python module `miniproto._native`.
///
/// `gil_used = false` declares support for free-threaded Python. Python-object access still requires an attached thread, which holds the GIL on GIL-enabled builds. Selected exports detach for native work. Registration errors propagate as Python exceptions.
///
/// # Arguments
///
/// - `m`: The newly-created `miniproto._native` Python module receiving the registered exports.
#[pymodule(gil_used = false)]
fn _native(m: &Bound<'_, PyModule>) -> PyResult<()> {
    crypto::register(m)?;
    mtproto::register(m)?;
    tl::register(m)?;
    transport::register(m)?;
    Ok(())
}
