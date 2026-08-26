---
title: "miniproto_native::tl::register"
description: "Registers the fallback-compatible `tl_*` Python functions on `miniproto._native`."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::register"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L102"
python_visible: false
---

## Provenance

- Rust visibility: `public`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L102)
- Python exposure: Not evidenced by static PyO3 attributes.

## Signature

```rust
fn register(m: &_) -> _
```

## Arguments

- `m`: The Python extension module receiving the TL callables.

## cargo-docs-md rendering

### `register`

```rust
fn register(m: &Bound<'_, pyo3::types::PyModule>) -> PyResult<()>
```

*Defined in `rust/miniproto/src/tl.rs:102-126`*

Registers the fallback-compatible `tl_*` Python functions on `miniproto._native`.

Returns a PyO3 error if any function cannot be exported.

# Arguments

- `m`: The Python extension module receiving the TL callables.
