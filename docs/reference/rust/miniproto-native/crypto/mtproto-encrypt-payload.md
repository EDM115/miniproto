---
title: "miniproto_native::crypto::mtproto_encrypt_payload"
description: "Encrypts padded MTProto plaintext for Python `mtproto_encrypt_payload`."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::mtproto_encrypt_payload"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L202"
aliases: ["miniproto._native.mtproto_encrypt_payload"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L202)
- Python exposure: `miniproto._native.mtproto_encrypt_payload` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn mtproto_encrypt_payload(py: _, auth_key: _, plaintext_with_padding: _, client_to_server: bool) -> _
```

## Arguments

- `py`: The acquired GIL token used to detach large encryption work.
- `auth_key`: The 256-byte MTProto authorization key.
- `plaintext_with_padding`: AES-block-aligned inner plaintext to encrypt.
- `client_to_server`: Selects the directional MTProto key schedule.

## cargo-docs-md rendering

### `mtproto_encrypt_payload`

```rust
fn mtproto_encrypt_payload(py: Python<'_>, auth_key: Vec<u8>, plaintext_with_padding: Vec<u8>, client_to_server: bool) -> PyResult<(Vec<u8>, Vec<u8>, Vec<u8>)>
```

*Defined in `rust/miniproto/src/crypto.rs:202-212`*

Encrypts padded MTProto plaintext for Python `mtproto_encrypt_payload`.

Returns `(auth_key_id, msg_key, ciphertext)` or `ValueError` for invalid key or block input;
large work runs without the GIL.

# Arguments

- `py`: The acquired GIL token used to detach large encryption work.
- `auth_key`: The 256-byte MTProto authorization key.
- `plaintext_with_padding`: AES-block-aligned inner plaintext to encrypt.
- `client_to_server`: Selects the directional MTProto key schedule.
