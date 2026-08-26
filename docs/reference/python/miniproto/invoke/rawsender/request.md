---
title: "miniproto.invoke.RawSender.request"
description: "Send one RPC body, applying sender-specific timeout and retry behavior."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.RawSender.request"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L91"
module: "miniproto.invoke"
---

## `miniproto.invoke.RawSender.request`

```python
request(body: bytes | object, *, content_related: bool = True, retry_safe: bool, request_timeout: float | None = None) -> object
```

Send one RPC body, applying sender-specific timeout and retry behavior.

**Parameters:**

- **body** (<code>[bytes](#bytes) | [object](#object)</code>) – Raw TL request object or its already encoded bytes.
- **content_related** (<code>[bool](#bool)</code>) – Whether MTProto must allocate content-related sequencing.
- **retry_safe** (<code>[bool](#bool)</code>) – Whether transport/request retries may repeat this request.
- **request_timeout** (<code>[float](#float) | None</code>) – Per-request timeout in seconds; ``None`` uses sender defaults.
