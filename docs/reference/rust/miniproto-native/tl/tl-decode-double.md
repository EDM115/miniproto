---
title: "miniproto_native::tl::tl_decode_double"
description: "Decodes Python `tl_decode_double(data, offset)` and returns `(value, next_offset)` or `ValueError`."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_decode_double"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L635"
aliases: ["miniproto._native.tl_decode_double"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L635)
- Python exposure: `miniproto._native.tl_decode_double` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_decode_double(data: &[u8], offset: usize) -> _
```

## Arguments

- `data`: TL bytes containing an eight-byte double.
- `offset`: Byte offset at which the double starts.

## cargo-docs-md rendering

### `tl_decode_double`

```rust
fn tl_decode_double(data: &[u8], offset: usize) -> PyResult<(f64, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:635-638`*

Decodes Python `tl_decode_double(data, offset)` and returns `(value, next_offset)` or `ValueError`.

# Arguments

- `data`: TL bytes containing an eight-byte double.
- `offset`: Byte offset at which the double starts.
