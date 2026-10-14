---
title: "miniproto.connection.framing.create_frame_codec"
description: "Select the native TCP framing codec when available, otherwise the Python codec."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.framing.create_frame_codec"
source_path: "src/miniproto/connection/framing.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/framing.py#L507"
module: "miniproto.connection.framing"
---

## `miniproto.connection.framing.create_frame_codec`

```python
create_frame_codec(mode: TransportMode | str, *, max_payload_size: int, server_side: bool = False) -> TransportFrameCodec
```

Select the native TCP framing codec when available, otherwise the Python codec.

**Parameters:**

- **mode** (<code>[TransportMode](#miniproto.config.TransportMode) | [str](#str)</code>) – Requested TCP transport mode.
- **max_payload_size** (<code>[int](#int)</code>) – Maximum permitted unframed MTProto payload size.
- **server_side** (<code>[bool](#bool)</code>) – Whether decoding models traffic received by a server.

**Returns:**

- <code>[TransportFrameCodec](#miniproto.connection.framing.TransportFrameCodec)</code> – The native adapter when its extension is available; otherwise the
- <code>[TransportFrameCodec](#miniproto.connection.framing.TransportFrameCodec)</code> – behavior-equivalent pure-Python incremental codec.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the selected codec rejects the mode or payload bound.
- <code>[OverflowError](#OverflowError)</code> – If a native payload bound cannot fit the platform's unsigned size type.
- <code>[RuntimeError](#RuntimeError)</code> – If the native extension is found but cannot initialize.
