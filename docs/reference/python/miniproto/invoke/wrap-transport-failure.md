---
title: "miniproto.invoke.wrap_transport_failure"
description: "Translate a transport exception to the RPC-level error exposed to callers."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.wrap_transport_failure"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L582"
module: "miniproto.invoke"
---

## `miniproto.invoke.wrap_transport_failure`

```python
wrap_transport_failure(exc: BaseException, raw_request: object, *, connected: bool) -> RpcError
```

Translate a transport exception to the RPC-level error exposed to callers.

A disconnected sender takes precedence over a timeout classification so retry
policy can distinguish a lost client lifecycle from an individual request delay.

**Parameters:**

- **exc** (<code>[BaseException](#BaseException)</code>) – Transport-layer exception raised while processing the request.
- **raw_request** (<code>[object](#object)</code>) – Original raw request retained on the resulting RPC error.
- **connected** (<code>[bool](#bool)</code>) – Whether the sender was connected when the failure was classified.
