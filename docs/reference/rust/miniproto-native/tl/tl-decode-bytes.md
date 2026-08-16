---
title: "miniproto_native::tl::tl_decode_bytes"
description: "Decodes Python `tl_decode_bytes(data, offset)` and returns bytes plus the next aligned offset."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_decode_bytes"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L659"
aliases: ["miniproto._native.tl_decode_bytes"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L659)
- Python exposure: `miniproto._native.tl_decode_bytes` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_decode_bytes(data: &[u8], offset: usize) -> _
```

## Arguments

- `data`: TL bytes containing one length-prefixed byte field.
- `offset`: Byte offset at which the field starts.

## cargo-docs-md rendering

### `tl_decode_bytes`

```rust
fn tl_decode_bytes(data: &[u8], offset: usize) -> PyResult<(Vec<u8>, usize)>
```

*Defined in `rust\miniproto\src\tl.rs:659-661`*

Decodes Python `tl_decode_bytes(data, offset)` and returns bytes plus the next aligned offset.

Returns `ValueError` for malformed or truncated TL data.

# Arguments

- `data`: TL bytes containing one length-prefixed byte field.
- `offset`: Byte offset at which the field starts.
