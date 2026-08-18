---
title: "miniproto_native::crypto::mtproto_decrypt_payload"
description: "Decrypts and verifies Python `mtproto_decrypt_payload` ciphertext."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::crypto::mtproto_decrypt_payload"
source_path: "rust/miniproto/src/crypto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L227"
aliases: ["miniproto._native.mtproto_decrypt_payload"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/crypto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/crypto.rs#L227)
- Python exposure: `miniproto._native.mtproto_decrypt_payload` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn mtproto_decrypt_payload(py: _, auth_key: _, msg_key: _, ciphertext: _, client_to_server: bool) -> _
```

## Arguments

- `py`: The acquired GIL token used to detach large decryption work.
- `auth_key`: The 256-byte MTProto authorization key.
- `msg_key`: The 16-byte message key to verify.
- `ciphertext`: AES-IGE ciphertext whose length must be an AES-block multiple.
- `client_to_server`: Selects the directional MTProto key schedule.

## cargo-docs-md rendering

### `mtproto_decrypt_payload`

```rust
fn mtproto_decrypt_payload(py: Python<'_>, auth_key: Vec<u8>, msg_key: Vec<u8>, ciphertext: Vec<u8>, client_to_server: bool) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/crypto.rs:227-238`*

Decrypts and verifies Python `mtproto_decrypt_payload` ciphertext.

Returns padded plaintext or `ValueError` for invalid lengths, key material, or message-key
verification; large work runs without the GIL.

# Arguments

- `py`: The acquired GIL token used to detach large decryption work.
- `auth_key`: The 256-byte MTProto authorization key.
- `msg_key`: The 16-byte message key to verify.
- `ciphertext`: AES-IGE ciphertext whose length must be an AES-block multiple.
- `client_to_server`: Selects the directional MTProto key schedule.
