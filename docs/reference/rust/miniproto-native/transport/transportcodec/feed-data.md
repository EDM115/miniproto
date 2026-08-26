---
title: "miniproto_native::transport::TransportCodec::feed_data"
description: "Feeds Python `feed_data(data)` and returns tagged native event tuples."
generated: true
editUrl: false
language: "rust"
kind: "method"
qualified_name: "miniproto_native::transport::TransportCodec::feed_data"
source_path: "rust/miniproto/src/transport.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs#L187"
aliases: ["miniproto._native.TransportCodec.feed_data"]
python_visible: true
---

## Provenance

- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/transport.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs#L187)
- Python exposure: `miniproto._native.TransportCodec.feed_data` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn feed_data(self: &mut Self, data: &[u8]) -> _
```

## Arguments

- `data`: Newly received TCP bytes to append to this codec's buffered stream.

## cargo-docs-md rendering

- <span id="transportcodec-feed-data"></span>`fn feed_data(&mut self, data: &[u8]) -> PyResult<Vec<(u8, Vec<u8>, i64, bool)>>`

  Feeds Python `feed_data(data)` and returns tagged native event tuples.

  

  Tuple kinds are `0` payload, `1` quick ACK and `2` negative transport error. It preserves

  incomplete trailing bytes for the next call and raises Python errors for invalid framing.

  

  # Arguments

  

  - `data`: Newly received TCP bytes to append to this codec's buffered stream.
