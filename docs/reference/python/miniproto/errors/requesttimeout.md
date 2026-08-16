---
title: "miniproto.errors.RequestTimeout"
description: "Raised when the client-side request deadline expires."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.RequestTimeout"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L143"
aliases: ["miniproto.RequestTimeout"]
module: "miniproto.errors"
---

## `miniproto.errors.RequestTimeout`

```python
RequestTimeout(message: str = 'request timed out', *, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[InvokeError](#miniproto.errors.InvokeError)</code>

Raised when the client-side request deadline expires.

Create a request-timeout failure with optional request diagnostics.

**Parameters:**

- **message** (<code>[str](#str)</code>) – Timeout explanation, redacted by the base exception.
- **request** (<code>[object](#object) | None</code>) – Optional request that exceeded its local deadline.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
