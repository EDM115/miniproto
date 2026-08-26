---
title: "miniproto.errors.Unauthorized"
description: "Classified Telegram authorization failure with status code 401."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.Unauthorized"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L205"
aliases: ["miniproto.Unauthorized"]
module: "miniproto.errors"
---

## `miniproto.errors.Unauthorized`

```python
Unauthorized(message: str = 'unauthorized', *, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[RpcError](#miniproto.errors.RpcError)</code>

Classified Telegram authorization failure with status code 401.

Create an unauthorized error with optional request context.

**Parameters:**

- **message** (<code>[str](#str)</code>) – Telegram authorization-failure text.
- **request** (<code>[object](#object) | None</code>) – Optional request associated with the failure.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
