---
title: "miniproto_native::transport::TransportCodec::encode_packet"
description: "Encodes Python `encode_packet(payload, quick_ack=False)` into a single TCP frame."
generated: true
editUrl: false
language: "rust"
kind: "method"
qualified_name: "miniproto_native::transport::TransportCodec::encode_packet"
source_path: "rust/miniproto/src/transport.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs#L175"
aliases: ["miniproto._native.TransportCodec.encode_packet"]
python_visible: true
---

## Provenance

- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/transport.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs#L175)
- Python exposure: `miniproto._native.TransportCodec.encode_packet` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn encode_packet(self: &Self, payload: &[u8], quick_ack: bool) -> _
```

## Arguments

- `payload`: Complete MTProto payload to frame.
- `quick_ack`: Whether to set the outbound quick-ACK request bit where the mode supports it.

## cargo-docs-md rendering

- <span id="transportcodec-encode-packet"></span>`fn encode_packet(&self, payload: &[u8], quick_ack: bool) -> PyResult<Vec<u8>>`

  Encodes Python `encode_packet(payload, quick_ack=False)` into a single TCP frame.

  

  Returns `ValueError` for oversized payloads, invalid abridged alignment, length overflow,

  or operating-system randomness failure in padded mode.

  

  # Arguments

  

  - `payload`: Complete MTProto payload to frame.

  - `quick_ack`: Whether to set the outbound quick-ACK request bit where the mode supports it.
