---
title: "miniproto_native::crypto::mtproto_derive_aes_key_iv"
description: "Derives the AES-256 key and IV used by Python `mtproto_derive_aes_key_iv`."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::mtproto_derive_aes_key_iv"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L172"
aliases: ["miniproto._native.mtproto_derive_aes_key_iv"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L172)
- Python exposure: `miniproto._native.mtproto_derive_aes_key_iv` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn mtproto_derive_aes_key_iv(py: _, auth_key: _, msg_key: _, client_to_server: bool) -> _
```

## Arguments

- `py`: The acquired GIL token retained by this bounded-size operation.
- `auth_key`: The 256-byte MTProto authorization key.
- `msg_key`: The 16-byte MTProto message key.
- `client_to_server`: Selects the directional MTProto key offset.

## cargo-docs-md rendering

### `mtproto_derive_aes_key_iv`

```rust
fn mtproto_derive_aes_key_iv(py: Python<'_>, auth_key: Vec<u8>, msg_key: Vec<u8>, client_to_server: bool) -> PyResult<(Vec<u8>, Vec<u8>)>
```

*Defined in `rust\miniproto\src\crypto.rs:172-188`*

Derives the AES-256 key and IV used by Python `mtproto_derive_aes_key_iv`.

Returns `(key, iv)` and validates both fixed-width inputs. Valid inputs total 272 bytes
(`auth_key` 256 plus `msg_key` 16), so this wrapper never exceeds the detach threshold and
performs the derivation while holding the GIL.

# Arguments

- `py`: The acquired GIL token retained by this bounded-size operation.
- `auth_key`: The 256-byte MTProto authorization key.
- `msg_key`: The 16-byte MTProto message key.
- `client_to_server`: Selects the directional MTProto key offset.
