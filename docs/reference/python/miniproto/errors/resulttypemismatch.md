---
title: "miniproto.errors.ResultTypeMismatch"
description: "Raised when an RPC result does not match the requested result contract."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.ResultTypeMismatch"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L163"
aliases: ["miniproto.ResultTypeMismatch"]
module: "miniproto.errors"
---

## `miniproto.errors.ResultTypeMismatch`

```python
ResultTypeMismatch(expected: str, actual: object, *, request: object | None = None) -> None
```

Bases: <code>[InvokeError](#miniproto.errors.InvokeError)</code>

Raised when an RPC result does not match the requested result contract.

Record expected and actual result type names for a failed invocation.

**Parameters:**

- **expected** (<code>[str](#str)</code>) – Declared TL result type expected by the request.
- **actual** (<code>[object](#object)</code>) – Decoded result object that failed the type contract.
- **request** (<code>[object](#object) | None</code>) – Optional original request retained for diagnostics.
