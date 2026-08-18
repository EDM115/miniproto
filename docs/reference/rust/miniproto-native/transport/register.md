---
title: "miniproto_native::transport::register"
description: "Registers Python `TransportCodec` and `quick_ack_token` on `miniproto._native`."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::transport::register"
source_path: "rust/miniproto/src/transport.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs#L39"
crate: "miniproto_native"
python_visible: false
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `public`
- Source: [`rust/miniproto/src/transport.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs#L39)
- Python exposure: Not evidenced by static PyO3 attributes.

## Signature

```rust
fn register(m: &_) -> _
```

## Arguments

- `m`: The Python extension module receiving the transport exports.

## cargo-docs-md rendering

### `register`

```rust
fn register(m: &Bound<'_, pyo3::types::PyModule>) -> PyResult<()>
```

*Defined in `rust/miniproto/src/transport.rs:39-43`*

Registers Python `TransportCodec` and `quick_ack_token` on `miniproto._native`.

Returns a PyO3 exception if either export cannot be installed.

# Arguments

- `m`: The Python extension module receiving the transport exports.
