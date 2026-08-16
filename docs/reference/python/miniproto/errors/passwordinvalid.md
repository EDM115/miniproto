---
title: "miniproto.errors.PasswordInvalid"
description: "Authentication flow received an invalid two-factor password."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.PasswordInvalid"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L368"
aliases: ["miniproto.PasswordInvalid"]
module: "miniproto.errors"
---

## `miniproto.errors.PasswordInvalid`

```python
PasswordInvalid(message: str = 'invalid 2FA password', *, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[AuthError](#miniproto.errors.AuthError)</code>

Authentication flow received an invalid two-factor password.

Create a password-invalid failure with status code 400.

**Parameters:**

- **message** (<code>[str](#str)</code>) – Two-factor-password failure text.
- **request** (<code>[object](#object) | None</code>) – Optional password-check request associated with the failure.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
