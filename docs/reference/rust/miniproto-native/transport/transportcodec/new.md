---
title: "miniproto_native::transport::TransportCodec::new"
description: "Creates `TransportCodec(mode, max_payload_size, server_side=False)`."
generated: true
editUrl: false
language: "rust"
kind: "method"
qualified_name: "miniproto_native::transport::TransportCodec::new"
source_path: "rust/miniproto/src/transport.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs#L152"
aliases: ["miniproto._native.TransportCodec"]
python_visible: true
---

## Provenance

- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/transport.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs#L152)
- Python exposure: `miniproto._native.TransportCodec` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn new(mode: &str, max_payload_size: usize, server_side: bool) -> _
```

## Arguments

- `mode`: One of the supported Python TCP mode names.
- `max_payload_size`: Positive upper bound for decoded application payload bytes.
- `server_side`: Whether inbound quick-ACK request bits remain payload metadata instead of being interpreted as quick-ACK response frames.

## cargo-docs-md rendering

- <span id="transportcodec-new"></span>`fn new(mode: &str, max_payload_size: usize, server_side: bool) -> PyResult<Self>`

  Creates `TransportCodec(mode, max_payload_size, server_side=False)`.

  

  An unsupported `mode` or zero payload bound raises `ValueError`. A negative bound or one larger than `usize` raises `OverflowError` during PyO3 conversion.

  

  # Arguments

  

  - `mode`: One of the supported Python TCP mode names.

  - `max_payload_size`: Positive upper bound for decoded application payload bytes.

  - `server_side`: Whether inbound quick-ACK request bits remain payload metadata instead of

    being interpreted as quick-ACK response frames.
