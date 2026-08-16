---
title: "miniproto.errors.NotFound"
description: "Classified Telegram missing-resource failure with status code 404."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.NotFound"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L237"
aliases: ["miniproto.NotFound"]
module: "miniproto.errors"
---

## `miniproto.errors.NotFound`

```python
NotFound(message: str = 'not found', *, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[RpcError](#miniproto.errors.RpcError)</code>

Classified Telegram missing-resource failure with status code 404.

Create a not-found error with optional request context.

**Parameters:**

- **message** (<code>[str](#str)</code>) – Telegram missing-resource text.
- **request** (<code>[object](#object) | None</code>) – Optional request associated with the failure.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
