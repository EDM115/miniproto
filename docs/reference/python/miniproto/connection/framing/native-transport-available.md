---
title: "miniproto.connection.framing.native_transport_available"
description: "Return whether the imported native module exposes ``TransportCodec``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.connection.framing.native_transport_available"
source_path: "src/miniproto/connection/framing.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/connection/framing.py#L498"
module: "miniproto.connection.framing"
---

## `miniproto.connection.framing.native_transport_available`

```python
native_transport_available() -> bool
```

Return whether the imported native module exposes ``TransportCodec``.

Merely importing ``miniproto._native`` is insufficient: this is true only
when that import succeeds and provides the codec capability required here.
