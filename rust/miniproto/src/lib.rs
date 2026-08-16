//! Bundled PyO3 acceleration module for [`miniproto`](https://pypi.org/project/miniproto/).
//!
//! Python imports this crate as `miniproto._native`.  It registers native implementations for
//! cryptographic primitives, encrypted MTProto envelopes, selected TL codecs, and TCP transport
//! framing.  These routines are an optional acceleration layer: the Python package owns the
//! public fallback policy and must remain correct when this extension cannot be imported.

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
/// PyO3 declares this module usable without the GIL (`gil_used = false`), but individual exports
/// still acquire or release it as required by their Python-object interactions.  Returns a Python
/// exception if any submodule registration fails.
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
