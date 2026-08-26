---
title: "miniproto_native::tl::tl_encode_string"
description: "Encodes Python `tl_encode_string(value)` as UTF-8 TL bytes."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_encode_string"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L669"
aliases: ["miniproto._native.tl_encode_string"]
python_visible: true
---

## Provenance

- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L669)
- Python exposure: `miniproto._native.tl_encode_string` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_encode_string(value: &str) -> _
```

## Arguments

- `value`: UTF-8 Rust string to encode as TL bytes.

## cargo-docs-md rendering

### `tl_encode_string`

```rust
fn tl_encode_string(value: &str) -> Vec<u8>
```

*Defined in `rust/miniproto/src/tl.rs:669-671`*

Encodes Python `tl_encode_string(value)` as UTF-8 TL bytes.

# Arguments

- `value`: UTF-8 Rust string to encode as TL bytes.
