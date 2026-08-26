---
title: "miniproto.errors.AuthKeyRegenerationRequired"
description: "Authentication key is duplicated or unsynchronized and must be replaced."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.AuthKeyRegenerationRequired"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L428"
aliases: ["miniproto.AuthKeyRegenerationRequired"]
module: "miniproto.errors"
---

## `miniproto.errors.AuthKeyRegenerationRequired`

```python
AuthKeyRegenerationRequired(message: str = 'auth key must be regenerated', *, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[AuthError](#miniproto.errors.AuthError)</code>

Authentication key is duplicated or unsynchronized and must be replaced.

Create an auth-key-regeneration failure with status code 406.

**Parameters:**

- **message** (<code>[str](#str)</code>) – Telegram key-regeneration requirement text.
- **request** (<code>[object](#object) | None</code>) – Optional request attempted with the unsynchronized key.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
