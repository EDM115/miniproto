---
title: "miniproto.errors.PasswordRequired"
description: "Authentication flow requires a configured two-factor password."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.PasswordRequired"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L348"
aliases: ["miniproto.PasswordRequired"]
module: "miniproto.errors"
---

## `miniproto.errors.PasswordRequired`

```python
PasswordRequired(message: str = '2FA password required', *, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[AuthError](#miniproto.errors.AuthError)</code>

Authentication flow requires a configured two-factor password.

Create a password-required failure with status code 401.

**Parameters:**

- **message** (<code>[str](#str)</code>) – Two-factor-password requirement text.
- **request** (<code>[object](#object) | None</code>) – Optional authentication request associated with the failure.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
