---
title: "miniproto_native::crypto::aes_256_gcm_encrypt"
description: "Authenticated-encrypts Python `aes_256_gcm_encrypt` plaintext and associated data."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::aes_256_gcm_encrypt"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L391"
aliases: ["miniproto._native.aes_256_gcm_encrypt"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L391)
- Python exposure: `miniproto._native.aes_256_gcm_encrypt` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn aes_256_gcm_encrypt(py: _, plaintext: _, key: _, nonce: _, associated_data: _) -> _
```

## Arguments

- `py`: The acquired GIL token used to detach large authenticated-encryption work.
- `plaintext`: Bytes to encrypt.
- `key`: The 32-byte AES-256 key.
- `nonce`: The 12-byte GCM nonce.
- `associated_data`: Authenticated bytes that are not encrypted.

## cargo-docs-md rendering

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
