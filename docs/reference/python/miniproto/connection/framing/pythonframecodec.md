---
title: "miniproto.connection.framing.PythonFrameCodec"
description: "Pure-Python incremental encoder/decoder for Telegram TCP transports."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.connection.framing.PythonFrameCodec"
source_path: "src/miniproto/connection/framing.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/framing.py#L88"
module: "miniproto.connection.framing"
---

## `miniproto.connection.framing.PythonFrameCodec`

```python
PythonFrameCodec(mode: TransportMode | str, *, max_payload_size: int, server_side: bool = False) -> None
```

Pure-Python incremental encoder/decoder for Telegram TCP transports.

Create an incremental codec for a TCP transport mode.

**Parameters:**

- **mode** (<code>[TransportMode](#miniproto.config.TransportMode) | [str](#str)</code>) – ``tcp_abridged``, ``tcp_intermediate``, or
``tcp_padded_intermediate``.
- **max_payload_size** (<code>[int](#int)</code>) – Maximum unframed MTProto payload size in bytes.
- **server_side** (<code>[bool](#bool)</code>) – Decode a peer quick-ACK request as a payload flag
rather than treating an incoming quick-ACK marker as a receipt.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If the mode is unsupported or the size bound is not
positive.
