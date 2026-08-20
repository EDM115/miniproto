---
title: "miniproto_native::crypto"
description: "Registers cryptographic Python callables."
generated: true
editUrl: false
language: "rust"
kind: "module"
qualified_name: "miniproto_native::crypto"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L1"
crate: "miniproto_native"
python_visible: false
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `crate`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L1)
- Python exposure: Not evidenced by static PyO3 attributes.

## Documented items

- [`miniproto_native::crypto::aes_256_gcm_encrypt`](./aes-256-gcm-encrypt/)
- [`miniproto_native::crypto::aes_256_gcm_decrypt`](./aes-256-gcm-decrypt/)
- [`miniproto_native::crypto::scrypt_derive`](./scrypt-derive/)
- [`miniproto_native::crypto::pq_factorize`](./pq-factorize/)
- [`miniproto_native::crypto::register`](./register/)
- [`miniproto_native::crypto::native_available`](./native-available/)
- [`miniproto_native::crypto::sha1_digest`](./sha1-digest/)
- [`miniproto_native::crypto::sha256_digest`](./sha256-digest/)
- [`miniproto_native::crypto::mtproto_auth_key_id`](./mtproto-auth-key-id/)
- [`miniproto_native::crypto::mtproto_message_key`](./mtproto-message-key/)
- [`miniproto_native::crypto::mtproto_derive_aes_key_iv`](./mtproto-derive-aes-key-iv/)
- [`miniproto_native::crypto::mtproto_encrypt_payload`](./mtproto-encrypt-payload/)
- [`miniproto_native::crypto::mtproto_decrypt_payload`](./mtproto-decrypt-payload/)
- [`miniproto_native::crypto::xor_bytes`](./xor-bytes/)
- [`miniproto_native::crypto::aes_256_ige_encrypt`](./aes-256-ige-encrypt/)
- [`miniproto_native::crypto::aes_256_ige_decrypt`](./aes-256-ige-decrypt/)
- [`miniproto_native::crypto::aes_256_cbc_encrypt`](./aes-256-cbc-encrypt/)
- [`miniproto_native::crypto::aes_256_cbc_decrypt`](./aes-256-cbc-decrypt/)
- [`miniproto_native::crypto::aes_256_ctr_crypt`](./aes-256-ctr-crypt/)

## cargo-docs-md rendering

*miniproto_native / [crypto](index.md)*

---

# Module `crypto`

Registers cryptographic Python callables.
Native cryptographic primitives used by MTProto and its Python fallback-compatible API.

Each `#[pyfunction]` is exported under its Rust name in `miniproto._native`.  Byte-heavy
wrappers conditionally release the GIL, while `*_raw` functions are Rust-only building blocks
that never require it. PyO3 rejects incompatible Python argument conversion first, preserving
its `TypeError`, `OverflowError`, or source exception; algorithm and byte-shape validation in
this module intentionally return Python `ValueError`. No caller-facing unsafe API is exposed.

## Contents

- [Functions](#functions)
  - [`detach_if_large`](#detach-if-large)
  - [`register`](#register)
  - [`native_available`](#native-available)
  - [`__pyfunction_native_available`](#pyfunction-native-available)
  - [`sha1_digest`](#sha1-digest)
  - [`__pyfunction_sha1_digest`](#pyfunction-sha1-digest)
  - [`sha256_digest`](#sha256-digest)
  - [`__pyfunction_sha256_digest`](#pyfunction-sha256-digest)
  - [`mtproto_auth_key_id`](#mtproto-auth-key-id)
  - [`__pyfunction_mtproto_auth_key_id`](#pyfunction-mtproto-auth-key-id)
  - [`mtproto_message_key`](#mtproto-message-key)
  - [`__pyfunction_mtproto_message_key`](#pyfunction-mtproto-message-key)
  - [`mtproto_derive_aes_key_iv`](#mtproto-derive-aes-key-iv)
  - [`__pyfunction_mtproto_derive_aes_key_iv`](#pyfunction-mtproto-derive-aes-key-iv)
  - [`mtproto_encrypt_payload`](#mtproto-encrypt-payload)
  - [`__pyfunction_mtproto_encrypt_payload`](#pyfunction-mtproto-encrypt-payload)
  - [`mtproto_decrypt_payload`](#mtproto-decrypt-payload)
  - [`__pyfunction_mtproto_decrypt_payload`](#pyfunction-mtproto-decrypt-payload)
  - [`xor_bytes`](#xor-bytes)
  - [`__pyfunction_xor_bytes`](#pyfunction-xor-bytes)
  - [`aes_256_ige_encrypt`](#aes-256-ige-encrypt)
  - [`__pyfunction_aes_256_ige_encrypt`](#pyfunction-aes-256-ige-encrypt)
  - [`aes_256_ige_decrypt`](#aes-256-ige-decrypt)
  - [`__pyfunction_aes_256_ige_decrypt`](#pyfunction-aes-256-ige-decrypt)
  - [`aes_256_cbc_encrypt`](#aes-256-cbc-encrypt)
  - [`__pyfunction_aes_256_cbc_encrypt`](#pyfunction-aes-256-cbc-encrypt)
  - [`aes_256_cbc_decrypt`](#aes-256-cbc-decrypt)
  - [`__pyfunction_aes_256_cbc_decrypt`](#pyfunction-aes-256-cbc-decrypt)
  - [`aes_256_ctr_crypt`](#aes-256-ctr-crypt)
  - [`__pyfunction_aes_256_ctr_crypt`](#pyfunction-aes-256-ctr-crypt)
  - [`aes_256_gcm_encrypt`](#aes-256-gcm-encrypt)
  - [`__pyfunction_aes_256_gcm_encrypt`](#pyfunction-aes-256-gcm-encrypt)
  - [`aes_256_gcm_decrypt`](#aes-256-gcm-decrypt)
  - [`__pyfunction_aes_256_gcm_decrypt`](#pyfunction-aes-256-gcm-decrypt)
  - [`scrypt_derive`](#scrypt-derive)
  - [`__pyfunction_scrypt_derive`](#pyfunction-scrypt-derive)
  - [`pq_factorize`](#pq-factorize)
  - [`__pyfunction_pq_factorize`](#pyfunction-pq-factorize)
  - [`sha1_digest_raw`](#sha1-digest-raw)
  - [`sha256_digest_raw`](#sha256-digest-raw)
  - [`mtproto_auth_key_id_raw`](#mtproto-auth-key-id-raw)
  - [`mtproto_message_key_raw`](#mtproto-message-key-raw)
  - [`mtproto_derive_aes_key_iv_raw`](#mtproto-derive-aes-key-iv-raw)
  - [`mtproto_encrypt_payload_raw`](#mtproto-encrypt-payload-raw)
  - [`mtproto_decrypt_payload_raw`](#mtproto-decrypt-payload-raw)
  - [`xor_bytes_raw`](#xor-bytes-raw)
  - [`aes_256_ige_encrypt_raw`](#aes-256-ige-encrypt-raw)
  - [`aes_256_ige_decrypt_raw`](#aes-256-ige-decrypt-raw)
  - [`aes_256_cbc_encrypt_raw`](#aes-256-cbc-encrypt-raw)
  - [`aes_256_cbc_decrypt_raw`](#aes-256-cbc-decrypt-raw)
  - [`aes_256_ctr_crypt_raw`](#aes-256-ctr-crypt-raw)
  - [`aes_256_gcm_encrypt_raw`](#aes-256-gcm-encrypt-raw)
  - [`aes_256_gcm_decrypt_raw`](#aes-256-gcm-decrypt-raw)
  - [`scrypt_derive_raw`](#scrypt-derive-raw)
  - [`pq_factorize_raw`](#pq-factorize-raw)
  - [`validate_auth_key`](#validate-auth-key)
  - [`validate_msg_key`](#validate-msg-key)
  - [`validate_block_multiple`](#validate-block-multiple)
  - [`validate_aes_key`](#validate-aes-key)
  - [`validate_ige_iv`](#validate-ige-iv)
  - [`validate_cbc_ctr_iv`](#validate-cbc-ctr-iv)
  - [`validate_gcm_nonce`](#validate-gcm-nonce)
  - [`direction_offset`](#direction-offset)
  - [`xor_block`](#xor-block)
  - [`increment_counter`](#increment-counter)
  - [`gcd`](#gcd)
  - [`mul_mod`](#mul-mod)
  - [`pow_mod`](#pow-mod)
  - [`is_prime_u64`](#is-prime-u64)
  - [`factor_u64`](#factor-u64)
- [Constants](#constants)
  - [`AES_BLOCK_SIZE`](#aes-block-size)
  - [`MT_PROTO_AUTH_KEY_SIZE`](#mt-proto-auth-key-size)
  - [`MT_PROTO_MSG_KEY_SIZE`](#mt-proto-msg-key-size)
  - [`GIL_RELEASE_THRESHOLD_BYTES`](#gil-release-threshold-bytes)
  - [`SCRYPT_MAX_MEMORY_BYTES`](#scrypt-max-memory-bytes)
  - [`SCRYPT_MAX_WORK_BYTES`](#scrypt-max-work-bytes)

## Quick Reference

| Item | Kind | Description |
|------|------|-------------|
| [`detach_if_large`](#detach-if-large) | fn | Runs `f` without the GIL when its input work estimate exceeds the native threshold. |
| [`register`](#register) | fn | Registers this module's fallback-compatible Python callables on `miniproto._native`. |
| [`native_available`](#native-available) | fn | Implements Python `native_available`, which always returns `true` while this compiled callable is importable. |
| [`__pyfunction_native_available`](#pyfunction-native-available) | fn |  |
| [`sha1_digest`](#sha1-digest) | fn | Computes Python `sha1_digest(data)` and returns the 20-byte SHA-1 digest. |
| [`__pyfunction_sha1_digest`](#pyfunction-sha1-digest) | fn |  |
| [`sha256_digest`](#sha256-digest) | fn | Computes Python `sha256_digest(data)` and returns the 32-byte SHA-256 digest. |
| [`__pyfunction_sha256_digest`](#pyfunction-sha256-digest) | fn |  |
| [`mtproto_auth_key_id`](#mtproto-auth-key-id) | fn | Computes Python `mtproto_auth_key_id(auth_key)` from a validated 256-byte key. |
| [`__pyfunction_mtproto_auth_key_id`](#pyfunction-mtproto-auth-key-id) | fn |  |
| [`mtproto_message_key`](#mtproto-message-key) | fn | Computes Python `mtproto_message_key` for padded plaintext and one MTProto direction. |
| [`__pyfunction_mtproto_message_key`](#pyfunction-mtproto-message-key) | fn |  |
| [`mtproto_derive_aes_key_iv`](#mtproto-derive-aes-key-iv) | fn | Derives the AES-256 key and IV used by Python `mtproto_derive_aes_key_iv`. |
| [`__pyfunction_mtproto_derive_aes_key_iv`](#pyfunction-mtproto-derive-aes-key-iv) | fn |  |
| [`mtproto_encrypt_payload`](#mtproto-encrypt-payload) | fn | Encrypts padded MTProto plaintext for Python `mtproto_encrypt_payload`. |
| [`__pyfunction_mtproto_encrypt_payload`](#pyfunction-mtproto-encrypt-payload) | fn |  |
| [`mtproto_decrypt_payload`](#mtproto-decrypt-payload) | fn | Decrypts and verifies Python `mtproto_decrypt_payload` ciphertext. |
| [`__pyfunction_mtproto_decrypt_payload`](#pyfunction-mtproto-decrypt-payload) | fn |  |
| [`xor_bytes`](#xor-bytes) | fn | Returns the bytewise exclusive-or of Python `xor_bytes(left, right)` inputs. |
| [`__pyfunction_xor_bytes`](#pyfunction-xor-bytes) | fn |  |
| [`aes_256_ige_encrypt`](#aes-256-ige-encrypt) | fn | Encrypts block-aligned bytes with Python `aes_256_ige_encrypt`. |
| [`__pyfunction_aes_256_ige_encrypt`](#pyfunction-aes-256-ige-encrypt) | fn |  |
| [`aes_256_ige_decrypt`](#aes-256-ige-decrypt) | fn | Decrypts block-aligned bytes with Python `aes_256_ige_decrypt`. |
| [`__pyfunction_aes_256_ige_decrypt`](#pyfunction-aes-256-ige-decrypt) | fn |  |
| [`aes_256_cbc_encrypt`](#aes-256-cbc-encrypt) | fn | Encrypts block-aligned bytes with Python `aes_256_cbc_encrypt` without padding. |
| [`__pyfunction_aes_256_cbc_encrypt`](#pyfunction-aes-256-cbc-encrypt) | fn |  |
| [`aes_256_cbc_decrypt`](#aes-256-cbc-decrypt) | fn | Decrypts block-aligned bytes with Python `aes_256_cbc_decrypt` without padding. |
| [`__pyfunction_aes_256_cbc_decrypt`](#pyfunction-aes-256-cbc-decrypt) | fn |  |
| [`aes_256_ctr_crypt`](#aes-256-ctr-crypt) | fn | Applies Python `aes_256_ctr_crypt` to data using AES-CTR keystream XOR. |
| [`__pyfunction_aes_256_ctr_crypt`](#pyfunction-aes-256-ctr-crypt) | fn |  |
| [`aes_256_gcm_encrypt`](#aes-256-gcm-encrypt) | fn | Authenticated-encrypts Python `aes_256_gcm_encrypt` plaintext and associated data. |
| [`__pyfunction_aes_256_gcm_encrypt`](#pyfunction-aes-256-gcm-encrypt) | fn |  |
| [`aes_256_gcm_decrypt`](#aes-256-gcm-decrypt) | fn | Authenticated-decrypts Python `aes_256_gcm_decrypt` ciphertext-and-tag bytes. |
| [`__pyfunction_aes_256_gcm_decrypt`](#pyfunction-aes-256-gcm-decrypt) | fn |  |
| [`scrypt_derive`](#scrypt-derive) | fn | Derives Python `scrypt_derive` bytes from password, salt, and scrypt cost parameters. |
| [`__pyfunction_scrypt_derive`](#pyfunction-scrypt-derive) | fn |  |
| [`pq_factorize`](#pq-factorize) | fn | Factorizes Python `pq_factorize(pq)` into ordered nontrivial `u64` factors. |
| [`__pyfunction_pq_factorize`](#pyfunction-pq-factorize) | fn |  |
| [`sha1_digest_raw`](#sha1-digest-raw) | fn | Computes SHA-1 for Rust callers without Python or GIL interaction. |
| [`sha256_digest_raw`](#sha256-digest-raw) | fn | Computes SHA-256 for Rust callers without Python or GIL interaction. |
| [`mtproto_auth_key_id_raw`](#mtproto-auth-key-id-raw) | fn | Derives the trailing eight SHA-1 bytes that identify a validated MTProto authorization key. |
| [`mtproto_message_key_raw`](#mtproto-message-key-raw) | fn | Derives an MTProto 2.0 message key from a validated authorization key and padded plaintext. |
| [`mtproto_derive_aes_key_iv_raw`](#mtproto-derive-aes-key-iv-raw) | fn | Derives the MTProto 2.0 AES-IGE key and IV from validated fixed-width key material. |
| [`mtproto_encrypt_payload_raw`](#mtproto-encrypt-payload-raw) | fn | Produces the auth-key identifier, message key, and AES-IGE ciphertext for padded plaintext. |
| [`mtproto_decrypt_payload_raw`](#mtproto-decrypt-payload-raw) | fn | Decrypts and authenticates an MTProto payload using validated directional key derivation. |
| [`xor_bytes_raw`](#xor-bytes-raw) | fn | Computes bytewise XOR for equal-length Rust byte slices. |
| [`aes_256_ige_encrypt_raw`](#aes-256-ige-encrypt-raw) | fn | Encrypts a block-aligned byte slice using AES-256 IGE for Rust callers. |
| [`aes_256_ige_decrypt_raw`](#aes-256-ige-decrypt-raw) | fn | Decrypts a block-aligned AES-256 IGE ciphertext for Rust callers. |
| [`aes_256_cbc_encrypt_raw`](#aes-256-cbc-encrypt-raw) | fn | Encrypts a block-aligned byte slice with unpadded AES-256 CBC. |
| [`aes_256_cbc_decrypt_raw`](#aes-256-cbc-decrypt-raw) | fn | Decrypts a block-aligned unpadded AES-256 CBC ciphertext. |
| [`aes_256_ctr_crypt_raw`](#aes-256-ctr-crypt-raw) | fn | XORs bytes with an AES-256 CTR keystream; the same operation encrypts and decrypts. |
| [`aes_256_gcm_encrypt_raw`](#aes-256-gcm-encrypt-raw) | fn | Authenticated-encrypts plaintext with AES-256 GCM and returns ciphertext plus tag. |
| [`aes_256_gcm_decrypt_raw`](#aes-256-gcm-decrypt-raw) | fn | Authenticated-decrypts AES-256 GCM ciphertext-and-tag data. |
| [`scrypt_derive_raw`](#scrypt-derive-raw) | fn | Runs scrypt with validated protocol-level output limits for Rust callers. |
| [`pq_factorize_raw`](#pq-factorize-raw) | fn | Finds and orders the two nontrivial factors of an MTProto `pq` value. |
| [`validate_auth_key`](#validate-auth-key) | fn | Validates the fixed 256-byte MTProto authorization-key width. |
| [`validate_msg_key`](#validate-msg-key) | fn | Validates the fixed 16-byte MTProto message-key width. |
| [`validate_block_multiple`](#validate-block-multiple) | fn | Validates that AES block-mode input has a whole-number count of AES blocks. |
| [`validate_aes_key`](#validate-aes-key) | fn | Validates a 32-byte AES-256 key and returns `ValueError` otherwise. |
| [`validate_ige_iv`](#validate-ige-iv) | fn | Validates the two-block, 32-byte IV required by AES-IGE. |
| [`validate_cbc_ctr_iv`](#validate-cbc-ctr-iv) | fn | Validates the one-block IV or counter used by CBC and CTR modes. |
| [`validate_gcm_nonce`](#validate-gcm-nonce) | fn | Validates the 12-byte nonce mandated by this AES-GCM interface. |
| [`direction_offset`](#direction-offset) | fn | Returns the MTProto key-schedule offset for the requested packet direction. |
| [`xor_block`](#xor-block) | fn | Computes a fixed-width XOR block used by the AES block-mode loops. |
| [`increment_counter`](#increment-counter) | fn | Advances a big-endian AES-CTR counter in place, wrapping at the full block width. |
| [`gcd`](#gcd) | fn | Computes the greatest common divisor used by Pollard-rho factorization. |
| [`mul_mod`](#mul-mod) | fn | Multiplies modulo `modulus` with a widened intermediate to avoid `u64` overflow. |
| [`pow_mod`](#pow-mod) | fn | Computes modular exponentiation for deterministic Miller-Rabin witnesses. |
| [`is_prime_u64`](#is-prime-u64) | fn | Deterministically tests whether a `u64` is prime using fixed Miller-Rabin witnesses. |
| [`factor_u64`](#factor-u64) | fn | Returns one factor of a composite `u64` using trial division and Pollard-rho iteration. |
| [`AES_BLOCK_SIZE`](#aes-block-size) | const | AES's fixed block size in bytes. |
| [`MT_PROTO_AUTH_KEY_SIZE`](#mt-proto-auth-key-size) | const | Required byte length of an MTProto authorization key. |
| [`MT_PROTO_MSG_KEY_SIZE`](#mt-proto-msg-key-size) | const | Required byte length of an MTProto 2.0 message key. |
| [`GIL_RELEASE_THRESHOLD_BYTES`](#gil-release-threshold-bytes) | const | Work-size threshold above which native wrappers detach from the Python GIL. |
| [`SCRYPT_MAX_MEMORY_BYTES`](#scrypt-max-memory-bytes) | const | Maximum memory estimate accepted by the public scrypt primitive. |
| [`SCRYPT_MAX_WORK_BYTES`](#scrypt-max-work-bytes) | const | Maximum CPU-work estimate accepted by the public scrypt primitive. |

## Functions

### `detach_if_large`

```rust
fn detach_if_large<T, F>(py: Python<'_>, work_bytes: usize, f: F) -> T
where
    T: Ungil,
    F: Ungil + FnOnce() -> T
```

*Defined in `rust/miniproto/src/crypto.rs:49-59`*

Runs `f` without the GIL when its input work estimate exceeds the native threshold.

`work_bytes` is an estimate used solely for GIL scheduling; `f` must satisfy PyO3's `Ungil`
requirements.  This helper preserves synchronous results and does not itself allocate.

# Arguments

- `T`: The GIL-independent result type returned by `f`.
- `F`: The one-shot GIL-independent closure performing the native operation.
- `py`: The acquired GIL token that can detach `f`.
- `work_bytes`: Conservative byte-work estimate compared with the detach threshold.
- `f`: The native computation to run attached or detached.

### `register`

```rust
fn register(m: &Bound<'_, pyo3::types::PyModule>) -> PyResult<()>
```

*Defined in `rust/miniproto/src/crypto.rs:68-88`*

Registers this module's fallback-compatible Python callables on `miniproto._native`.

Returns a PyO3 exception if a callable cannot be added to `m`.

# Arguments

- `m`: The Python extension module receiving the crypto callables.

### `native_available`

```rust
fn native_available() -> bool
```

*Defined in `rust/miniproto/src/crypto.rs:93-95`*

Implements Python `native_available`, which always returns `true` while this compiled callable
is importable. Python fallback selection happens before this function can be called.

### `__pyfunction_native_available`

```rust
unsafe fn __pyfunction_native_available<'py>(py: ::pyo3::Python<'py>, _slf: *mut ::pyo3::ffi::PyObject) -> ::pyo3::PyResult<*mut ::pyo3::ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:92`*

### `sha1_digest`

```rust
fn sha1_digest(py: Python<'_>, data: Vec<u8>) -> Vec<u8>
```

*Defined in `rust/miniproto/src/crypto.rs:106-108`*

Computes Python `sha1_digest(data)` and returns the 20-byte SHA-1 digest.

Large inputs are hashed with the GIL released.

# Arguments

- `py`: The acquired GIL token used to detach a large hash operation.
- `data`: Bytes to hash.

### `__pyfunction_sha1_digest`

```rust
unsafe fn __pyfunction_sha1_digest<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:105`*

### `sha256_digest`

```rust
fn sha256_digest(py: Python<'_>, data: Vec<u8>) -> Vec<u8>
```

*Defined in `rust/miniproto/src/crypto.rs:119-121`*

Computes Python `sha256_digest(data)` and returns the 32-byte SHA-256 digest.

Large inputs are hashed with the GIL released.

# Arguments

- `py`: The acquired GIL token used to detach a large hash operation.
- `data`: Bytes to hash.

### `__pyfunction_sha256_digest`

```rust
unsafe fn __pyfunction_sha256_digest<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:118`*

### `mtproto_auth_key_id`

```rust
fn mtproto_auth_key_id(auth_key: &[u8]) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:131-133`*

Computes Python `mtproto_auth_key_id(auth_key)` from a validated 256-byte key.

Returns `ValueError` when `auth_key` has the wrong length.

# Arguments

- `auth_key`: The 256-byte MTProto authorization key.

### `__pyfunction_mtproto_auth_key_id`

```rust
unsafe fn __pyfunction_mtproto_auth_key_id<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:130`*

### `mtproto_message_key`

```rust
fn mtproto_message_key(py: Python<'_>, auth_key: Vec<u8>, plaintext_with_padding: Vec<u8>, client_to_server: bool) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:147-162`*

Computes Python `mtproto_message_key` for padded plaintext and one MTProto direction.

Returns a 16-byte message key; rejects an invalid authorization key and releases the GIL for
large inputs.

# Arguments

- `py`: The acquired GIL token used to detach a large hash operation.
- `auth_key`: The 256-byte MTProto authorization key.
- `plaintext_with_padding`: Block-aligned inner plaintext that contributes to the message key.
- `client_to_server`: Selects the directional MTProto key offset.

### `__pyfunction_mtproto_message_key`

```rust
unsafe fn __pyfunction_mtproto_message_key<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:146`*

### `mtproto_derive_aes_key_iv`

```rust
fn mtproto_derive_aes_key_iv(py: Python<'_>, auth_key: Vec<u8>, msg_key: Vec<u8>, client_to_server: bool) -> PyResult<(Vec<u8>, Vec<u8>)>
```

*Defined in `rust/miniproto/src/crypto.rs:177-193`*

Derives the AES-256 key and IV used by Python `mtproto_derive_aes_key_iv`.

Returns `(key, iv)` and validates both fixed-width inputs. Valid inputs total 272 bytes
(`auth_key` 256 plus `msg_key` 16), so this wrapper never exceeds the detach threshold and
performs the derivation while holding the GIL.

# Arguments

- `py`: The acquired GIL token retained by this bounded-size operation.
- `auth_key`: The 256-byte MTProto authorization key.
- `msg_key`: The 16-byte MTProto message key.
- `client_to_server`: Selects the directional MTProto key offset.

### `__pyfunction_mtproto_derive_aes_key_iv`

```rust
unsafe fn __pyfunction_mtproto_derive_aes_key_iv<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:176`*

### `mtproto_encrypt_payload`

```rust
fn mtproto_encrypt_payload(py: Python<'_>, auth_key: Vec<u8>, plaintext_with_padding: Vec<u8>, client_to_server: bool) -> PyResult<(Vec<u8>, Vec<u8>, Vec<u8>)>
```

*Defined in `rust/miniproto/src/crypto.rs:207-217`*

Encrypts padded MTProto plaintext for Python `mtproto_encrypt_payload`.

Returns `(auth_key_id, msg_key, ciphertext)` or `ValueError` for invalid key or block input;
large work runs without the GIL.

# Arguments

- `py`: The acquired GIL token used to detach large encryption work.
- `auth_key`: The 256-byte MTProto authorization key.
- `plaintext_with_padding`: AES-block-aligned inner plaintext to encrypt.
- `client_to_server`: Selects the directional MTProto key schedule.

### `__pyfunction_mtproto_encrypt_payload`

```rust
unsafe fn __pyfunction_mtproto_encrypt_payload<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:206`*

### `mtproto_decrypt_payload`

```rust
fn mtproto_decrypt_payload(py: Python<'_>, auth_key: Vec<u8>, msg_key: Vec<u8>, ciphertext: Vec<u8>, client_to_server: bool) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:232-243`*

Decrypts and verifies Python `mtproto_decrypt_payload` ciphertext.

Returns padded plaintext or `ValueError` for invalid lengths, key material, or message-key
verification; large work runs without the GIL.

# Arguments

- `py`: The acquired GIL token used to detach large decryption work.
- `auth_key`: The 256-byte MTProto authorization key.
- `msg_key`: The 16-byte message key to verify.
- `ciphertext`: AES-IGE ciphertext whose length must be an AES-block multiple.
- `client_to_server`: Selects the directional MTProto key schedule.

### `__pyfunction_mtproto_decrypt_payload`

```rust
unsafe fn __pyfunction_mtproto_decrypt_payload<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:231`*

### `xor_bytes`

```rust
fn xor_bytes(left: &[u8], right: &[u8]) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:254-256`*

Returns the bytewise exclusive-or of Python `xor_bytes(left, right)` inputs.

Returns `ValueError` unless both inputs have equal length.

# Arguments

- `left`: First equal-length byte sequence.
- `right`: Second equal-length byte sequence.

### `__pyfunction_xor_bytes`

```rust
unsafe fn __pyfunction_xor_bytes<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:253`*

### `aes_256_ige_encrypt`

```rust
fn aes_256_ige_encrypt(py: Python<'_>, plaintext: Vec<u8>, key: Vec<u8>, iv: Vec<u8>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:270-280`*

Encrypts block-aligned bytes with Python `aes_256_ige_encrypt`.

Requires a 32-byte key and IV; returns `ValueError` for invalid lengths and releases the GIL
for large plaintexts.

# Arguments

- `py`: The acquired GIL token used to detach large encryption work.
- `plaintext`: AES-block-aligned bytes to encrypt.
- `key`: The 32-byte AES-256 key.
- `iv`: The 32-byte AES-IGE initialization vector.

### `__pyfunction_aes_256_ige_encrypt`

```rust
unsafe fn __pyfunction_aes_256_ige_encrypt<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:269`*

### `aes_256_ige_decrypt`

```rust
fn aes_256_ige_decrypt(py: Python<'_>, ciphertext: Vec<u8>, key: Vec<u8>, iv: Vec<u8>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:294-304`*

Decrypts block-aligned bytes with Python `aes_256_ige_decrypt`.

Requires a 32-byte key and IV; returns `ValueError` for invalid lengths and releases the GIL
for large ciphertexts.

# Arguments

- `py`: The acquired GIL token used to detach large decryption work.
- `ciphertext`: AES-block-aligned bytes to decrypt.
- `key`: The 32-byte AES-256 key.
- `iv`: The 32-byte AES-IGE initialization vector.

### `__pyfunction_aes_256_ige_decrypt`

```rust
unsafe fn __pyfunction_aes_256_ige_decrypt<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:293`*

### `aes_256_cbc_encrypt`

```rust
fn aes_256_cbc_encrypt(py: Python<'_>, plaintext: Vec<u8>, key: Vec<u8>, iv: Vec<u8>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:318-328`*

Encrypts block-aligned bytes with Python `aes_256_cbc_encrypt` without padding.

Requires 32-byte key and 16-byte IV inputs; invalid lengths become `ValueError` and large
plaintexts release the GIL.

# Arguments

- `py`: The acquired GIL token used to detach large encryption work.
- `plaintext`: AES-block-aligned bytes to encrypt.
- `key`: The 32-byte AES-256 key.
- `iv`: The 16-byte CBC initialization vector.

### `__pyfunction_aes_256_cbc_encrypt`

```rust
unsafe fn __pyfunction_aes_256_cbc_encrypt<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:317`*

### `aes_256_cbc_decrypt`

```rust
fn aes_256_cbc_decrypt(py: Python<'_>, ciphertext: Vec<u8>, key: Vec<u8>, iv: Vec<u8>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:342-352`*

Decrypts block-aligned bytes with Python `aes_256_cbc_decrypt` without padding.

Requires 32-byte key and 16-byte IV inputs; invalid lengths become `ValueError` and large
ciphertexts release the GIL.

# Arguments

- `py`: The acquired GIL token used to detach large decryption work.
- `ciphertext`: AES-block-aligned bytes to decrypt.
- `key`: The 32-byte AES-256 key.
- `iv`: The 16-byte CBC initialization vector.

### `__pyfunction_aes_256_cbc_decrypt`

```rust
unsafe fn __pyfunction_aes_256_cbc_decrypt<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:341`*

### `aes_256_ctr_crypt`

```rust
fn aes_256_ctr_crypt(py: Python<'_>, data: Vec<u8>, key: Vec<u8>, iv: Vec<u8>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:366-376`*

Applies Python `aes_256_ctr_crypt` to data using AES-CTR keystream XOR.

The same routine encrypts and decrypts; it validates the 32-byte key and 16-byte counter IV,
and releases the GIL for large data.

# Arguments

- `py`: The acquired GIL token used to detach large counter-mode work.
- `data`: Bytes to encrypt or decrypt.
- `key`: The 32-byte AES-256 key.
- `iv`: The 16-byte initial counter block.

### `__pyfunction_aes_256_ctr_crypt`

```rust
unsafe fn __pyfunction_aes_256_ctr_crypt<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:365`*

### `aes_256_gcm_encrypt`

```rust
fn aes_256_gcm_encrypt(py: Python<'_>, plaintext: Vec<u8>, key: Vec<u8>, nonce: Vec<u8>, associated_data: Vec<u8>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:391-402`*

Authenticated-encrypts Python `aes_256_gcm_encrypt` plaintext and associated data.

Returns ciphertext followed by its GCM tag, or `ValueError` for a bad 32-byte key, 12-byte
nonce, or encryption failure; large work releases the GIL.

# Arguments

- `py`: The acquired GIL token used to detach large authenticated-encryption work.
- `plaintext`: Bytes to encrypt.
- `key`: The 32-byte AES-256 key.
- `nonce`: The 12-byte GCM nonce.
- `associated_data`: Authenticated bytes that are not encrypted.

### `__pyfunction_aes_256_gcm_encrypt`

```rust
unsafe fn __pyfunction_aes_256_gcm_encrypt<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:390`*

### `aes_256_gcm_decrypt`

```rust
fn aes_256_gcm_decrypt(py: Python<'_>, ciphertext_and_tag: Vec<u8>, key: Vec<u8>, nonce: Vec<u8>, associated_data: Vec<u8>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:417-428`*

Authenticated-decrypts Python `aes_256_gcm_decrypt` ciphertext-and-tag bytes.

Returns plaintext or `ValueError` for invalid key/nonce material or authentication failure;
large work releases the GIL.

# Arguments

- `py`: The acquired GIL token used to detach large authenticated-decryption work.
- `ciphertext_and_tag`: GCM ciphertext followed by its authentication tag.
- `key`: The 32-byte AES-256 key.
- `nonce`: The 12-byte GCM nonce.
- `associated_data`: Authenticated bytes that are not encrypted.

### `__pyfunction_aes_256_gcm_decrypt`

```rust
unsafe fn __pyfunction_aes_256_gcm_decrypt<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:416`*

### `scrypt_derive`

```rust
fn scrypt_derive(py: Python<'_>, password: Vec<u8>, salt: Vec<u8>, n: u32, r: u32, p: u32, length: usize) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:446-463`*

Derives Python `scrypt_derive` bytes from password, salt, and scrypt cost parameters.

`n` must be a power of two above one and `length` is limited to 1..=1024; invalid parameters
return `ValueError`. Estimated memory is capped at 256 MiB and aggregate work at 1 GiB. The
GIL is released when the `128 * n * r * p` work estimate exceeds 4 KiB.

# Arguments

- `py`: The acquired GIL token used to detach only sufficiently large scrypt work.
- `password`: Password bytes accepted by scrypt.
- `salt`: Salt bytes accepted by scrypt.
- `n`: CPU/memory cost, required to be a power of two greater than one.
- `r`: scrypt block-size cost parameter.
- `p`: scrypt parallelization cost parameter.
- `length`: Requested derived-key length in the inclusive range 1..=1024.

### `__pyfunction_scrypt_derive`

```rust
unsafe fn __pyfunction_scrypt_derive<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:445`*

### `pq_factorize`

```rust
fn pq_factorize(py: Python<'_>, pq: u64) -> PyResult<(u64, u64)>
```

*Defined in `rust/miniproto/src/crypto.rs:475-477`*

Factorizes Python `pq_factorize(pq)` into ordered nontrivial `u64` factors.

Returns `ValueError` for non-composite values and runs the potentially expensive search with
the GIL released.

# Arguments

- `py`: The acquired GIL token used to detach the factorization search.
- `pq`: Composite MTProto handshake value to split into ordered factors.

### `__pyfunction_pq_factorize`

```rust
unsafe fn __pyfunction_pq_factorize<'py>(py: Python<'py>, _slf: *mut ffi::PyObject, _args: *const *mut ffi::PyObject, _nargs: ffi::Py_ssize_t, _kwargs: *mut ffi::PyObject) -> PyResult<*mut ffi::PyObject>
```

*Defined in `rust/miniproto/src/crypto.rs:474`*

### `sha1_digest_raw`

```rust
fn sha1_digest_raw(data: &[u8]) -> Vec<u8>
```

*Defined in `rust/miniproto/src/crypto.rs:484-486`*

Computes SHA-1 for Rust callers without Python or GIL interaction.

# Arguments

- `data`: Bytes to hash.

### `sha256_digest_raw`

```rust
fn sha256_digest_raw(data: &[u8]) -> Vec<u8>
```

*Defined in `rust/miniproto/src/crypto.rs:493-495`*

Computes SHA-256 for Rust callers without Python or GIL interaction.

# Arguments

- `data`: Bytes to hash.

### `mtproto_auth_key_id_raw`

```rust
fn mtproto_auth_key_id_raw(auth_key: &[u8]) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:504-508`*

Derives the trailing eight SHA-1 bytes that identify a validated MTProto authorization key.

Returns `ValueError` if the key is not exactly 256 bytes; does not acquire the GIL.

# Arguments

- `auth_key`: Authorization key whose SHA-1 tail supplies the identifier.

### `mtproto_message_key_raw`

```rust
fn mtproto_message_key_raw(auth_key: &[u8], plaintext_with_padding: &[u8], client_to_server: bool) -> Vec<u8>
```

*Defined in `rust/miniproto/src/crypto.rs:520-531`*

Derives an MTProto 2.0 message key from a validated authorization key and padded plaintext.

Callers must validate the authorization-key length before use because this internal primitive
slices its fixed protocol ranges directly.

# Arguments

- `auth_key`: Previously validated 256-byte authorization key.
- `plaintext_with_padding`: Padded inner plaintext to include in the SHA-256 derivation.
- `client_to_server`: Selects the directional key offset.

### `mtproto_derive_aes_key_iv_raw`

```rust
fn mtproto_derive_aes_key_iv_raw(auth_key: &[u8], msg_key: &[u8], client_to_server: bool) -> (Vec<u8>, Vec<u8>)
```

*Defined in `rust/miniproto/src/crypto.rs:542-568`*

Derives the MTProto 2.0 AES-IGE key and IV from validated fixed-width key material.

Callers must validate `auth_key` and `msg_key` before calling; the function has no GIL use.

# Arguments

- `auth_key`: Previously validated 256-byte authorization key.
- `msg_key`: Previously validated 16-byte message key.
- `client_to_server`: Selects the directional key offset.

### `mtproto_encrypt_payload_raw`

```rust
fn mtproto_encrypt_payload_raw(auth_key: &[u8], plaintext_with_padding: &[u8], client_to_server: bool) -> PyResult<(Vec<u8>, Vec<u8>, Vec<u8>)>
```

*Defined in `rust/miniproto/src/crypto.rs:579-591`*

Produces the auth-key identifier, message key, and AES-IGE ciphertext for padded plaintext.

Returns `ValueError` for malformed keys or non-block-aligned plaintext; no GIL interaction.

# Arguments

- `auth_key`: 256-byte authorization key used for id, message key, and AES derivation.
- `plaintext_with_padding`: AES-block-aligned inner plaintext to encrypt.
- `client_to_server`: Selects the directional MTProto key schedule.

### `mtproto_decrypt_payload_raw`

```rust
fn mtproto_decrypt_payload_raw(auth_key: &[u8], msg_key: &[u8], ciphertext: &[u8], client_to_server: bool) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:603-620`*

Decrypts and authenticates an MTProto payload using validated directional key derivation.

Returns `ValueError` for malformed inputs or a message-key mismatch; no GIL interaction.

# Arguments

- `auth_key`: 256-byte authorization key used for directional AES derivation.
- `msg_key`: 16-byte message key expected after decryption.
- `ciphertext`: AES-block-aligned encrypted payload.
- `client_to_server`: Selects the directional MTProto key schedule.

### `xor_bytes_raw`

```rust
fn xor_bytes_raw(left: &[u8], right: &[u8]) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:630-637`*

Computes bytewise XOR for equal-length Rust byte slices.

Returns `ValueError` for unequal lengths and does not use the GIL.

# Arguments

- `left`: First equal-length byte slice.
- `right`: Second equal-length byte slice.

### `aes_256_ige_encrypt_raw`

```rust
fn aes_256_ige_encrypt_raw(plaintext: &[u8], key: &[u8], iv: &[u8]) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:648-675`*

Encrypts a block-aligned byte slice using AES-256 IGE for Rust callers.

Returns `ValueError` unless the key, IV, and plaintext lengths meet AES-IGE requirements.

# Arguments

- `plaintext`: AES-block-aligned bytes to encrypt.
- `key`: The 32-byte AES-256 key.
- `iv`: The 32-byte AES-IGE initialization vector.

### `aes_256_ige_decrypt_raw`

```rust
fn aes_256_ige_decrypt_raw(ciphertext: &[u8], key: &[u8], iv: &[u8]) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:686-713`*

Decrypts a block-aligned AES-256 IGE ciphertext for Rust callers.

Returns `ValueError` unless the key, IV, and ciphertext lengths meet AES-IGE requirements.

# Arguments

- `ciphertext`: AES-block-aligned bytes to decrypt.
- `key`: The 32-byte AES-256 key.
- `iv`: The 32-byte AES-IGE initialization vector.

### `aes_256_cbc_encrypt_raw`

```rust
fn aes_256_cbc_encrypt_raw(plaintext: &[u8], key: &[u8], iv: &[u8]) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:724-744`*

Encrypts a block-aligned byte slice with unpadded AES-256 CBC.

Returns `ValueError` unless the key, IV, and plaintext lengths are valid.

# Arguments

- `plaintext`: AES-block-aligned bytes to encrypt.
- `key`: The 32-byte AES-256 key.
- `iv`: The 16-byte CBC initialization vector.

### `aes_256_cbc_decrypt_raw`

```rust
fn aes_256_cbc_decrypt_raw(ciphertext: &[u8], key: &[u8], iv: &[u8]) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:755-776`*

Decrypts a block-aligned unpadded AES-256 CBC ciphertext.

Returns `ValueError` unless the key, IV, and ciphertext lengths are valid.

# Arguments

- `ciphertext`: AES-block-aligned bytes to decrypt.
- `key`: The 32-byte AES-256 key.
- `iv`: The 16-byte CBC initialization vector.

### `aes_256_ctr_crypt_raw`

```rust
fn aes_256_ctr_crypt_raw(data: &[u8], key: &[u8], iv: &[u8]) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:787-801`*

XORs bytes with an AES-256 CTR keystream; the same operation encrypts and decrypts.

Returns `ValueError` unless `key` is 32 bytes and `iv` is one AES block.

# Arguments

- `data`: Bytes to XOR with the generated CTR keystream.
- `key`: The 32-byte AES-256 key.
- `iv`: The 16-byte initial counter block.

### `aes_256_gcm_encrypt_raw`

```rust
fn aes_256_gcm_encrypt_raw(plaintext: &[u8], key: &[u8], nonce: &[u8], associated_data: &[u8]) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:813-834`*

Authenticated-encrypts plaintext with AES-256 GCM and returns ciphertext plus tag.

Returns `ValueError` for an invalid key or nonce or if the cipher rejects the operation.

# Arguments

- `plaintext`: Bytes to encrypt.
- `key`: The 32-byte AES-256 key.
- `nonce`: The 12-byte GCM nonce.
- `associated_data`: Authenticated bytes that are not encrypted.

### `aes_256_gcm_decrypt_raw`

```rust
fn aes_256_gcm_decrypt_raw(ciphertext_and_tag: &[u8], key: &[u8], nonce: &[u8], associated_data: &[u8]) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:846-867`*

Authenticated-decrypts AES-256 GCM ciphertext-and-tag data.

Returns `ValueError` for invalid key/nonce material or a failed authentication check.

# Arguments

- `ciphertext_and_tag`: GCM ciphertext followed by its authentication tag.
- `key`: The 32-byte AES-256 key.
- `nonce`: The 12-byte GCM nonce.
- `associated_data`: Authenticated bytes that are not encrypted.

### `scrypt_derive_raw`

```rust
fn scrypt_derive_raw(password: &[u8], salt: &[u8], n: u32, r: u32, p: u32, length: usize) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:882-918`*

Runs scrypt with validated protocol-level output limits for Rust callers.

Returns `ValueError` for invalid cost parameters, an unsupported output length, or derivation
failure.  This is a synchronous, GIL-free primitive.

# Arguments

- `password`: Password bytes accepted by scrypt.
- `salt`: Salt bytes accepted by scrypt.
- `n`: CPU/memory cost, required to be a power of two greater than one.
- `r`: scrypt block-size cost parameter.
- `p`: scrypt parallelization cost parameter.
- `length`: Requested derived-key length in the inclusive range 1..=1024.

### `pq_factorize_raw`

```rust
fn pq_factorize_raw(pq: u64) -> PyResult<(u64, u64)>
```

*Defined in `rust/miniproto/src/crypto.rs:927-941`*

Finds and orders the two nontrivial factors of an MTProto `pq` value.

Returns `ValueError` for values below four or values that are not composite.

# Arguments

- `pq`: Candidate composite integer to split into its two ordered factors.

### `validate_auth_key`

```rust
fn validate_auth_key(auth_key: &[u8]) -> PyResult<()>
```

*Defined in `rust/miniproto/src/crypto.rs:950-955`*

Validates the fixed 256-byte MTProto authorization-key width.

Returns `ValueError` rather than allowing fixed-offset protocol code to panic.

# Arguments

- `auth_key`: Candidate authorization key expected to contain 256 bytes.

### `validate_msg_key`

```rust
fn validate_msg_key(msg_key: &[u8]) -> PyResult<()>
```

*Defined in `rust/miniproto/src/crypto.rs:964-969`*

Validates the fixed 16-byte MTProto message-key width.

Returns `ValueError` on a malformed input slice.

# Arguments

- `msg_key`: Candidate message key expected to contain 16 bytes.

### `validate_block_multiple`

```rust
fn validate_block_multiple(data: &[u8]) -> PyResult<()>
```

*Defined in `rust/miniproto/src/crypto.rs:978-985`*

Validates that AES block-mode input has a whole-number count of AES blocks.

Returns `ValueError` when the byte length is not divisible by 16.

# Arguments

- `data`: Candidate AES block-mode input.

### `validate_aes_key`

```rust
fn validate_aes_key(key: &[u8]) -> PyResult<()>
```

*Defined in `rust/miniproto/src/crypto.rs:992-997`*

Validates a 32-byte AES-256 key and returns `ValueError` otherwise.

# Arguments

- `key`: Candidate AES-256 key.

### `validate_ige_iv`

```rust
fn validate_ige_iv(iv: &[u8]) -> PyResult<()>
```

*Defined in `rust/miniproto/src/crypto.rs:1004-1009`*

Validates the two-block, 32-byte IV required by AES-IGE.

# Arguments

- `iv`: Candidate AES-IGE initialization vector.

### `validate_cbc_ctr_iv`

```rust
fn validate_cbc_ctr_iv(iv: &[u8]) -> PyResult<()>
```

*Defined in `rust/miniproto/src/crypto.rs:1016-1021`*

Validates the one-block IV or counter used by CBC and CTR modes.

# Arguments

- `iv`: Candidate CBC initialization vector or CTR counter block.

### `validate_gcm_nonce`

```rust
fn validate_gcm_nonce(nonce: &[u8]) -> PyResult<()>
```

*Defined in `rust/miniproto/src/crypto.rs:1028-1033`*

Validates the 12-byte nonce mandated by this AES-GCM interface.

# Arguments

- `nonce`: Candidate AES-GCM nonce.

### `direction_offset`

```rust
fn direction_offset(client_to_server: bool) -> usize
```

*Defined in `rust/miniproto/src/crypto.rs:1040-1042`*

Returns the MTProto key-schedule offset for the requested packet direction.

# Arguments

- `client_to_server`: Whether the packet travels from client to server.

### `xor_block`

```rust
fn xor_block(left: &[u8; 16], right: &[u8; 16]) -> [u8; 16]
```

*Defined in `rust/miniproto/src/crypto.rs:1050-1056`*

Computes a fixed-width XOR block used by the AES block-mode loops.

# Arguments

- `left`: First AES-sized block.
- `right`: Second AES-sized block.

### `increment_counter`

```rust
fn increment_counter(counter: &mut [u8; 16])
```

*Defined in `rust/miniproto/src/crypto.rs:1063-1071`*

Advances a big-endian AES-CTR counter in place, wrapping at the full block width.

# Arguments

- `counter`: Mutable AES-sized counter block to increment.

### `gcd`

```rust
fn gcd(left: u64, right: u64) -> u64
```

*Defined in `rust/miniproto/src/crypto.rs:1079-1086`*

Computes the greatest common divisor used by Pollard-rho factorization.

# Arguments

- `left`: First nonnegative integer.
- `right`: Second nonnegative integer.

### `mul_mod`

```rust
fn mul_mod(left: u64, right: u64, modulus: u64) -> u64
```

*Defined in `rust/miniproto/src/crypto.rs:1100-1102`*

Multiplies modulo `modulus` with a widened intermediate to avoid `u64` overflow.

# Panics

Panics if `modulus` is zero because the remainder operation is undefined. Callers must also
pass a nonzero modulus; `u128` widening prevents multiplication overflow for all `u64` inputs.

# Arguments

- `left`: First modular multiplicand.
- `right`: Second modular multiplicand.
- `modulus`: Nonzero modulus used for the reduced product.

### `pow_mod`

```rust
fn pow_mod(base: u64, exponent: u64, modulus: u64) -> u64
```

*Defined in `rust/miniproto/src/crypto.rs:1116-1126`*

Computes modular exponentiation for deterministic Miller-Rabin witnesses.

# Panics

Panics if `modulus` is zero because both reduction paths use remainder operations. Arithmetic
overflow is avoided by delegating products to `mul_mod` with its widened intermediate.

# Arguments

- `base`: Base to exponentiate modulo `modulus`.
- `exponent`: Nonnegative exponent encoded as `u64`.
- `modulus`: Nonzero modulus used for every reduction.

### `is_prime_u64`

```rust
fn is_prime_u64(value: u64) -> bool
```

*Defined in `rust/miniproto/src/crypto.rs:1133-1172`*

Deterministically tests whether a `u64` is prime using fixed Miller-Rabin witnesses.

# Arguments

- `value`: Unsigned integer to classify as prime or composite.

### `factor_u64`

```rust
fn factor_u64(value: u64) -> u64
```

*Defined in `rust/miniproto/src/crypto.rs:1179-1207`*

Returns one factor of a composite `u64` using trial division and Pollard-rho iteration.

# Arguments

- `value`: Composite unsigned integer whose nontrivial factor is requested.

## Constants

### `AES_BLOCK_SIZE`
```rust
const AES_BLOCK_SIZE: usize = 16usize;
```

*Defined in `rust/miniproto/src/crypto.rs:25`*

AES's fixed block size in bytes.

### `MT_PROTO_AUTH_KEY_SIZE`
```rust
const MT_PROTO_AUTH_KEY_SIZE: usize = 256usize;
```

*Defined in `rust/miniproto/src/crypto.rs:27`*

Required byte length of an MTProto authorization key.

### `MT_PROTO_MSG_KEY_SIZE`
```rust
const MT_PROTO_MSG_KEY_SIZE: usize = 16usize;
```

*Defined in `rust/miniproto/src/crypto.rs:29`*

Required byte length of an MTProto 2.0 message key.

### `GIL_RELEASE_THRESHOLD_BYTES`
```rust
const GIL_RELEASE_THRESHOLD_BYTES: usize = 4_096usize;
```

*Defined in `rust/miniproto/src/crypto.rs:31`*

Work-size threshold above which native wrappers detach from the Python GIL.

### `SCRYPT_MAX_MEMORY_BYTES`
```rust
const SCRYPT_MAX_MEMORY_BYTES: usize = 268_435_456usize;
```

*Defined in `rust/miniproto/src/crypto.rs:33`*

Maximum memory estimate accepted by the public scrypt primitive.

### `SCRYPT_MAX_WORK_BYTES`
```rust
const SCRYPT_MAX_WORK_BYTES: usize = 1_073_741_824usize;
```

*Defined in `rust/miniproto/src/crypto.rs:35`*

Maximum CPU-work estimate accepted by the public scrypt primitive.
