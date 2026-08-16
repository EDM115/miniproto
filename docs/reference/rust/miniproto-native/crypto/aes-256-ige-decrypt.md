---
title: "miniproto_native::crypto::aes_256_ige_decrypt"
description: "Decrypts block-aligned bytes with Python `aes_256_ige_decrypt`."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::aes_256_ige_decrypt"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L289"
aliases: ["miniproto._native.aes_256_ige_decrypt"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L289)
- Python exposure: `miniproto._native.aes_256_ige_decrypt` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn aes_256_ige_decrypt(py: _, ciphertext: _, key: _, iv: _) -> _
```

## Arguments

- `py`: The acquired GIL token used to detach large decryption work.
- `ciphertext`: AES-block-aligned bytes to decrypt.
- `key`: The 32-byte AES-256 key.
- `iv`: The 32-byte AES-IGE initialization vector.

## cargo-docs-md rendering

### `aes_256_ige_decrypt`

```rust
fn aes_256_ige_decrypt(py: Python<'_>, ciphertext: Vec<u8>, key: Vec<u8>, iv: Vec<u8>) -> PyResult<Vec<u8>>
```

*Defined in `rust\miniproto\src\crypto.rs:289-299`*

Decrypts block-aligned bytes with Python `aes_256_ige_decrypt`.

Requires a 32-byte key and IV; returns `ValueError` for invalid lengths and releases the GIL
for large ciphertexts.

# Arguments

- `py`: The acquired GIL token used to detach large decryption work.
- `ciphertext`: AES-block-aligned bytes to decrypt.
- `key`: The 32-byte AES-256 key.
- `iv`: The 32-byte AES-IGE initialization vector.
