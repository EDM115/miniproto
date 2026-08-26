---
title: "miniproto_native::tl::tl_encode_uint"
description: "Encodes Python `tl_encode_uint(value)` as a four-byte little-endian unsigned integer."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_encode_uint"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L526"
aliases: ["miniproto._native.tl_encode_uint"]
python_visible: true
---

## Provenance

- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L526)
- Python exposure: `miniproto._native.tl_encode_uint` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_encode_uint(value: u32) -> _
```

## Arguments

- `value`: Unsigned 32-bit integer to serialize.

## cargo-docs-md rendering

### `tl_encode_uint`

```rust
fn tl_encode_uint(value: u32) -> Vec<u8>
```

*Defined in `rust/miniproto/src/tl.rs:526-528`*

Encodes Python `tl_encode_uint(value)` as a four-byte little-endian unsigned integer.

# Arguments

- `value`: Unsigned 32-bit integer to serialize.
