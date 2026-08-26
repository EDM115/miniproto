---
title: "miniproto_native::tl::tl_fast_decode"
description: "Attempts Python `tl_fast_decode` for a generated constructor at `offset`."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_fast_decode"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L210"
aliases: ["miniproto._native.tl_fast_decode"]
python_visible: true
---

## Provenance

- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L210)
- Python exposure: `miniproto._native.tl_fast_decode` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_fast_decode(py: _, constructor_id: u32, data: &[u8], offset: usize, boxed: bool) -> _
```

## Arguments

- `py`: The acquired GIL token used to construct decoded Python values.
- `constructor_id`: Generated TL constructor id selecting a trusted fast-path descriptor.
- `data`: TL wire bytes to decode.
- `offset`: Byte offset at which this constructor begins.
- `boxed`: Whether `data` starts with and must match the constructor id.

## cargo-docs-md rendering

### `tl_fast_decode`

```rust
fn tl_fast_decode(py: Python<'_>, constructor_id: u32, data: &[u8], offset: usize, boxed: bool) -> PyResult<Option<(Py<pyo3::types::PyTuple>, usize)>>
```

*Defined in `rust/miniproto/src/tl.rs:210-266`*

Attempts Python `tl_fast_decode` for a generated constructor at `offset`.

`boxed` requires and verifies the constructor id. Returns `None` if no native decoder exists,
otherwise `(values_tuple, next_offset)`; malformed wire input raises a Python exception. This
conversion necessarily holds the GIL to create Python objects. PyO3 conversion errors are
propagated unchanged, whereas malformed TL bytes use `ValueError`. Descriptor indices and flag
bits come from trusted generated metadata and are not revalidated on every hot-path call.

# Arguments

- `py`: The acquired GIL token used to construct decoded Python values.
- `constructor_id`: Generated TL constructor id selecting a trusted fast-path descriptor.
- `data`: TL wire bytes to decode.
- `offset`: Byte offset at which this constructor begins.
- `boxed`: Whether `data` starts with and must match the constructor id.
