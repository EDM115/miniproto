---
title: "miniproto_native::crypto::xor_bytes"
description: "Returns the bytewise exclusive-or of Python `xor_bytes(left, right)` inputs."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::xor_bytes"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L254"
aliases: ["miniproto._native.xor_bytes"]
python_visible: true
---

## Provenance

- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L254)
- Python exposure: `miniproto._native.xor_bytes` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn xor_bytes(left: &[u8], right: &[u8]) -> _
```

## Arguments

- `left`: First equal-length byte sequence.
- `right`: Second equal-length byte sequence.

## cargo-docs-md rendering

### `xor_bytes`

```rust
fn xor_bytes(left: &[u8], right: &[u8]) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:254-256`*

Returns the bytewise exclusive-or of Python `xor_bytes(left, right)` inputs.

Returns `ValueError` unless both inputs have equal length.

# Arguments

- `left`: First equal-length byte sequence.
- `right`: Second equal-length byte sequence.
