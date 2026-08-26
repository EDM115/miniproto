---
title: "miniproto_native::transport::TransportCodec::feed_transport_data"
description: "Feeds compatibility `feed_transport_data(data)` and returns bytes or integer Python events."
generated: true
editUrl: false
language: "rust"
kind: "method"
qualified_name: "miniproto_native::transport::TransportCodec::feed_transport_data"
source_path: "rust/miniproto/src/transport.rs"
source_url: "https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs#L212"
aliases: ["miniproto._native.TransportCodec.feed_transport_data"]
python_visible: true
---

## Provenance

- Rust visibility: `restricted`
- Source: [`rust/miniproto/src/transport.rs`](https://github.com/EDM115/miniproto/blob/master/rust/miniproto/src/transport.rs#L212)
- Python exposure: `miniproto._native.TransportCodec.feed_transport_data` (confirmed from adjacent PyO3 attributes)

## Signature

```rust
fn feed_transport_data(self: &mut Self, py: _, data: &[u8]) -> _
```

## Arguments

- `py`: The acquired GIL token used to build Python `bytes` and integer events.
- `data`: Newly received TCP bytes to append to this codec's buffered stream.

## cargo-docs-md rendering

- <span id="transportcodec-feed-transport-data"></span>`fn feed_transport_data(&mut self, py: Python<'_>, data: &[u8]) -> PyResult<Vec<Py<PyAny>>>`

  Feeds compatibility `feed_transport_data(data)` and returns bytes or integer Python events.

  

  The GIL token is used only for object conversion after native parsing; malformed framing

  returns a Python exception.

  

  # Arguments

  

  - `py`: The acquired GIL token used to build Python `bytes` and integer events.

  - `data`: Newly received TCP bytes to append to this codec's buffered stream.
