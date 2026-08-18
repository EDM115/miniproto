---
title: "miniproto_native::tl::tl_decode_string"
description: "Decodes Python `tl_decode_string(data, offset)` as UTF-8 and returns it with the next offset."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_decode_string"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L682"
aliases: ["miniproto._native.tl_decode_string"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L682)
- Python exposure: `miniproto._native.tl_decode_string` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_decode_string(data: &[u8], offset: usize) -> _
```

## Arguments

- `data`: TL bytes containing one length-prefixed string field.
- `offset`: Byte offset at which the field starts.

## cargo-docs-md rendering

### `tl_decode_string`

```rust
fn tl_decode_string(data: &[u8], offset: usize) -> PyResult<(String, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:682-687`*

Decodes Python `tl_decode_string(data, offset)` as UTF-8 and returns it with the next offset.

Returns `ValueError` for malformed TL data or non-UTF-8 payload bytes.

# Arguments

- `data`: TL bytes containing one length-prefixed string field.
- `offset`: Byte offset at which the field starts.
