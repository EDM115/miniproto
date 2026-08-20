//! Native cryptographic primitives used by MTProto and its Python fallback-compatible API.
//!
//! Each `#[pyfunction]` is exported under its Rust name in `miniproto._native`.  Byte-heavy
//! wrappers conditionally release the GIL, while `*_raw` functions are Rust-only building blocks
//! that never require it. PyO3 rejects incompatible Python argument conversion first, preserving
//! its `TypeError`, `OverflowError`, or source exception; algorithm and byte-shape validation in
//! this module intentionally return Python `ValueError`. No caller-facing unsafe API is exposed.

use aes::Aes256;
use aes_gcm::aead::consts::U12;
use aes_gcm::aead::{Aead, KeyInit, Payload};
use aes_gcm::{Aes256Gcm, Nonce};
use cipher::{BlockCipherDecrypt, BlockCipherEncrypt};
use pyo3::exceptions::PyValueError;
use pyo3::marker::Ungil;
use pyo3::prelude::*;
use pyo3::types::PyModule;
use pyo3::wrap_pyfunction;
use scrypt::{Params as ScryptParams, scrypt};
use sha1::Sha1;
use sha2::{Digest, Sha256};
use subtle::ConstantTimeEq;

/// AES's fixed block size in bytes.
pub(crate) const AES_BLOCK_SIZE: usize = 16;
/// Required byte length of an MTProto authorization key.
pub(crate) const MT_PROTO_AUTH_KEY_SIZE: usize = 256;
/// Required byte length of an MTProto 2.0 message key.
pub(crate) const MT_PROTO_MSG_KEY_SIZE: usize = 16;
/// Work-size threshold above which native wrappers detach from the Python GIL.
pub(crate) const GIL_RELEASE_THRESHOLD_BYTES: usize = 4 * 1024;
/// Maximum memory estimate accepted by the public scrypt primitive.
const SCRYPT_MAX_MEMORY_BYTES: usize = 256 * 1024 * 1024;
/// Maximum CPU-work estimate accepted by the public scrypt primitive.
const SCRYPT_MAX_WORK_BYTES: usize = 1024 * 1024 * 1024;

/// Runs `f` without the GIL when its input work estimate exceeds the native threshold.
///
/// `work_bytes` is an estimate used solely for GIL scheduling; `f` must satisfy PyO3's `Ungil`
/// requirements.  This helper preserves synchronous results and does not itself allocate.
///
/// # Arguments
///
/// - `T`: The GIL-independent result type returned by `f`.
/// - `F`: The one-shot GIL-independent closure performing the native operation.
/// - `py`: The acquired GIL token that can detach `f`.
/// - `work_bytes`: Conservative byte-work estimate compared with the detach threshold.
/// - `f`: The native computation to run attached or detached.
pub(crate) fn detach_if_large<T, F>(py: Python<'_>, work_bytes: usize, f: F) -> T
where
    T: Ungil,
    F: Ungil + FnOnce() -> T,
{
    if work_bytes > GIL_RELEASE_THRESHOLD_BYTES {
        py.detach(f)
    } else {
        f()
    }
}

/// Registers this module's fallback-compatible Python callables on `miniproto._native`.
///
/// Returns a PyO3 exception if a callable cannot be added to `m`.
///
/// # Arguments
///
/// - `m`: The Python extension module receiving the crypto callables.
pub fn register(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(native_available, m)?)?;
    m.add_function(wrap_pyfunction!(sha1_digest, m)?)?;
    m.add_function(wrap_pyfunction!(sha256_digest, m)?)?;
    m.add_function(wrap_pyfunction!(mtproto_auth_key_id, m)?)?;
    m.add_function(wrap_pyfunction!(mtproto_message_key, m)?)?;
    m.add_function(wrap_pyfunction!(mtproto_derive_aes_key_iv, m)?)?;
    m.add_function(wrap_pyfunction!(mtproto_encrypt_payload, m)?)?;
    m.add_function(wrap_pyfunction!(mtproto_decrypt_payload, m)?)?;
    m.add_function(wrap_pyfunction!(xor_bytes, m)?)?;
    m.add_function(wrap_pyfunction!(aes_256_ige_encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(aes_256_ige_decrypt, m)?)?;
    m.add_function(wrap_pyfunction!(aes_256_ctr_crypt, m)?)?;
    m.add_function(wrap_pyfunction!(aes_256_cbc_encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(aes_256_cbc_decrypt, m)?)?;
    m.add_function(wrap_pyfunction!(aes_256_gcm_encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(aes_256_gcm_decrypt, m)?)?;
    m.add_function(wrap_pyfunction!(scrypt_derive, m)?)?;
    m.add_function(wrap_pyfunction!(pq_factorize, m)?)?;
    Ok(())
}

/// Implements Python `native_available`, which always returns `true` while this compiled callable
/// is importable. Python fallback selection happens before this function can be called.
#[pyfunction]
fn native_available() -> bool {
    true
}

/// Computes Python `sha1_digest(data)` and returns the 20-byte SHA-1 digest.
///
/// Large inputs are hashed with the GIL released.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach a large hash operation.
/// - `data`: Bytes to hash.
#[pyfunction]
fn sha1_digest(py: Python<'_>, data: Vec<u8>) -> Vec<u8> {
    detach_if_large(py, data.len(), || sha1_digest_raw(&data))
}

/// Computes Python `sha256_digest(data)` and returns the 32-byte SHA-256 digest.
///
/// Large inputs are hashed with the GIL released.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach a large hash operation.
/// - `data`: Bytes to hash.
#[pyfunction]
fn sha256_digest(py: Python<'_>, data: Vec<u8>) -> Vec<u8> {
    detach_if_large(py, data.len(), || sha256_digest_raw(&data))
}

/// Computes Python `mtproto_auth_key_id(auth_key)` from a validated 256-byte key.
///
/// Returns `ValueError` when `auth_key` has the wrong length.
///
/// # Arguments
///
/// - `auth_key`: The 256-byte MTProto authorization key.
#[pyfunction]
fn mtproto_auth_key_id(auth_key: &[u8]) -> PyResult<Vec<u8>> {
    mtproto_auth_key_id_raw(auth_key)
}

/// Computes Python `mtproto_message_key` for padded plaintext and one MTProto direction.
///
/// Returns a 16-byte message key; rejects an invalid authorization key and releases the GIL for
/// large inputs.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach a large hash operation.
/// - `auth_key`: The 256-byte MTProto authorization key.
/// - `plaintext_with_padding`: Block-aligned inner plaintext that contributes to the message key.
/// - `client_to_server`: Selects the directional MTProto key offset.
#[pyfunction]
fn mtproto_message_key(
    py: Python<'_>,
    auth_key: Vec<u8>,
    plaintext_with_padding: Vec<u8>,
    client_to_server: bool,
) -> PyResult<Vec<u8>> {
    let work_bytes = auth_key.len() + plaintext_with_padding.len();
    detach_if_large(py, work_bytes, move || {
        validate_auth_key(&auth_key)?;
        Ok(mtproto_message_key_raw(
            &auth_key,
            &plaintext_with_padding,
            client_to_server,
        ))
    })
}

/// Derives the AES-256 key and IV used by Python `mtproto_derive_aes_key_iv`.
///
/// Returns `(key, iv)` and validates both fixed-width inputs. Valid inputs total 272 bytes
/// (`auth_key` 256 plus `msg_key` 16), so this wrapper never exceeds the detach threshold and
/// performs the derivation while holding the GIL.
///
/// # Arguments
///
/// - `py`: The acquired GIL token retained by this bounded-size operation.
/// - `auth_key`: The 256-byte MTProto authorization key.
/// - `msg_key`: The 16-byte MTProto message key.
/// - `client_to_server`: Selects the directional MTProto key offset.
#[pyfunction]
fn mtproto_derive_aes_key_iv(
    py: Python<'_>,
    auth_key: Vec<u8>,
    msg_key: Vec<u8>,
    client_to_server: bool,
) -> PyResult<(Vec<u8>, Vec<u8>)> {
    let work_bytes = auth_key.len() + msg_key.len();
    detach_if_large(py, work_bytes, move || {
        validate_auth_key(&auth_key)?;
        validate_msg_key(&msg_key)?;
        Ok(mtproto_derive_aes_key_iv_raw(
            &auth_key,
            &msg_key,
            client_to_server,
        ))
    })
}

/// Encrypts padded MTProto plaintext for Python `mtproto_encrypt_payload`.
///
/// Returns `(auth_key_id, msg_key, ciphertext)` or `ValueError` for invalid key or block input;
/// large work runs without the GIL.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach large encryption work.
/// - `auth_key`: The 256-byte MTProto authorization key.
/// - `plaintext_with_padding`: AES-block-aligned inner plaintext to encrypt.
/// - `client_to_server`: Selects the directional MTProto key schedule.
#[pyfunction]
fn mtproto_encrypt_payload(
    py: Python<'_>,
    auth_key: Vec<u8>,
    plaintext_with_padding: Vec<u8>,
    client_to_server: bool,
) -> PyResult<(Vec<u8>, Vec<u8>, Vec<u8>)> {
    let work_bytes = auth_key.len() + plaintext_with_padding.len();
    detach_if_large(py, work_bytes, move || {
        mtproto_encrypt_payload_raw(&auth_key, &plaintext_with_padding, client_to_server)
    })
}

/// Decrypts and verifies Python `mtproto_decrypt_payload` ciphertext.
///
/// Returns padded plaintext or `ValueError` for invalid lengths, key material, or message-key
/// verification; large work runs without the GIL.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach large decryption work.
/// - `auth_key`: The 256-byte MTProto authorization key.
/// - `msg_key`: The 16-byte message key to verify.
/// - `ciphertext`: AES-IGE ciphertext whose length must be an AES-block multiple.
/// - `client_to_server`: Selects the directional MTProto key schedule.
#[pyfunction]
fn mtproto_decrypt_payload(
    py: Python<'_>,
    auth_key: Vec<u8>,
    msg_key: Vec<u8>,
    ciphertext: Vec<u8>,
    client_to_server: bool,
) -> PyResult<Vec<u8>> {
    let work_bytes = auth_key.len() + msg_key.len() + ciphertext.len();
    detach_if_large(py, work_bytes, move || {
        mtproto_decrypt_payload_raw(&auth_key, &msg_key, &ciphertext, client_to_server)
    })
}

/// Returns the bytewise exclusive-or of Python `xor_bytes(left, right)` inputs.
///
/// Returns `ValueError` unless both inputs have equal length.
///
/// # Arguments
///
/// - `left`: First equal-length byte sequence.
/// - `right`: Second equal-length byte sequence.
#[pyfunction]
fn xor_bytes(left: &[u8], right: &[u8]) -> PyResult<Vec<u8>> {
    xor_bytes_raw(left, right)
}

/// Encrypts block-aligned bytes with Python `aes_256_ige_encrypt`.
///
/// Requires a 32-byte key and IV; returns `ValueError` for invalid lengths and releases the GIL
/// for large plaintexts.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach large encryption work.
/// - `plaintext`: AES-block-aligned bytes to encrypt.
/// - `key`: The 32-byte AES-256 key.
/// - `iv`: The 32-byte AES-IGE initialization vector.
#[pyfunction]
fn aes_256_ige_encrypt(
    py: Python<'_>,
    plaintext: Vec<u8>,
    key: Vec<u8>,
    iv: Vec<u8>,
) -> PyResult<Vec<u8>> {
    let work_bytes = plaintext.len();
    detach_if_large(py, work_bytes, move || {
        aes_256_ige_encrypt_raw(&plaintext, &key, &iv)
    })
}

/// Decrypts block-aligned bytes with Python `aes_256_ige_decrypt`.
///
/// Requires a 32-byte key and IV; returns `ValueError` for invalid lengths and releases the GIL
/// for large ciphertexts.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach large decryption work.
/// - `ciphertext`: AES-block-aligned bytes to decrypt.
/// - `key`: The 32-byte AES-256 key.
/// - `iv`: The 32-byte AES-IGE initialization vector.
#[pyfunction]
fn aes_256_ige_decrypt(
    py: Python<'_>,
    ciphertext: Vec<u8>,
    key: Vec<u8>,
    iv: Vec<u8>,
) -> PyResult<Vec<u8>> {
    let work_bytes = ciphertext.len();
    detach_if_large(py, work_bytes, move || {
        aes_256_ige_decrypt_raw(&ciphertext, &key, &iv)
    })
}

/// Encrypts block-aligned bytes with Python `aes_256_cbc_encrypt` without padding.
///
/// Requires 32-byte key and 16-byte IV inputs; invalid lengths become `ValueError` and large
/// plaintexts release the GIL.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach large encryption work.
/// - `plaintext`: AES-block-aligned bytes to encrypt.
/// - `key`: The 32-byte AES-256 key.
/// - `iv`: The 16-byte CBC initialization vector.
#[pyfunction]
fn aes_256_cbc_encrypt(
    py: Python<'_>,
    plaintext: Vec<u8>,
    key: Vec<u8>,
    iv: Vec<u8>,
) -> PyResult<Vec<u8>> {
    let work_bytes = plaintext.len();
    detach_if_large(py, work_bytes, move || {
        aes_256_cbc_encrypt_raw(&plaintext, &key, &iv)
    })
}

/// Decrypts block-aligned bytes with Python `aes_256_cbc_decrypt` without padding.
///
/// Requires 32-byte key and 16-byte IV inputs; invalid lengths become `ValueError` and large
/// ciphertexts release the GIL.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach large decryption work.
/// - `ciphertext`: AES-block-aligned bytes to decrypt.
/// - `key`: The 32-byte AES-256 key.
/// - `iv`: The 16-byte CBC initialization vector.
#[pyfunction]
fn aes_256_cbc_decrypt(
    py: Python<'_>,
    ciphertext: Vec<u8>,
    key: Vec<u8>,
    iv: Vec<u8>,
) -> PyResult<Vec<u8>> {
    let work_bytes = ciphertext.len();
    detach_if_large(py, work_bytes, move || {
        aes_256_cbc_decrypt_raw(&ciphertext, &key, &iv)
    })
}

/// Applies Python `aes_256_ctr_crypt` to data using AES-CTR keystream XOR.
///
/// The same routine encrypts and decrypts; it validates the 32-byte key and 16-byte counter IV,
/// and releases the GIL for large data.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach large counter-mode work.
/// - `data`: Bytes to encrypt or decrypt.
/// - `key`: The 32-byte AES-256 key.
/// - `iv`: The 16-byte initial counter block.
#[pyfunction]
fn aes_256_ctr_crypt(
    py: Python<'_>,
    data: Vec<u8>,
    key: Vec<u8>,
    iv: Vec<u8>,
) -> PyResult<Vec<u8>> {
    let work_bytes = data.len();
    detach_if_large(py, work_bytes, move || {
        aes_256_ctr_crypt_raw(&data, &key, &iv)
    })
}

/// Authenticated-encrypts Python `aes_256_gcm_encrypt` plaintext and associated data.
///
/// Returns ciphertext followed by its GCM tag, or `ValueError` for a bad 32-byte key, 12-byte
/// nonce, or encryption failure; large work releases the GIL.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach large authenticated-encryption work.
/// - `plaintext`: Bytes to encrypt.
/// - `key`: The 32-byte AES-256 key.
/// - `nonce`: The 12-byte GCM nonce.
/// - `associated_data`: Authenticated bytes that are not encrypted.
#[pyfunction]
fn aes_256_gcm_encrypt(
    py: Python<'_>,
    plaintext: Vec<u8>,
    key: Vec<u8>,
    nonce: Vec<u8>,
    associated_data: Vec<u8>,
) -> PyResult<Vec<u8>> {
    let work_bytes = plaintext.len() + associated_data.len();
    detach_if_large(py, work_bytes, move || {
        aes_256_gcm_encrypt_raw(&plaintext, &key, &nonce, &associated_data)
    })
}

/// Authenticated-decrypts Python `aes_256_gcm_decrypt` ciphertext-and-tag bytes.
///
/// Returns plaintext or `ValueError` for invalid key/nonce material or authentication failure;
/// large work releases the GIL.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach large authenticated-decryption work.
/// - `ciphertext_and_tag`: GCM ciphertext followed by its authentication tag.
/// - `key`: The 32-byte AES-256 key.
/// - `nonce`: The 12-byte GCM nonce.
/// - `associated_data`: Authenticated bytes that are not encrypted.
#[pyfunction]
fn aes_256_gcm_decrypt(
    py: Python<'_>,
    ciphertext_and_tag: Vec<u8>,
    key: Vec<u8>,
    nonce: Vec<u8>,
    associated_data: Vec<u8>,
) -> PyResult<Vec<u8>> {
    let work_bytes = ciphertext_and_tag.len() + associated_data.len();
    detach_if_large(py, work_bytes, move || {
        aes_256_gcm_decrypt_raw(&ciphertext_and_tag, &key, &nonce, &associated_data)
    })
}

/// Derives Python `scrypt_derive` bytes from password, salt, and scrypt cost parameters.
///
/// `n` must be a power of two above one and `length` is limited to 1..=1024; invalid parameters
/// return `ValueError`. Estimated memory is capped at 256 MiB and aggregate work at 1 GiB. The
/// GIL is released when the `128 * n * r * p` work estimate exceeds 4 KiB.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach only sufficiently large scrypt work.
/// - `password`: Password bytes accepted by scrypt.
/// - `salt`: Salt bytes accepted by scrypt.
/// - `n`: CPU/memory cost, required to be a power of two greater than one.
/// - `r`: scrypt block-size cost parameter.
/// - `p`: scrypt parallelization cost parameter.
/// - `length`: Requested derived-key length in the inclusive range 1..=1024.
#[pyfunction]
fn scrypt_derive(
    py: Python<'_>,
    password: Vec<u8>,
    salt: Vec<u8>,
    n: u32,
    r: u32,
    p: u32,
    length: usize,
) -> PyResult<Vec<u8>> {
    let work_bytes = usize::try_from(n)
        .unwrap_or(usize::MAX)
        .saturating_mul(r as usize)
        .saturating_mul(p as usize)
        .saturating_mul(128);
    detach_if_large(py, work_bytes, move || {
        scrypt_derive_raw(&password, &salt, n, r, p, length)
    })
}

/// Factorizes Python `pq_factorize(pq)` into ordered nontrivial `u64` factors.
///
/// Returns `ValueError` for non-composite values and runs the potentially expensive search with
/// the GIL released.
///
/// # Arguments
///
/// - `py`: The acquired GIL token used to detach the factorization search.
/// - `pq`: Composite MTProto handshake value to split into ordered factors.
#[pyfunction]
fn pq_factorize(py: Python<'_>, pq: u64) -> PyResult<(u64, u64)> {
    detach_if_large(py, 8 * 1024, move || pq_factorize_raw(pq))
}

/// Computes SHA-1 for Rust callers without Python or GIL interaction.
///
/// # Arguments
///
/// - `data`: Bytes to hash.
pub(crate) fn sha1_digest_raw(data: &[u8]) -> Vec<u8> {
    Sha1::digest(data).to_vec()
}

/// Computes SHA-256 for Rust callers without Python or GIL interaction.
///
/// # Arguments
///
/// - `data`: Bytes to hash.
pub(crate) fn sha256_digest_raw(data: &[u8]) -> Vec<u8> {
    Sha256::digest(data).to_vec()
}

/// Derives the trailing eight SHA-1 bytes that identify a validated MTProto authorization key.
///
/// Returns `ValueError` if the key is not exactly 256 bytes; does not acquire the GIL.
///
/// # Arguments
///
/// - `auth_key`: Authorization key whose SHA-1 tail supplies the identifier.
pub(crate) fn mtproto_auth_key_id_raw(auth_key: &[u8]) -> PyResult<Vec<u8>> {
    validate_auth_key(auth_key)?;
    let digest = Sha1::digest(auth_key);
    Ok(digest[12..20].to_vec())
}

/// Derives an MTProto 2.0 message key from a validated authorization key and padded plaintext.
///
/// Callers must validate the authorization-key length before use because this internal primitive
/// slices its fixed protocol ranges directly.
///
/// # Arguments
///
/// - `auth_key`: Previously validated 256-byte authorization key.
/// - `plaintext_with_padding`: Padded inner plaintext to include in the SHA-256 derivation.
/// - `client_to_server`: Selects the directional key offset.
pub(crate) fn mtproto_message_key_raw(
    auth_key: &[u8],
    plaintext_with_padding: &[u8],
    client_to_server: bool,
) -> Vec<u8> {
    let x = direction_offset(client_to_server);
    let mut hasher = Sha256::new();
    hasher.update(&auth_key[88 + x..120 + x]);
    hasher.update(plaintext_with_padding);
    let digest = hasher.finalize();
    digest[8..24].to_vec()
}

/// Derives the MTProto 2.0 AES-IGE key and IV from validated fixed-width key material.
///
/// Callers must validate `auth_key` and `msg_key` before calling; the function has no GIL use.
///
/// # Arguments
///
/// - `auth_key`: Previously validated 256-byte authorization key.
/// - `msg_key`: Previously validated 16-byte message key.
/// - `client_to_server`: Selects the directional key offset.
pub(crate) fn mtproto_derive_aes_key_iv_raw(
    auth_key: &[u8],
    msg_key: &[u8],
    client_to_server: bool,
) -> (Vec<u8>, Vec<u8>) {
    let x = direction_offset(client_to_server);
    let mut hasher_a = Sha256::new();
    hasher_a.update(msg_key);
    hasher_a.update(&auth_key[x..x + 36]);
    let sha256_a = hasher_a.finalize();

    let mut hasher_b = Sha256::new();
    hasher_b.update(&auth_key[40 + x..76 + x]);
    hasher_b.update(msg_key);
    let sha256_b = hasher_b.finalize();

    let mut aes_key = Vec::with_capacity(32);
    aes_key.extend_from_slice(&sha256_a[..8]);
    aes_key.extend_from_slice(&sha256_b[8..24]);
    aes_key.extend_from_slice(&sha256_a[24..32]);

    let mut aes_iv = Vec::with_capacity(32);
    aes_iv.extend_from_slice(&sha256_b[..8]);
    aes_iv.extend_from_slice(&sha256_a[8..24]);
    aes_iv.extend_from_slice(&sha256_b[24..32]);
    (aes_key, aes_iv)
}

/// Produces the auth-key identifier, message key, and AES-IGE ciphertext for padded plaintext.
///
/// Returns `ValueError` for malformed keys or non-block-aligned plaintext; no GIL interaction.
///
/// # Arguments
///
/// - `auth_key`: 256-byte authorization key used for id, message key, and AES derivation.
/// - `plaintext_with_padding`: AES-block-aligned inner plaintext to encrypt.
/// - `client_to_server`: Selects the directional MTProto key schedule.
pub(crate) fn mtproto_encrypt_payload_raw(
    auth_key: &[u8],
    plaintext_with_padding: &[u8],
    client_to_server: bool,
) -> PyResult<(Vec<u8>, Vec<u8>, Vec<u8>)> {
    validate_auth_key(auth_key)?;
    validate_block_multiple(plaintext_with_padding)?;
    let auth_key_id = mtproto_auth_key_id_raw(auth_key)?;
    let msg_key = mtproto_message_key_raw(auth_key, plaintext_with_padding, client_to_server);
    let (aes_key, aes_iv) = mtproto_derive_aes_key_iv_raw(auth_key, &msg_key, client_to_server);
    let ciphertext = aes_256_ige_encrypt_raw(plaintext_with_padding, &aes_key, &aes_iv)?;
    Ok((auth_key_id, msg_key, ciphertext))
}

/// Decrypts and authenticates an MTProto payload using validated directional key derivation.
///
/// Returns `ValueError` for malformed inputs or a message-key mismatch; no GIL interaction.
///
/// # Arguments
///
/// - `auth_key`: 256-byte authorization key used for directional AES derivation.
/// - `msg_key`: 16-byte message key expected after decryption.
/// - `ciphertext`: AES-block-aligned encrypted payload.
/// - `client_to_server`: Selects the directional MTProto key schedule.
pub(crate) fn mtproto_decrypt_payload_raw(
    auth_key: &[u8],
    msg_key: &[u8],
    ciphertext: &[u8],
    client_to_server: bool,
) -> PyResult<Vec<u8>> {
    validate_auth_key(auth_key)?;
    validate_msg_key(msg_key)?;
    validate_block_multiple(ciphertext)?;
    let (aes_key, aes_iv) = mtproto_derive_aes_key_iv_raw(auth_key, msg_key, client_to_server);
    let plaintext_with_padding = aes_256_ige_decrypt_raw(ciphertext, &aes_key, &aes_iv)?;
    let expected_msg_key =
        mtproto_message_key_raw(auth_key, &plaintext_with_padding, client_to_server);
    if expected_msg_key.as_slice().ct_eq(msg_key).unwrap_u8() != 1 {
        return Err(PyValueError::new_err("MTProto msg_key verification failed"));
    }
    Ok(plaintext_with_padding)
}

/// Computes bytewise XOR for equal-length Rust byte slices.
///
/// Returns `ValueError` for unequal lengths and does not use the GIL.
///
/// # Arguments
///
/// - `left`: First equal-length byte slice.
/// - `right`: Second equal-length byte slice.
pub(crate) fn xor_bytes_raw(left: &[u8], right: &[u8]) -> PyResult<Vec<u8>> {
    if left.len() != right.len() {
        return Err(PyValueError::new_err(
            "xor inputs must have the same length",
        ));
    }
    Ok(left.iter().zip(right.iter()).map(|(a, b)| a ^ b).collect())
}

/// Encrypts a block-aligned byte slice using AES-256 IGE for Rust callers.
///
/// Returns `ValueError` unless the key, IV, and plaintext lengths meet AES-IGE requirements.
///
/// # Arguments
///
/// - `plaintext`: AES-block-aligned bytes to encrypt.
/// - `key`: The 32-byte AES-256 key.
/// - `iv`: The 32-byte AES-IGE initialization vector.
pub(crate) fn aes_256_ige_encrypt_raw(
    plaintext: &[u8],
    key: &[u8],
    iv: &[u8],
) -> PyResult<Vec<u8>> {
    validate_aes_key(key)?;
    validate_ige_iv(iv)?;
    validate_block_multiple(plaintext)?;
    let cipher = Aes256::new_from_slice(key)
        .map_err(|_| PyValueError::new_err("AES-256 key must be 32 bytes"))?;
    let mut previous_cipher: [u8; AES_BLOCK_SIZE] = iv[..AES_BLOCK_SIZE]
        .try_into()
        .expect("validated IV length");
    let mut previous_plain: [u8; AES_BLOCK_SIZE] = iv[AES_BLOCK_SIZE..]
        .try_into()
        .expect("validated IV length");
    let mut output = Vec::with_capacity(plaintext.len());
    for block in plaintext.chunks_exact(AES_BLOCK_SIZE) {
        let plain_block: [u8; AES_BLOCK_SIZE] = block.try_into().expect("chunk size is 16");
        let mut mixed = xor_block(&plain_block, &previous_cipher);
        cipher.encrypt_block((&mut mixed).into());
        let cipher_block = xor_block(&mixed, &previous_plain);
        output.extend_from_slice(&cipher_block);
        previous_cipher = cipher_block;
        previous_plain = plain_block;
    }
    Ok(output)
}

/// Decrypts a block-aligned AES-256 IGE ciphertext for Rust callers.
///
/// Returns `ValueError` unless the key, IV, and ciphertext lengths meet AES-IGE requirements.
///
/// # Arguments
///
/// - `ciphertext`: AES-block-aligned bytes to decrypt.
/// - `key`: The 32-byte AES-256 key.
/// - `iv`: The 32-byte AES-IGE initialization vector.
pub(crate) fn aes_256_ige_decrypt_raw(
    ciphertext: &[u8],
    key: &[u8],
    iv: &[u8],
) -> PyResult<Vec<u8>> {
    validate_aes_key(key)?;
    validate_ige_iv(iv)?;
    validate_block_multiple(ciphertext)?;
    let cipher = Aes256::new_from_slice(key)
        .map_err(|_| PyValueError::new_err("AES-256 key must be 32 bytes"))?;
    let mut previous_cipher: [u8; AES_BLOCK_SIZE] = iv[..AES_BLOCK_SIZE]
        .try_into()
        .expect("validated IV length");
    let mut previous_plain: [u8; AES_BLOCK_SIZE] = iv[AES_BLOCK_SIZE..]
        .try_into()
        .expect("validated IV length");
    let mut output = Vec::with_capacity(ciphertext.len());
    for block in ciphertext.chunks_exact(AES_BLOCK_SIZE) {
        let cipher_block: [u8; AES_BLOCK_SIZE] = block.try_into().expect("chunk size is 16");
        let mut mixed = xor_block(&cipher_block, &previous_plain);
        cipher.decrypt_block((&mut mixed).into());
        let plain_block = xor_block(&mixed, &previous_cipher);
        output.extend_from_slice(&plain_block);
        previous_cipher = cipher_block;
        previous_plain = plain_block;
    }
    Ok(output)
}

/// Encrypts a block-aligned byte slice with unpadded AES-256 CBC.
///
/// Returns `ValueError` unless the key, IV, and plaintext lengths are valid.
///
/// # Arguments
///
/// - `plaintext`: AES-block-aligned bytes to encrypt.
/// - `key`: The 32-byte AES-256 key.
/// - `iv`: The 16-byte CBC initialization vector.
pub(crate) fn aes_256_cbc_encrypt_raw(
    plaintext: &[u8],
    key: &[u8],
    iv: &[u8],
) -> PyResult<Vec<u8>> {
    validate_aes_key(key)?;
    validate_cbc_ctr_iv(iv)?;
    validate_block_multiple(plaintext)?;
    let cipher = Aes256::new_from_slice(key)
        .map_err(|_| PyValueError::new_err("AES-256 key must be 32 bytes"))?;
    let mut previous: [u8; AES_BLOCK_SIZE] = iv.try_into().expect("validated IV length");
    let mut output = Vec::with_capacity(plaintext.len());
    for block in plaintext.chunks_exact(AES_BLOCK_SIZE) {
        let plain_block: [u8; AES_BLOCK_SIZE] = block.try_into().expect("chunk size is 16");
        let mut cipher_block = xor_block(&plain_block, &previous);
        cipher.encrypt_block((&mut cipher_block).into());
        output.extend_from_slice(&cipher_block);
        previous = cipher_block;
    }
    Ok(output)
}

/// Decrypts a block-aligned unpadded AES-256 CBC ciphertext.
///
/// Returns `ValueError` unless the key, IV, and ciphertext lengths are valid.
///
/// # Arguments
///
/// - `ciphertext`: AES-block-aligned bytes to decrypt.
/// - `key`: The 32-byte AES-256 key.
/// - `iv`: The 16-byte CBC initialization vector.
pub(crate) fn aes_256_cbc_decrypt_raw(
    ciphertext: &[u8],
    key: &[u8],
    iv: &[u8],
) -> PyResult<Vec<u8>> {
    validate_aes_key(key)?;
    validate_cbc_ctr_iv(iv)?;
    validate_block_multiple(ciphertext)?;
    let cipher = Aes256::new_from_slice(key)
        .map_err(|_| PyValueError::new_err("AES-256 key must be 32 bytes"))?;
    let mut previous: [u8; AES_BLOCK_SIZE] = iv.try_into().expect("validated IV length");
    let mut output = Vec::with_capacity(ciphertext.len());
    for block in ciphertext.chunks_exact(AES_BLOCK_SIZE) {
        let cipher_block: [u8; AES_BLOCK_SIZE] = block.try_into().expect("chunk size is 16");
        let mut plain_block = cipher_block;
        cipher.decrypt_block((&mut plain_block).into());
        plain_block = xor_block(&plain_block, &previous);
        output.extend_from_slice(&plain_block);
        previous = cipher_block;
    }
    Ok(output)
}

/// XORs bytes with an AES-256 CTR keystream; the same operation encrypts and decrypts.
///
/// Returns `ValueError` unless `key` is 32 bytes and `iv` is one AES block.
///
/// # Arguments
///
/// - `data`: Bytes to XOR with the generated CTR keystream.
/// - `key`: The 32-byte AES-256 key.
/// - `iv`: The 16-byte initial counter block.
pub(crate) fn aes_256_ctr_crypt_raw(data: &[u8], key: &[u8], iv: &[u8]) -> PyResult<Vec<u8>> {
    validate_aes_key(key)?;
    validate_cbc_ctr_iv(iv)?;
    let cipher = Aes256::new_from_slice(key)
        .map_err(|_| PyValueError::new_err("AES-256 key must be 32 bytes"))?;
    let mut counter: [u8; AES_BLOCK_SIZE] = iv.try_into().expect("validated IV length");
    let mut output = Vec::with_capacity(data.len());
    for block in data.chunks(AES_BLOCK_SIZE) {
        let mut stream_block = counter;
        cipher.encrypt_block((&mut stream_block).into());
        output.extend(block.iter().zip(stream_block.iter()).map(|(a, b)| a ^ b));
        increment_counter(&mut counter);
    }
    Ok(output)
}

/// Authenticated-encrypts plaintext with AES-256 GCM and returns ciphertext plus tag.
///
/// Returns `ValueError` for an invalid key or nonce or if the cipher rejects the operation.
///
/// # Arguments
///
/// - `plaintext`: Bytes to encrypt.
/// - `key`: The 32-byte AES-256 key.
/// - `nonce`: The 12-byte GCM nonce.
/// - `associated_data`: Authenticated bytes that are not encrypted.
pub(crate) fn aes_256_gcm_encrypt_raw(
    plaintext: &[u8],
    key: &[u8],
    nonce: &[u8],
    associated_data: &[u8],
) -> PyResult<Vec<u8>> {
    validate_aes_key(key)?;
    validate_gcm_nonce(nonce)?;
    let cipher = Aes256Gcm::new_from_slice(key)
        .map_err(|_| PyValueError::new_err("AES-256 key must be 32 bytes"))?;
    let nonce = Nonce::<U12>::try_from(nonce)
        .map_err(|_| PyValueError::new_err("AES-GCM nonce must be 12 bytes"))?;
    cipher
        .encrypt(
            &nonce,
            Payload {
                msg: plaintext,
                aad: associated_data,
            },
        )
        .map_err(|_| PyValueError::new_err("AES-GCM encryption failed"))
}

/// Authenticated-decrypts AES-256 GCM ciphertext-and-tag data.
///
/// Returns `ValueError` for invalid key/nonce material or a failed authentication check.
///
/// # Arguments
///
/// - `ciphertext_and_tag`: GCM ciphertext followed by its authentication tag.
/// - `key`: The 32-byte AES-256 key.
/// - `nonce`: The 12-byte GCM nonce.
/// - `associated_data`: Authenticated bytes that are not encrypted.
pub(crate) fn aes_256_gcm_decrypt_raw(
    ciphertext_and_tag: &[u8],
    key: &[u8],
    nonce: &[u8],
    associated_data: &[u8],
) -> PyResult<Vec<u8>> {
    validate_aes_key(key)?;
    validate_gcm_nonce(nonce)?;
    let cipher = Aes256Gcm::new_from_slice(key)
        .map_err(|_| PyValueError::new_err("AES-256 key must be 32 bytes"))?;
    let nonce = Nonce::<U12>::try_from(nonce)
        .map_err(|_| PyValueError::new_err("AES-GCM nonce must be 12 bytes"))?;
    cipher
        .decrypt(
            &nonce,
            Payload {
                msg: ciphertext_and_tag,
                aad: associated_data,
            },
        )
        .map_err(|_| PyValueError::new_err("AES-GCM authentication failed"))
}

/// Runs scrypt with validated protocol-level output limits for Rust callers.
///
/// Returns `ValueError` for invalid cost parameters, an unsupported output length, or derivation
/// failure.  This is a synchronous, GIL-free primitive.
///
/// # Arguments
///
/// - `password`: Password bytes accepted by scrypt.
/// - `salt`: Salt bytes accepted by scrypt.
/// - `n`: CPU/memory cost, required to be a power of two greater than one.
/// - `r`: scrypt block-size cost parameter.
/// - `p`: scrypt parallelization cost parameter.
/// - `length`: Requested derived-key length in the inclusive range 1..=1024.
pub(crate) fn scrypt_derive_raw(
    password: &[u8],
    salt: &[u8],
    n: u32,
    r: u32,
    p: u32,
    length: usize,
) -> PyResult<Vec<u8>> {
    if n < 2 || !n.is_power_of_two() {
        return Err(PyValueError::new_err(
            "scrypt n must be a power of two greater than one",
        ));
    }
    if length == 0 || length > 1024 {
        return Err(PyValueError::new_err(
            "scrypt output length must be between 1 and 1024 bytes",
        ));
    }
    let memory_bytes = usize::try_from(n)
        .unwrap_or(usize::MAX)
        .saturating_mul(r as usize)
        .saturating_mul(128);
    let work_bytes = memory_bytes.saturating_mul(p as usize);
    if memory_bytes > SCRYPT_MAX_MEMORY_BYTES || work_bytes > SCRYPT_MAX_WORK_BYTES {
        return Err(PyValueError::new_err(
            "scrypt parameters exceed the resource limit",
        ));
    }
    let log_n = u8::try_from(n.trailing_zeros())
        .map_err(|_| PyValueError::new_err("scrypt n is too large"))?;
    let params = ScryptParams::new(log_n, r, p)
        .map_err(|_| PyValueError::new_err("invalid scrypt parameters"))?;
    let mut output = vec![0_u8; length];
    scrypt(password, salt, &params, &mut output)
        .map_err(|_| PyValueError::new_err("scrypt derivation failed"))?;
    Ok(output)
}

/// Finds and orders the two nontrivial factors of an MTProto `pq` value.
///
/// Returns `ValueError` for values below four or values that are not composite.
///
/// # Arguments
///
/// - `pq`: Candidate composite integer to split into its two ordered factors.
fn pq_factorize_raw(pq: u64) -> PyResult<(u64, u64)> {
    if pq < 4 {
        return Err(PyValueError::new_err("pq must be a composite integer >= 4"));
    }
    let factor = factor_u64(pq);
    if factor == 1 || factor == pq {
        return Err(PyValueError::new_err("pq must be composite"));
    }
    let other = pq / factor;
    Ok(if factor <= other {
        (factor, other)
    } else {
        (other, factor)
    })
}

/// Validates the fixed 256-byte MTProto authorization-key width.
///
/// Returns `ValueError` rather than allowing fixed-offset protocol code to panic.
///
/// # Arguments
///
/// - `auth_key`: Candidate authorization key expected to contain 256 bytes.
pub(crate) fn validate_auth_key(auth_key: &[u8]) -> PyResult<()> {
    if auth_key.len() != MT_PROTO_AUTH_KEY_SIZE {
        return Err(PyValueError::new_err("MTProto auth_key must be 256 bytes"));
    }
    Ok(())
}

/// Validates the fixed 16-byte MTProto message-key width.
///
/// Returns `ValueError` on a malformed input slice.
///
/// # Arguments
///
/// - `msg_key`: Candidate message key expected to contain 16 bytes.
pub(crate) fn validate_msg_key(msg_key: &[u8]) -> PyResult<()> {
    if msg_key.len() != MT_PROTO_MSG_KEY_SIZE {
        return Err(PyValueError::new_err("MTProto msg_key must be 16 bytes"));
    }
    Ok(())
}

/// Validates that AES block-mode input has a whole-number count of AES blocks.
///
/// Returns `ValueError` when the byte length is not divisible by 16.
///
/// # Arguments
///
/// - `data`: Candidate AES block-mode input.
pub(crate) fn validate_block_multiple(data: &[u8]) -> PyResult<()> {
    if !data.len().is_multiple_of(AES_BLOCK_SIZE) {
        return Err(PyValueError::new_err(
            "AES block mode input length must be a multiple of 16 bytes",
        ));
    }
    Ok(())
}

/// Validates a 32-byte AES-256 key and returns `ValueError` otherwise.
///
/// # Arguments
///
/// - `key`: Candidate AES-256 key.
fn validate_aes_key(key: &[u8]) -> PyResult<()> {
    if key.len() != 32 {
        return Err(PyValueError::new_err("AES-256 key must be 32 bytes"));
    }
    Ok(())
}

/// Validates the two-block, 32-byte IV required by AES-IGE.
///
/// # Arguments
///
/// - `iv`: Candidate AES-IGE initialization vector.
fn validate_ige_iv(iv: &[u8]) -> PyResult<()> {
    if iv.len() != 32 {
        return Err(PyValueError::new_err("AES-IGE IV must be 32 bytes"));
    }
    Ok(())
}

/// Validates the one-block IV or counter used by CBC and CTR modes.
///
/// # Arguments
///
/// - `iv`: Candidate CBC initialization vector or CTR counter block.
fn validate_cbc_ctr_iv(iv: &[u8]) -> PyResult<()> {
    if iv.len() != AES_BLOCK_SIZE {
        return Err(PyValueError::new_err("AES IV must be 16 bytes"));
    }
    Ok(())
}

/// Validates the 12-byte nonce mandated by this AES-GCM interface.
///
/// # Arguments
///
/// - `nonce`: Candidate AES-GCM nonce.
fn validate_gcm_nonce(nonce: &[u8]) -> PyResult<()> {
    if nonce.len() != 12 {
        return Err(PyValueError::new_err("AES-GCM nonce must be 12 bytes"));
    }
    Ok(())
}

/// Returns the MTProto key-schedule offset for the requested packet direction.
///
/// # Arguments
///
/// - `client_to_server`: Whether the packet travels from client to server.
fn direction_offset(client_to_server: bool) -> usize {
    if client_to_server { 0 } else { 8 }
}

/// Computes a fixed-width XOR block used by the AES block-mode loops.
///
/// # Arguments
///
/// - `left`: First AES-sized block.
/// - `right`: Second AES-sized block.
fn xor_block(left: &[u8; AES_BLOCK_SIZE], right: &[u8; AES_BLOCK_SIZE]) -> [u8; AES_BLOCK_SIZE] {
    let mut output = [0_u8; AES_BLOCK_SIZE];
    for index in 0..AES_BLOCK_SIZE {
        output[index] = left[index] ^ right[index];
    }
    output
}

/// Advances a big-endian AES-CTR counter in place, wrapping at the full block width.
///
/// # Arguments
///
/// - `counter`: Mutable AES-sized counter block to increment.
fn increment_counter(counter: &mut [u8; AES_BLOCK_SIZE]) {
    for byte in counter.iter_mut().rev() {
        let (next, carry) = byte.overflowing_add(1);
        *byte = next;
        if !carry {
            break;
        }
    }
}

/// Computes the greatest common divisor used by Pollard-rho factorization.
///
/// # Arguments
///
/// - `left`: First nonnegative integer.
/// - `right`: Second nonnegative integer.
fn gcd(mut left: u64, mut right: u64) -> u64 {
    while right != 0 {
        let remainder = left % right;
        left = right;
        right = remainder;
    }
    left
}

/// Multiplies modulo `modulus` with a widened intermediate to avoid `u64` overflow.
///
/// # Panics
///
/// Panics if `modulus` is zero because the remainder operation is undefined. Callers must also
/// pass a nonzero modulus; `u128` widening prevents multiplication overflow for all `u64` inputs.
///
/// # Arguments
///
/// - `left`: First modular multiplicand.
/// - `right`: Second modular multiplicand.
/// - `modulus`: Nonzero modulus used for the reduced product.
fn mul_mod(left: u64, right: u64, modulus: u64) -> u64 {
    (((left as u128) * (right as u128)) % (modulus as u128)) as u64
}

/// Computes modular exponentiation for deterministic Miller-Rabin witnesses.
///
/// # Panics
///
/// Panics if `modulus` is zero because both reduction paths use remainder operations. Arithmetic
/// overflow is avoided by delegating products to `mul_mod` with its widened intermediate.
///
/// # Arguments
///
/// - `base`: Base to exponentiate modulo `modulus`.
/// - `exponent`: Nonnegative exponent encoded as `u64`.
/// - `modulus`: Nonzero modulus used for every reduction.
fn pow_mod(mut base: u64, mut exponent: u64, modulus: u64) -> u64 {
    let mut result = 1_u64;
    while exponent > 0 {
        if exponent & 1 == 1 {
            result = mul_mod(result, base, modulus);
        }
        base = mul_mod(base, base, modulus);
        exponent >>= 1;
    }
    result
}

/// Deterministically tests whether a `u64` is prime using fixed Miller-Rabin witnesses.
///
/// # Arguments
///
/// - `value`: Unsigned integer to classify as prime or composite.
fn is_prime_u64(value: u64) -> bool {
    if value < 2 {
        return false;
    }
    for small in [2_u64, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37] {
        if value == small {
            return true;
        }
        if value.is_multiple_of(small) {
            return false;
        }
    }
    let mut d = value - 1;
    let mut s = 0_u32;
    while d.is_multiple_of(2) {
        d /= 2;
        s += 1;
    }
    for base in [2_u64, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37] {
        if base >= value {
            continue;
        }
        let mut x = pow_mod(base, d, value);
        if x == 1 || x == value - 1 {
            continue;
        }
        let mut witnessed = false;
        for _ in 1..s {
            x = mul_mod(x, x, value);
            if x == value - 1 {
                witnessed = true;
                break;
            }
        }
        if !witnessed {
            return false;
        }
    }
    true
}

/// Returns one factor of a composite `u64` using trial division and Pollard-rho iteration.
///
/// # Arguments
///
/// - `value`: Composite unsigned integer whose nontrivial factor is requested.
fn factor_u64(value: u64) -> u64 {
    if value.is_multiple_of(2) {
        return 2;
    }
    if is_prime_u64(value) {
        return value;
    }
    let mut c = 1_u64;
    loop {
        let mut x = 2_u64;
        let mut y = 2_u64;
        let mut d = 1_u64;
        let step = |input: u64, constant: u64| -> u64 {
            (mul_mod(input, input, value) + constant) % value
        };
        for _ in 0..100_000 {
            x = step(x, c);
            y = step(step(y, c), c);
            d = gcd(x.abs_diff(y), value);
            if d > 1 {
                break;
            }
        }
        if d > 1 && d < value {
            return d;
        }
        c = c.wrapping_add(1);
    }
}

/// Unit tests for native crypto primitives and stable interoperability vectors.
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    /// Locks down SHA and MTProto authorization-key identifier test vectors.
    fn sha_and_auth_key_outputs_are_stable() {
        assert_eq!(
            sha1_digest_raw(b"abc"),
            vec![
                0xa9, 0x99, 0x3e, 0x36, 0x47, 0x06, 0x81, 0x6a, 0xba, 0x3e, 0x25, 0x71, 0x78, 0x50,
                0xc2, 0x6c, 0x9c, 0xd0, 0xd8, 0x9d,
            ]
        );
        assert_eq!(
            sha256_digest_raw(b"abc"),
            vec![
                0xba, 0x78, 0x16, 0xbf, 0x8f, 0x01, 0xcf, 0xea, 0x41, 0x41, 0x40, 0xde, 0x5d, 0xae,
                0x22, 0x23, 0xb0, 0x03, 0x61, 0xa3, 0x96, 0x17, 0x7a, 0x9c, 0xb4, 0x10, 0xff, 0x61,
                0xf2, 0x00, 0x15, 0xad,
            ]
        );
        assert_eq!(
            mtproto_auth_key_id_raw(&auth_key()).unwrap(),
            vec![0x32, 0xd1, 0x58, 0x6e, 0xa4, 0x57, 0xdf, 0xc8]
        );
    }

    #[test]
    /// Verifies AES-IGE round-trips a block-aligned fixture.
    fn aes_ige_roundtrips() {
        let plaintext = bytes_mod(64, 1);
        let key = bytes_mod(32, 2);
        let iv = bytes_mod(32, 3);
        let ciphertext = aes_256_ige_encrypt_raw(&plaintext, &key, &iv).unwrap();
        assert_ne!(ciphertext, plaintext);
        assert_eq!(
            aes_256_ige_decrypt_raw(&ciphertext, &key, &iv).unwrap(),
            plaintext
        );
    }

    #[test]
    /// Verifies that applying AES-CTR twice with the same counter restores the input.
    fn aes_ctr_is_symmetric() {
        let plaintext = bytes_mod(65, 4);
        let key = bytes_mod(32, 5);
        let iv = bytes_mod(16, 6);
        let ciphertext = aes_256_ctr_crypt_raw(&plaintext, &key, &iv).unwrap();
        assert_ne!(ciphertext, plaintext);
        assert_eq!(
            aes_256_ctr_crypt_raw(&ciphertext, &key, &iv).unwrap(),
            plaintext
        );
    }

    #[test]
    /// Locks down AES-GCM and scrypt interoperability vectors.
    fn aes_gcm_and_scrypt_match_stable_vectors() {
        let key = scrypt_derive_raw(b"password", b"NaCl", 16_384, 8, 1, 32).unwrap();
        assert_eq!(
            hex(&key),
            "a8430d7e581f9ca03c952df506ac66c757899d67a21d71c0f1900bd778ac1d14"
        );
        let nonce = [7_u8; 12];
        let encrypted = aes_256_gcm_encrypt_raw(b"payload", &key, &nonce, b"header").unwrap();
        assert_eq!(
            aes_256_gcm_decrypt_raw(&encrypted, &key, &nonce, b"header").unwrap(),
            b"payload"
        );
        assert!(aes_256_gcm_decrypt_raw(&encrypted, &key, &nonce, b"wrong").is_err());
    }

    #[test]
    /// Rejects hostile scrypt work factors before allocating or deriving.
    fn scrypt_rejects_excessive_resource_parameters() {
        Python::initialize();
        let error = scrypt_derive_raw(b"password", b"salt", 1 << 20, 8, 16, 32).unwrap_err();
        assert!(error.to_string().contains("resource limit"));
    }

    #[test]
    /// Verifies native MTProto payload encryption and verified decryption round-trip.
    fn mtproto_payload_encrypt_decrypt_roundtrips() {
        let auth_key = auth_key();
        let plaintext = vec![0x58; 64];
        let (auth_key_id, msg_key, ciphertext) =
            mtproto_encrypt_payload_raw(&auth_key, &plaintext, true).unwrap();
        assert_eq!(auth_key_id, mtproto_auth_key_id_raw(&auth_key).unwrap());
        assert_eq!(
            mtproto_decrypt_payload_raw(&auth_key, &msg_key, &ciphertext, true).unwrap(),
            plaintext
        );
    }

    #[test]
    /// Covers XOR validation and `pq` factorization helpers.
    fn xor_and_pq_helpers_work() {
        assert_eq!(
            xor_bytes_raw(&[0x0f, 0xf0], &[0xf0, 0x0f]).unwrap(),
            vec![0xff, 0xff]
        );
        assert_eq!(
            pq_factorize_raw(1_000_003 * 1_000_033).unwrap(),
            (1_000_003, 1_000_033)
        );
    }

    /// Returns the deterministic 256-byte authorization-key fixture.
    fn auth_key() -> Vec<u8> {
        (0..=255).collect()
    }

    /// Builds a deterministic byte fixture with modular progression.
    ///
    /// # Arguments
    ///
    /// - `len`: Number of fixture bytes to produce.
    /// - `multiplier`: Per-index multiplier before truncation to a byte.
    fn bytes_mod(len: usize, multiplier: u8) -> Vec<u8> {
        (0..len)
            .map(|index| (index as u8).wrapping_mul(multiplier))
            .collect()
    }

    /// Formats fixture bytes as lowercase hexadecimal for stable-vector assertions.
    ///
    /// # Arguments
    ///
    /// - `value`: Fixture bytes to render.
    fn hex(value: &[u8]) -> String {
        value.iter().map(|byte| format!("{byte:02x}")).collect()
    }
}
