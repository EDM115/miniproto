---
title: "miniproto_native::tl::tl_encode_bytes"
description: "Encodes Python `tl_encode_bytes(value)` with TL's short/long length prefix and zero padding."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_encode_bytes"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L646"
aliases: ["miniproto._native.tl_encode_bytes"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L646)
- Python exposure: `miniproto._native.tl_encode_bytes` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_encode_bytes(value: &[u8]) -> _
```

## Arguments

- `value`: Bytes to prefix and pad according to TL rules.

## cargo-docs-md rendering

### `tl_encode_bytes`

```rust
fn tl_encode_bytes(value: &[u8]) -> Vec<u8>
```

*Defined in `rust/miniproto/src/tl.rs:646-648`*

Encodes Python `tl_encode_bytes(value)` with TL's short/long length prefix and zero padding.

# Arguments

- `value`: Bytes to prefix and pad according to TL rules.
