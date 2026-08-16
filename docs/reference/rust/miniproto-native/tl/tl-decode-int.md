---
title: "miniproto_native::tl::tl_decode_int"
description: "Decodes Python `tl_decode_int(data, offset)` and returns `(value, next_offset)` or `ValueError`."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_decode_int"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L515"
aliases: ["miniproto._native.tl_decode_int"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L515)
- Python exposure: `miniproto._native.tl_decode_int` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_decode_int(data: &[u8], offset: usize) -> _
```

## Arguments

- `data`: TL bytes containing a four-byte signed integer.
- `offset`: Byte offset at which the integer starts.

## cargo-docs-md rendering

### `tl_decode_int`

```rust
fn tl_decode_int(data: &[u8], offset: usize) -> PyResult<(i32, usize)>
```

*Defined in `rust\miniproto\src\tl.rs:515-518`*

Decodes Python `tl_decode_int(data, offset)` and returns `(value, next_offset)` or `ValueError`.

# Arguments

- `data`: TL bytes containing a four-byte signed integer.
- `offset`: Byte offset at which the integer starts.
