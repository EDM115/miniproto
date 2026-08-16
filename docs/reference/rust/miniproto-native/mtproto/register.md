---
title: "miniproto_native::mtproto::register"
description: "Adds the Python-visible MTProto envelope functions to `miniproto._native`."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::mtproto::register"
source_path: "rust/miniproto/src/mtproto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/mtproto.rs#L77"
crate: "miniproto_native"
python_visible: false
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `public`
- Source: [`rust/miniproto/src/mtproto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/mtproto.rs#L77)
- Python exposure: Not evidenced by static PyO3 attributes.

## Signature

```rust
fn register(m: &_) -> _
```

## Arguments

- `m`: The Python extension module to receive the envelope callables.

## cargo-docs-md rendering

### `register`

```rust
fn register(m: &Bound<'_, pyo3::types::PyModule>) -> PyResult<()>
```

*Defined in `rust\miniproto\src\mtproto.rs:77-81`*

Adds the Python-visible MTProto envelope functions to `miniproto._native`.

Returns a Python exception when PyO3 cannot register either callable.

# Arguments

- `m`: The Python extension module to receive the envelope callables.
