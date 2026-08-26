---
title: "miniproto_native::crypto::register"
description: "Registers this module's fallback-compatible Python callables on `miniproto._native`."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::register"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L68"
python_visible: false
---

## Provenance

- Rust visibility: `public`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L68)
- Python exposure: Not evidenced by static PyO3 attributes.

## Signature

```rust
fn register(m: &_) -> _
```

## Arguments

- `m`: The Python extension module receiving the crypto callables.

## cargo-docs-md rendering

### `register`

```rust
fn register(m: &Bound<'_, pyo3::types::PyModule>) -> PyResult<()>
```

*Defined in `rust/miniproto/src/crypto.rs:68-88`*

Registers this module's fallback-compatible Python callables on `miniproto._native`.

Returns a PyO3 exception if a callable cannot be added to `m`.

# Arguments

- `m`: The Python extension module receiving the crypto callables.
