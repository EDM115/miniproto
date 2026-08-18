---
title: "miniproto_native::crypto::aes_256_ige_encrypt"
description: "Encrypts block-aligned bytes with Python `aes_256_ige_encrypt`."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::aes_256_ige_encrypt"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L265"
aliases: ["miniproto._native.aes_256_ige_encrypt"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L265)
- Python exposure: `miniproto._native.aes_256_ige_encrypt` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn aes_256_ige_encrypt(py: _, plaintext: _, key: _, iv: _) -> _
```

## Arguments

- `py`: The acquired GIL token used to detach large encryption work.
- `plaintext`: AES-block-aligned bytes to encrypt.
- `key`: The 32-byte AES-256 key.
- `iv`: The 32-byte AES-IGE initialization vector.

## cargo-docs-md rendering

### `aes_256_ige_encrypt`

```rust
fn aes_256_ige_encrypt(py: Python<'_>, plaintext: Vec<u8>, key: Vec<u8>, iv: Vec<u8>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:265-275`*

Encrypts block-aligned bytes with Python `aes_256_ige_encrypt`.

Requires a 32-byte key and IV; returns `ValueError` for invalid lengths and releases the GIL
for large plaintexts.

# Arguments

- `py`: The acquired GIL token used to detach large encryption work.
- `plaintext`: AES-block-aligned bytes to encrypt.
- `key`: The 32-byte AES-256 key.
- `iv`: The 32-byte AES-IGE initialization vector.
