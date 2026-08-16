---
title: "miniproto.errors.ClientDisconnected"
description: "Raised when invocation cannot continue because the client disconnected."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.ClientDisconnected"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L123"
aliases: ["miniproto.ClientDisconnected"]
module: "miniproto.errors"
---

## `miniproto.errors.ClientDisconnected`

```python
ClientDisconnected(message: str = 'client disconnected', *, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[InvokeError](#miniproto.errors.InvokeError)</code>

Raised when invocation cannot continue because the client disconnected.

Create a disconnect failure with optional request diagnostics.

**Parameters:**

- **message** (<code>[str](#str)</code>) – Disconnect explanation, redacted by the base exception.
- **request** (<code>[object](#object) | None</code>) – Optional request interrupted by the client lifecycle change.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
