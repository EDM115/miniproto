---
title: "miniproto.errors.InvalidDatacenter"
description: "Telegram rejects the current data centre, commonly before a migration hint."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.InvalidDatacenter"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L448"
aliases: ["miniproto.InvalidDatacenter"]
module: "miniproto.errors"
---

## `miniproto.errors.InvalidDatacenter`

```python
InvalidDatacenter(message: str = 'invalid datacenter', *, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[AuthError](#miniproto.errors.AuthError)</code>

Telegram rejects the current data centre, commonly before a migration hint.

Create an invalid-datacenter failure with status code 303.

**Parameters:**

- **message** (<code>[str](#str)</code>) – Telegram data-center failure text.
- **request** (<code>[object](#object) | None</code>) – Optional request associated with the data-center failure.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
