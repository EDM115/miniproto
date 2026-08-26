---
title: "miniproto.connection.framing"
description: "Stateful MTProto TCP transport framing."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.connection.framing"
source_path: "src/miniproto/connection/framing.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/framing.py"
module: "miniproto.connection.framing"
---

## `miniproto.connection.framing`

Stateful MTProto TCP transport framing.

The codec is deliberately independent from sockets: callers may feed arbitrary
fragments and every complete frame is drained before another read is needed.

## Public objects

- [`PayloadFrame`](./payloadframe/) — A decoded MTProto transport payload.
- [`QuickAckFrame`](./quickackframe/) — A transport-level quick acknowledgement emitted by Telegram.
- [`TransportErrorFrame`](./transporterrorframe/) — A negative MTProto transport error code decoded from a frame.
- [`FrameEvent`](./frameevent/) — Public attribute `miniproto.connection.framing.FrameEvent`.
- [`TransportFrameCodec`](./transportframecodec/) — Incrementally encode and decode one MTProto TCP framing mode.
- [`PythonFrameCodec`](./pythonframecodec/) — Pure-Python incremental encoder/decoder for Telegram TCP transports.
- [`NativeFrameCodec`](./nativeframecodec/) — Typed adapter around the bundled Rust frame pump.
- [`native_transport_available`](./native-transport-available/) — Return whether the imported native module exposes ``TransportCodec``.
- [`create_frame_codec`](./create-frame-codec/) — Create the fastest available codec for one MTProto TCP framing mode.
