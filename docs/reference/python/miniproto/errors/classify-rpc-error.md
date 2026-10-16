---
title: "miniproto.errors.classify_rpc_error"
description: "Return the most specific public error matching a raw Telegram RPC error."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.errors.classify_rpc_error"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L533"
module: "miniproto.errors"
---

## `miniproto.errors.classify_rpc_error`

```python
classify_rpc_error(error: RpcError) -> RpcError
```

Return the most specific public error matching a raw Telegram RPC error.

Migration and supported pacing suffixes supply the target DC or wait duration. Generated schema classes take precedence over known exact errors and numeric status classes. Unknown errors retain their original instance.

**Parameters:**

- **error** (<code>[RpcError](#miniproto.errors.RpcError)</code>) – Raw or already classified RPC error to inspect.

**Returns:**

- <code>[RpcError](#miniproto.errors.RpcError)</code> – The same instance when no classification applies, otherwise a specific error retaining message, request and context. The selected error class may replace the numeric code with its standard code.
