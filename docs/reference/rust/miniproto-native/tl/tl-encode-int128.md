---
title: "miniproto_native::tl::tl_encode_int128"
description: "Encodes Python `tl_encode_int128(value)` to 16 little-endian bytes via `int.to_bytes`."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_encode_int128"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L572"
aliases: ["miniproto._native.tl_encode_int128"]
python_visible: true
---

## Provenance

- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L572)
- Python exposure: `miniproto._native.tl_encode_int128` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_encode_int128(value: &_) -> _
```

## Arguments

- `value`: Python integer to convert to exactly 16 little-endian bytes.

## cargo-docs-md rendering

### `tl_encode_int128`

```rust
fn tl_encode_int128(value: &Bound<'_, PyAny>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/tl.rs:572-574`*

Encodes Python `tl_encode_int128(value)` to 16 little-endian bytes via `int.to_bytes`.

Python raises if `value` cannot fit the requested unsigned representation.

# Arguments

- `value`: Python integer to convert to exactly 16 little-endian bytes.
