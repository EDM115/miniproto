---
title: "miniproto_native::crypto::aes_256_cbc_encrypt"
description: "Encrypts block-aligned bytes with Python `aes_256_cbc_encrypt` without padding."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::aes_256_cbc_encrypt"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L318"
aliases: ["miniproto._native.aes_256_cbc_encrypt"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L318)
- Python exposure: `miniproto._native.aes_256_cbc_encrypt` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn aes_256_cbc_encrypt(py: _, plaintext: _, key: _, iv: _) -> _
```

## Arguments

- `py`: The acquired GIL token used to detach large encryption work.
- `plaintext`: AES-block-aligned bytes to encrypt.
- `key`: The 32-byte AES-256 key.
- `iv`: The 16-byte CBC initialization vector.

## cargo-docs-md rendering

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
