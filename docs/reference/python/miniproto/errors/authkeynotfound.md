---
title: "miniproto.errors.AuthKeyNotFound"
description: "Authentication key is invalid, unregistered or no longer available."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.AuthKeyNotFound"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L408"
aliases: ["miniproto.AuthKeyNotFound"]
module: "miniproto.errors"
---

## `miniproto.errors.AuthKeyNotFound`

```python
AuthKeyNotFound(message: str = 'auth key not registered', *, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[AuthError](#miniproto.errors.AuthError)</code>

Authentication key is invalid, unregistered or no longer available.

Create an auth-key-not-found failure with status code 401.

**Parameters:**

- **message** (<code>[str](#str)</code>) – Telegram auth-key failure text.
- **request** (<code>[object](#object) | None</code>) – Optional request attempted with the unavailable key.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
