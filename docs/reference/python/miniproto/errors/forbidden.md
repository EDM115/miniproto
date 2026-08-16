---
title: "miniproto.errors.Forbidden"
description: "Classified Telegram permission failure with status code 403."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.Forbidden"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L221"
aliases: ["miniproto.Forbidden"]
module: "miniproto.errors"
---

## `miniproto.errors.Forbidden`

```python
Forbidden(message: str = 'forbidden', *, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[RpcError](#miniproto.errors.RpcError)</code>

Classified Telegram permission failure with status code 403.

Create a forbidden error with optional request context.

**Parameters:**

- **message** (<code>[str](#str)</code>) – Telegram permission-failure text.
- **request** (<code>[object](#object) | None</code>) – Optional request associated with the failure.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
