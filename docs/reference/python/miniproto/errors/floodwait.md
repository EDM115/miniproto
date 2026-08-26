---
title: "miniproto.errors.FloodWait"
description: "Telegram pacing failure that exposes the required wait duration in seconds."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.FloodWait"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L297"
aliases: ["miniproto.FloodWait"]
module: "miniproto.errors"
---

## `miniproto.errors.FloodWait`

```python
FloodWait(seconds: int, message: str | None = None, *, code: int = 420, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[RpcError](#miniproto.errors.RpcError)</code>

Telegram pacing failure that exposes the required wait duration in seconds.

Create a flood wait with its server-provided delay and optional diagnostics.

**Parameters:**

- **seconds** (<code>[int](#int)</code>) – Server-required wait duration in seconds.
- **message** (<code>[str](#str) | None</code>) – Optional Telegram error text; a descriptive default is generated when absent.
- **code** (<code>[int](#int)</code>) – RPC code, defaulting to Telegram's flood-wait code 420.
- **request** (<code>[object](#object) | None</code>) – Optional request that triggered pacing.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
