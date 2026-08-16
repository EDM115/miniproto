---
title: "miniproto_native::tl::tl_encode_double"
description: "Encodes Python `tl_encode_double(value)` as eight IEEE-754 little-endian bytes."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_encode_double"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L624"
aliases: ["miniproto._native.tl_encode_double"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L624)
- Python exposure: `miniproto._native.tl_encode_double` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_encode_double(value: f64) -> _
```

## Arguments

- `value`: Double-precision value to serialize.

## cargo-docs-md rendering

### `tl_encode_double`

```rust
fn tl_encode_double(value: f64) -> Vec<u8>
```

*Defined in `rust\miniproto\src\tl.rs:624-626`*

Encodes Python `tl_encode_double(value)` as eight IEEE-754 little-endian bytes.

# Arguments

- `value`: Double-precision value to serialize.
