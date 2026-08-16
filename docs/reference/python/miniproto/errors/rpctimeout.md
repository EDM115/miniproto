---
title: "miniproto.errors.RpcTimeout"
description: "Classified Telegram-side or transport RPC timeout, commonly code -503."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.RpcTimeout"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L253"
aliases: ["miniproto.RpcTimeout"]
module: "miniproto.errors"
---

## `miniproto.errors.RpcTimeout`

```python
RpcTimeout(message: str = 'RPC timeout', *, code: int | None = -503, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[RpcError](#miniproto.errors.RpcError)</code>

Classified Telegram-side or transport RPC timeout, commonly code -503.

Create an RPC timeout while preserving an explicit server code.

**Parameters:**

- **message** (<code>[str](#str)</code>) – Telegram or transport timeout explanation.
- **code** (<code>[int](#int) | None</code>) – Optional RPC code, defaulting to the common ``-503`` timeout code.
- **request** (<code>[object](#object) | None</code>) – Optional request associated with the timeout.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
