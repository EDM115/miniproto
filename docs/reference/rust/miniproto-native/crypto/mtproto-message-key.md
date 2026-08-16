---
title: "miniproto_native::crypto::mtproto_message_key"
description: "Computes Python `mtproto_message_key` for padded plaintext and one MTProto direction."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::mtproto_message_key"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L142"
aliases: ["miniproto._native.mtproto_message_key"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L142)
- Python exposure: `miniproto._native.mtproto_message_key` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn mtproto_message_key(py: _, auth_key: _, plaintext_with_padding: _, client_to_server: bool) -> _
```

## Arguments

- `py`: The acquired GIL token used to detach a large hash operation.
- `auth_key`: The 256-byte MTProto authorization key.
- `plaintext_with_padding`: Block-aligned inner plaintext that contributes to the message key.
- `client_to_server`: Selects the directional MTProto key offset.

## cargo-docs-md rendering

### `mtproto_message_key`

```rust
fn mtproto_message_key(py: Python<'_>, auth_key: Vec<u8>, plaintext_with_padding: Vec<u8>, client_to_server: bool) -> PyResult<Vec<u8>>
```

*Defined in `rust\miniproto\src\crypto.rs:142-157`*

Computes Python `mtproto_message_key` for padded plaintext and one MTProto direction.

Returns a 16-byte message key; rejects an invalid authorization key and releases the GIL for
large inputs.

# Arguments

- `py`: The acquired GIL token used to detach a large hash operation.
- `auth_key`: The 256-byte MTProto authorization key.
- `plaintext_with_padding`: Block-aligned inner plaintext that contributes to the message key.
- `client_to_server`: Selects the directional MTProto key offset.
