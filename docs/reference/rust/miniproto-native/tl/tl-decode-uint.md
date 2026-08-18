---
title: "miniproto_native::tl::tl_decode_uint"
description: "Decodes Python `tl_decode_uint(data, offset)` and returns `(value, next_offset)` or `ValueError`."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::tl::tl_decode_uint"
source_path: "rust/miniproto/src/tl.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L537"
aliases: ["miniproto._native.tl_decode_uint"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/tl.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/tl.rs#L537)
- Python exposure: `miniproto._native.tl_decode_uint` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn tl_decode_uint(data: &[u8], offset: usize) -> _
```

## Arguments

- `data`: TL bytes containing a four-byte unsigned integer.
- `offset`: Byte offset at which the integer starts.

## cargo-docs-md rendering

### `tl_decode_uint`

```rust
fn tl_decode_uint(data: &[u8], offset: usize) -> PyResult<(u32, usize)>
```

*Defined in `rust/miniproto/src/tl.rs:537-540`*

Decodes Python `tl_decode_uint(data, offset)` and returns `(value, next_offset)` or `ValueError`.

# Arguments

- `data`: TL bytes containing a four-byte unsigned integer.
- `offset`: Byte offset at which the integer starts.
