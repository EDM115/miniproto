---
title: "miniproto_native::tl::tl_encode_int256"
description: "Encodes Python `tl_encode_int256(value)` to 32 little-endian bytes via `int.to_bytes`."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_encode_int256"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L599"
aliases: ["miniproto._native.tl_encode_int256"]
python_visible: true
---

## Provenance

- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L599)
- Python exposure: `miniproto._native.tl_encode_int256` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_encode_int256(value: &_) -> _
```

## Arguments

- `value`: Python integer to convert to exactly 32 little-endian bytes.

## cargo-docs-md rendering

### `tl_encode_int256`

```rust
fn tl_encode_int256(value: &Bound<'_, PyAny>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/tl.rs:599-601`*

Encodes Python `tl_encode_int256(value)` to 32 little-endian bytes via `int.to_bytes`.

Python raises if `value` cannot fit the requested unsigned representation.

# Arguments

- `value`: Python integer to convert to exactly 32 little-endian bytes.
