---
title: "miniproto_native::transport::quick_ack_token"
description: "Computes the flagged quick-ACK token for Python `quick_ack_token`."
generated: true
editUrl: false
language: "rust"
kind: "function"
qualified_name: "miniproto_native::transport::quick_ack_token"
source_path: "rust/miniproto/src/transport.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs#L55"
aliases: ["miniproto._native.quick_ack_token"]
crate: "miniproto_native"
python_visible: true
---

## Provenance

- Crate: `miniproto_native`
- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/transport.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs#L55)
- Python exposure: `miniproto._native.quick_ack_token` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn quick_ack_token(auth_key: &[u8], encrypted_packet: &[u8]) -> _
```

## Arguments

- `auth_key`: 256-byte MTProto authorization key used by the quick-ACK hash schedule.
- `encrypted_packet`: Full MTProto packet whose nonempty encrypted suffix is hashed.

## cargo-docs-md rendering

### `quick_ack_token`

```rust
fn quick_ack_token(auth_key: &[u8], encrypted_packet: &[u8]) -> PyResult<u32>
```

*Defined in `rust\miniproto\src\transport.rs:55-68`*

Computes the flagged quick-ACK token for Python `quick_ack_token`.

The 256-byte `auth_key` and nonempty encrypted portion of `encrypted_packet` are validated.
Returns the token with the quick-ACK bit set or `ValueError` for invalid packet/key input.

# Arguments

- `auth_key`: 256-byte MTProto authorization key used by the quick-ACK hash schedule.
- `encrypted_packet`: Full MTProto packet whose nonempty encrypted suffix is hashed.
