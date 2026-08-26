---
title: "miniproto.errors.classify_rpc_error"
description: "Return the most specific public error matching a raw Telegram RPC error."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.errors.classify_rpc_error"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L531"
module: "miniproto.errors"
---

## `miniproto.errors.classify_rpc_error`

```python
classify_rpc_error(error: RpcError) -> RpcError
```

Return the most specific public error matching a raw Telegram RPC error.

Migration and flood suffixes preserve their extracted DC or wait duration;
generated schema classes take precedence, followed by known exact errors and
numeric status classes. Unknown errors are returned unchanged.

**Parameters:**

- **error** (<code>[RpcError](#miniproto.errors.RpcError)</code>) – Raw or already classified RPC error to inspect.

**Returns:**

- <code>[RpcError](#miniproto.errors.RpcError)</code> – The same instance when no classification applies, otherwise a specific
- <code>[RpcError](#miniproto.errors.RpcError)</code> – error that preserves message, code, request and context.
