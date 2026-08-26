---
title: "miniproto.errors.InternalServerError"
description: "Classified retryable server failure, normally a 5xx RPC code."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.InternalServerError"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L275"
aliases: ["miniproto.InternalServerError"]
module: "miniproto.errors"
---

## `miniproto.errors.InternalServerError`

```python
InternalServerError(message: str = 'internal server error', *, code: int | None = 500, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[RpcError](#miniproto.errors.RpcError)</code>

Classified retryable server failure, normally a 5xx RPC code.

Create a server error while preserving an explicit server code.

**Parameters:**

- **message** (<code>[str](#str)</code>) – Telegram server-failure text.
- **code** (<code>[int](#int) | None</code>) – Optional RPC code, defaulting to 500.
- **request** (<code>[object](#object) | None</code>) – Optional request associated with the server failure.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
