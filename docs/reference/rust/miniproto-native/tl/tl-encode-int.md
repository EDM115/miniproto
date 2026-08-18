---
title: "miniproto_native::tl::tl_encode_int"
description: "Encodes Python `tl_encode_int(value)` as a four-byte little-endian signed integer."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_encode_int"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L504"
aliases: ["miniproto._native.tl_encode_int"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L504)
- Python exposure: `miniproto._native.tl_encode_int` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_encode_int(value: i32) -> _
```

## Arguments

- `value`: Signed 32-bit integer to serialize.

## cargo-docs-md rendering

### `tl_encode_int`

```rust
fn tl_encode_int(value: i32) -> Vec<u8>
```

*Defined in `rust/miniproto/src/tl.rs:504-506`*

Encodes Python `tl_encode_int(value)` as a four-byte little-endian signed integer.

# Arguments

- `value`: Signed 32-bit integer to serialize.
