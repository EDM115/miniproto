---
title: "miniproto_native::crypto::aes_256_gcm_decrypt"
description: "Authenticated-decrypts Python `aes_256_gcm_decrypt` ciphertext-and-tag bytes."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::aes_256_gcm_decrypt"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L412"
aliases: ["miniproto._native.aes_256_gcm_decrypt"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L412)
- Python exposure: `miniproto._native.aes_256_gcm_decrypt` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn aes_256_gcm_decrypt(py: _, ciphertext_and_tag: _, key: _, nonce: _, associated_data: _) -> _
```

## Arguments

- `py`: The acquired GIL token used to detach large authenticated-decryption work.
- `ciphertext_and_tag`: GCM ciphertext followed by its authentication tag.
- `key`: The 32-byte AES-256 key.
- `nonce`: The 12-byte GCM nonce.
- `associated_data`: Authenticated bytes that are not encrypted.

## cargo-docs-md rendering

### `aes_256_gcm_decrypt`

```rust
fn aes_256_gcm_decrypt(py: Python<'_>, ciphertext_and_tag: Vec<u8>, key: Vec<u8>, nonce: Vec<u8>, associated_data: Vec<u8>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:412-423`*

Authenticated-decrypts Python `aes_256_gcm_decrypt` ciphertext-and-tag bytes.

Returns plaintext or `ValueError` for invalid key/nonce material or authentication failure;
large work releases the GIL.

# Arguments

- `py`: The acquired GIL token used to detach large authenticated-decryption work.
- `ciphertext_and_tag`: GCM ciphertext followed by its authentication tag.
- `key`: The 32-byte AES-256 key.
- `nonce`: The 12-byte GCM nonce.
- `associated_data`: Authenticated bytes that are not encrypted.
