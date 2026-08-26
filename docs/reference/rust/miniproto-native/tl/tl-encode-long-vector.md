---
title: "miniproto_native::tl::tl_encode_long_vector"
description: "Encodes Python `tl_encode_long_vector(values)` as a generic TL vector of 64-bit integers."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_encode_long_vector"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L733"
aliases: ["miniproto._native.tl_encode_long_vector"]
python_visible: true
---

## Provenance

- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L733)
- Python exposure: `miniproto._native.tl_encode_long_vector` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_encode_long_vector(py: _, values: _) -> _
```

## Arguments

- `py`: The acquired GIL token used to detach large vector encoding.
- `values`: Signed 64-bit values to serialize.

## cargo-docs-md rendering

### `tl_encode_long_vector`

```rust
fn tl_encode_long_vector(py: Python<'_>, values: Vec<i64>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/tl.rs:733-736`*

Encodes Python `tl_encode_long_vector(values)` as a generic TL vector of 64-bit integers.

Large vector encoding releases the GIL; invalid size or allocation raises a Python exception.

# Arguments

- `py`: The acquired GIL token used to detach large vector encoding.
- `values`: Signed 64-bit values to serialize.
