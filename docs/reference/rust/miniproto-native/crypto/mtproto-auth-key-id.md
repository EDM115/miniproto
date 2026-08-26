---
title: "miniproto_native::crypto::mtproto_auth_key_id"
description: "Computes Python `mtproto_auth_key_id(auth_key)` from a validated 256-byte key."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::mtproto_auth_key_id"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L131"
aliases: ["miniproto._native.mtproto_auth_key_id"]
python_visible: true
---

## Provenance

- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L131)
- Python exposure: `miniproto._native.mtproto_auth_key_id` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn mtproto_auth_key_id(auth_key: &[u8]) -> _
```

## Arguments

- `auth_key`: The 256-byte MTProto authorization key.

## cargo-docs-md rendering

### `mtproto_auth_key_id`

```rust
fn mtproto_auth_key_id(auth_key: &[u8]) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:131-133`*

Computes Python `mtproto_auth_key_id(auth_key)` from a validated 256-byte key.

Returns `ValueError` when `auth_key` has the wrong length.

# Arguments

- `auth_key`: The 256-byte MTProto authorization key.
