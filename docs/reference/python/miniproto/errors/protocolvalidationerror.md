---
title: "miniproto.errors.ProtocolValidationError"
description: "An authenticated MTProto message violated the inbound protocol contract."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.ProtocolValidationError"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L17"
module: "miniproto.errors"
---

## `miniproto.errors.ProtocolValidationError`

```python
ProtocolValidationError(reason: str, *, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[MiniprotoError](#miniproto.errors.MiniprotoError)</code>, <code>[ValueError](#ValueError)</code>

An authenticated MTProto message violated the inbound protocol contract.

Capture a validation reason and optional diagnostic context safely.

**Parameters:**

- **reason** (<code>[str](#str)</code>) – Protocol rule that the inbound authenticated message violated.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional diagnostic fields rendered through secret-safe formatting.
