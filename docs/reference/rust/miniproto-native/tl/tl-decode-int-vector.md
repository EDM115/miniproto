---
title: "miniproto_native::tl::tl_decode_int_vector"
description: "Decodes Python `tl_decode_int_vector(data, offset)` into values and a next offset."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_decode_int_vector"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L714"
aliases: ["miniproto._native.tl_decode_int_vector"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L714)
- Python exposure: `miniproto._native.tl_decode_int_vector` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_decode_int_vector(py: _, data: _, offset: i128) -> _
```

## Arguments

- `py`: The acquired GIL token used to detach large vector decoding.
- `data`: TL bytes containing a generic integer vector.
- `offset`: Python-facing signed byte offset that must convert to `usize`.

## cargo-docs-md rendering

### `tl_decode_int_vector`

```rust
fn tl_decode_int_vector(py: Python<'_>, data: Vec<u8>, offset: i128) -> PyResult<(Vec<i32>, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:714-722`*

Decodes Python `tl_decode_int_vector(data, offset)` into values and a next offset.

The signed Python offset must fit `usize`; large decoding releases the GIL and malformed input
returns a Python exception.

# Arguments

- `py`: The acquired GIL token used to detach large vector decoding.
- `data`: TL bytes containing a generic integer vector.
- `offset`: Python-facing signed byte offset that must convert to `usize`.
