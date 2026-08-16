---
title: "miniproto.errors.BadRequest"
description: "Classified client-side Telegram RPC error, normally status code 400."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.BadRequest"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L183"
aliases: ["miniproto.BadRequest"]
module: "miniproto.errors"
---

## `miniproto.errors.BadRequest`

```python
BadRequest(message: str = 'bad request', *, code: int = 400, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[RpcError](#miniproto.errors.RpcError)</code>

Classified client-side Telegram RPC error, normally status code 400.

Create a bad-request error, defaulting its code to 400.

**Parameters:**

- **message** (<code>[str](#str)</code>) – Telegram error text, redacted by the base exception.
- **code** (<code>[int](#int)</code>) – RPC status code, defaulting to Telegram's bad-request code.
- **request** (<code>[object](#object) | None</code>) – Optional request associated with the error.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
