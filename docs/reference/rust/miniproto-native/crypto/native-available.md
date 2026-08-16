---
title: "miniproto_native::crypto::native_available"
description: "Implements Python `native_available`, which always returns `true` while this compiled callable"
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::native_available"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L88"
aliases: ["miniproto._native.native_available"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L88)
- Python exposure: `miniproto._native.native_available` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn native_available() -> bool
```

## cargo-docs-md rendering

### `native_available`

```rust
fn native_available() -> bool
```

*Defined in `rust\miniproto\src\crypto.rs:88-90`*

Implements Python `native_available`, which always returns `true` while this compiled callable
is importable. Python fallback selection happens before this function can be called.
