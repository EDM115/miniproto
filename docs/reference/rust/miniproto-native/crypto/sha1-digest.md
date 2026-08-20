---
title: "miniproto_native::crypto::sha1_digest"
description: "Computes Python `sha1_digest(data)` and returns the 20-byte SHA-1 digest."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::sha1_digest"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L106"
aliases: ["miniproto._native.sha1_digest"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L106)
- Python exposure: `miniproto._native.sha1_digest` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn sha1_digest(py: _, data: _) -> _
```

## Arguments

- `py`: The acquired GIL token used to detach a large hash operation.
- `data`: Bytes to hash.

## cargo-docs-md rendering

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
