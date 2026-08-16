---
title: "miniproto_native::tl::tl_encode_long"
description: "Encodes Python `tl_encode_long(value)` as an eight-byte little-endian signed integer."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_encode_long"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L548"
aliases: ["miniproto._native.tl_encode_long"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L548)
- Python exposure: `miniproto._native.tl_encode_long` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_encode_long(value: i64) -> _
```

## Arguments

- `value`: Signed 64-bit integer to serialize.

## cargo-docs-md rendering

### `tl_encode_long`

```rust
fn tl_encode_long(value: i64) -> Vec<u8>
```

*Defined in `rust\miniproto\src\tl.rs:548-550`*

Encodes Python `tl_encode_long(value)` as an eight-byte little-endian signed integer.

# Arguments

- `value`: Signed 64-bit integer to serialize.
