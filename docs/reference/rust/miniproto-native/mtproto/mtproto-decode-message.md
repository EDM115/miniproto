---
title: "miniproto_native::mtproto::mtproto_decode_message"
description: "Decodes Python `mtproto_decode_message` packet bytes into its seven-element envelope tuple."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::mtproto::mtproto_decode_message"
source_path: "rust/miniproto/src/mtproto.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/mtproto.rs#L154"
aliases: ["miniproto._native.mtproto_decode_message"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/mtproto.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/mtproto.rs#L154)
- Python exposure: `miniproto._native.mtproto_decode_message` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn mtproto_decode_message(py: _, auth_key: _, packet: _, client_to_server: bool) -> _
```

## Arguments

- `py`: The acquired GIL token used only to detach large native work.
- `auth_key`: The 256-byte authorization key used to verify and decrypt `packet`.
- `packet`: Full encrypted MTProto packet including auth-key id and message key.
- `client_to_server`: Selects the directional MTProto key schedule used for verification.

## cargo-docs-md rendering

### `mtproto_decode_message`

```rust
fn mtproto_decode_message(py: Python<'_>, auth_key: Vec<u8>, packet: Vec<u8>, client_to_server: bool) -> PyResult<(Vec<u8>, u64, u64, i64, i32, Vec<u8>, Vec<u8>)>
```

*Defined in `rust\miniproto\src\mtproto.rs:154-173`*

Decodes Python `mtproto_decode_message` packet bytes into its seven-element envelope tuple.

`client_to_server` selects the direction used to verify and decrypt `packet`.  Returns
`(auth_key_id, server_salt, session_id, msg_id, seq_no, body, padding)`, or `ValueError` if
the wire packet, keys, body length, message key, or padding is invalid.  Large workloads run
with the GIL released.

# Arguments

- `py`: The acquired GIL token used only to detach large native work.
- `auth_key`: The 256-byte authorization key used to verify and decrypt `packet`.
- `packet`: Full encrypted MTProto packet including auth-key id and message key.
- `client_to_server`: Selects the directional MTProto key schedule used for verification.
