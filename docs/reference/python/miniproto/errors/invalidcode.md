---
title: "miniproto.errors.InvalidCode"
description: "Authentication flow failure for a missing, expired, or invalid phone code."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.InvalidCode"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L328"
aliases: ["miniproto.InvalidCode"]
module: "miniproto.errors"
---

## `miniproto.errors.InvalidCode`

```python
InvalidCode(message: str = 'invalid phone code', *, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[AuthError](#miniproto.errors.AuthError)</code>

Authentication flow failure for a missing, expired, or invalid phone code.

Create an invalid-code failure with status code 400.

**Parameters:**

- **message** (<code>[str](#str)</code>) – Phone-code failure text.
- **request** (<code>[object](#object) | None</code>) – Optional sign-in request associated with the failure.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
