---
title: "miniproto_native::crypto::sha256_digest"
description: "Computes Python `sha256_digest(data)` and returns the 32-byte SHA-256 digest."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::sha256_digest"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L119"
aliases: ["miniproto._native.sha256_digest"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L119)
- Python exposure: `miniproto._native.sha256_digest` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn sha256_digest(py: _, data: _) -> _
```

## Arguments

- `py`: The acquired GIL token used to detach a large hash operation.
- `data`: Bytes to hash.

## cargo-docs-md rendering

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
