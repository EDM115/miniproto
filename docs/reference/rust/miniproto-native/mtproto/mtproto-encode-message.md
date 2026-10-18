---
title: "miniproto_native::mtproto::mtproto_encode_message"
description: "Encodes one encrypted MTProto envelope as Python `mtproto_encode_message`."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::mtproto::mtproto_encode_message"
source_path: "rust/miniproto/src/mtproto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/mtproto.rs#L106"
aliases: ["miniproto._native.mtproto_encode_message"]
python_visible: true
---

## Provenance

- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/mtproto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/mtproto.rs#L106)
- Python exposure: `miniproto._native.mtproto_encode_message` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn mtproto_encode_message(py: _, auth_key: _, server_salt: u64, session_id: u64, msg_id: i64, seq_no: i32, body: _, client_to_server: bool, padding: _) -> _
```

## Arguments

- `py`: The acquired GIL token used only to detach large native work.
- `auth_key`: The 256-byte authorization key used to encrypt, but not serialize, the envelope.
- `server_salt`: The salt serialized at the start of the inner envelope.
- `session_id`: The session identifier serialized in the inner envelope.
- `msg_id`: The MTProto message identifier serialized in the inner envelope.
- `seq_no`: The MTProto sequence number serialized in the inner envelope.
- `body`: Four-byte-aligned application bytes serialized before the padding.
- `client_to_server`: Selects the directional MTProto key schedule.
- `padding`: Optional explicit padding; `None` requests operating-system random padding.

## cargo-docs-md rendering

### `mtproto_encode_message`

```rust
fn mtproto_encode_message(py: Python<'_>, auth_key: Vec<u8>, server_salt: u64, session_id: u64, msg_id: i64, seq_no: i32, body: Vec<u8>, client_to_server: bool, padding: Option<Vec<u8>>) -> PyResult<Vec<u8>>
```

*Defined in `rust/miniproto/src/mtproto.rs:106-130`*

Encodes one encrypted MTProto envelope as Python `mtproto_encode_message`.

Serializes the salt, session ID, message ID, sequence number, body length, body and padding, then encrypts them with `auth_key`. Returns the auth-key ID, message key and ciphertext in wire order. `client_to_server` selects the key schedule, and explicit `padding` replaces generated randomness. Invalid key, body or padding values raise `ValueError`, while integer conversion errors propagate from PyO3. Large workloads detach from Python.

# Arguments

- `py`: The acquired GIL token used only to detach large native work.
- `auth_key`: The 256-byte authorization key used to encrypt, but not serialize, the envelope.
- `server_salt`: The salt serialized at the start of the inner envelope.
- `session_id`: The session identifier serialized in the inner envelope.
- `msg_id`: The MTProto message identifier serialized in the inner envelope.
- `seq_no`: The MTProto sequence number serialized in the inner envelope.
- `body`: Four-byte-aligned application bytes serialized before the padding.
- `client_to_server`: Selects the directional MTProto key schedule.
- `padding`: Optional explicit padding; `None` requests operating-system random padding.
