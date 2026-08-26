---
title: "miniproto_native::crypto::aes_256_ctr_crypt"
description: "Applies Python `aes_256_ctr_crypt` to data using AES-CTR keystream XOR."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::aes_256_ctr_crypt"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L366"
aliases: ["miniproto._native.aes_256_ctr_crypt"]
python_visible: true
---

## Provenance

- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L366)
- Python exposure: `miniproto._native.aes_256_ctr_crypt` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn aes_256_ctr_crypt(py: _, data: _, key: _, iv: _) -> _
```

## Arguments

- `py`: The acquired GIL token used to detach large counter-mode work.
- `data`: Bytes to encrypt or decrypt.
- `key`: The 32-byte AES-256 key.
- `iv`: The 16-byte initial counter block.

## cargo-docs-md rendering

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
