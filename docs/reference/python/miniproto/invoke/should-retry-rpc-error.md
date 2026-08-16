---
title: "miniproto.invoke.should_retry_rpc_error"
description: "Return whether a classified server-side RPC failure is transient enough to retry."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.should_retry_rpc_error"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L312"
module: "miniproto.invoke"
---

## `miniproto.invoke.should_retry_rpc_error`

```python
should_retry_rpc_error(error: RpcError) -> bool
```

Return whether a classified server-side RPC failure is transient enough to retry.

**Parameters:**

- **error** (<code>[RpcError](#miniproto.errors.RpcError)</code>) – Classified RPC failure whose type and numeric code are inspected.
