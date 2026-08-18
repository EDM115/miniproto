---
title: "miniproto_native::tl::tl_fast_encode"
description: "Attempts Python `tl_fast_encode` for a generated constructor."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_fast_encode"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L143"
aliases: ["miniproto._native.tl_fast_encode"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L143)
- Python exposure: `miniproto._native.tl_fast_encode` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_fast_encode(constructor_id: u32, values: &_, boxed: bool) -> _
```

## Arguments

- `constructor_id`: Generated TL constructor id selecting a trusted fast-path descriptor.
- `values`: Python tuple whose exact arity and value types must match that descriptor.
- `boxed`: Whether to serialize the constructor id before its fields.

## cargo-docs-md rendering

### `tl_fast_encode`

```rust
fn tl_fast_encode(constructor_id: u32, values: &Bound<'_, pyo3::types::PyTuple>, boxed: bool) -> PyResult<Option<Vec<u8>>>
```

*Defined in `rust/miniproto/src/tl.rs:143-191`*

Attempts Python `tl_fast_encode` for a generated constructor.

`values` must have the generated constructor's exact tuple arity; `boxed` controls whether the
constructor id is emitted. Returns `None` if no native encoder exists, encoded bytes on
success, or a Python exception for incompatible values or generated metadata. PyO3 conversion
failures from tuple lookup/extraction propagate as `TypeError`, `OverflowError`, or the source
Python exception; algorithm and descriptor validation failures intentionally use `ValueError`.

# Arguments

- `constructor_id`: Generated TL constructor id selecting a trusted fast-path descriptor.
- `values`: Python tuple whose exact arity and value types must match that descriptor.
- `boxed`: Whether to serialize the constructor id before its fields.
