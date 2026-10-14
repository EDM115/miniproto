---
title: "miniproto.connection.framing.NativeFrameCodec"
description: "Typed adapter around the bundled Rust frame pump."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.connection.framing.NativeFrameCodec"
source_path: "src/miniproto/connection/framing.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/framing.py#L402"
module: "miniproto.connection.framing"
---

## `miniproto.connection.framing.NativeFrameCodec`

```python
NativeFrameCodec(mode: TransportMode | str, *, max_payload_size: int, server_side: bool = False) -> None
```

Typed adapter around the bundled Rust frame pump.

Create a typed adapter around the installed native codec.

**Parameters:**

- **mode** (<code>[TransportMode](#miniproto.config.TransportMode) | [str](#str)</code>) – MTProto TCP framing mode passed to the native implementation.
- **max_payload_size** (<code>[int](#int)</code>) – Maximum decoded MTProto payload size in bytes.
- **server_side** (<code>[bool](#bool)</code>) – Interpret peer quick-ACK request flags as server-side
input.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``mode`` or ``max_payload_size`` violates the same
framing contract enforced by the pure-Python codec.
- <code>[RuntimeError](#RuntimeError)</code> – If the native capability is unavailable or disappears
between capability detection and codec construction.
