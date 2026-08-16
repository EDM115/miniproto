---
title: "miniproto.errors.SignUpRequired"
description: "Authentication flow requires creating a Telegram account first."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.SignUpRequired"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L388"
aliases: ["miniproto.SignUpRequired"]
module: "miniproto.errors"
---

## `miniproto.errors.SignUpRequired`

```python
SignUpRequired(message: str = 'sign-up required', *, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[AuthError](#miniproto.errors.AuthError)</code>

Authentication flow requires creating a Telegram account first.

Create a sign-up-required failure with status code 401.

**Parameters:**

- **message** (<code>[str](#str)</code>) – Telegram sign-up requirement text.
- **request** (<code>[object](#object) | None</code>) – Optional sign-in request associated with the failure.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
