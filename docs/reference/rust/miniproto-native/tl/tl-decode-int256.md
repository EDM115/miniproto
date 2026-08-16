---
title: "miniproto_native::tl::tl_decode_int256"
description: "Decodes Python `tl_decode_int256(data, offset)` to a Python integer and next offset."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_decode_int256"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L613"
aliases: ["miniproto._native.tl_decode_int256"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L613)
- Python exposure: `miniproto._native.tl_decode_int256` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_decode_int256(py: _, data: &[u8], offset: usize) -> _
```

## Arguments

- `py`: The acquired GIL token used to construct the Python integer.
- `data`: TL bytes containing a 32-byte integer field.
- `offset`: Byte offset at which the fixed-width field starts.

## cargo-docs-md rendering

### `tl_decode_int256`

```rust
fn tl_decode_int256(py: Python<'_>, data: &[u8], offset: usize) -> PyResult<(Py<PyAny>, usize)>
```

*Defined in `rust\miniproto\src\tl.rs:613-616`*

Decodes Python `tl_decode_int256(data, offset)` to a Python integer and next offset.

Returns `ValueError` for truncated input and holds the GIL to construct the Python integer.

# Arguments

- `py`: The acquired GIL token used to construct the Python integer.
- `data`: TL bytes containing a 32-byte integer field.
- `offset`: Byte offset at which the fixed-width field starts.
