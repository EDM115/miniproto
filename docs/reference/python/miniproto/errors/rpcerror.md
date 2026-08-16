---
title: "miniproto.errors.RpcError"
description: "Raw or classified Telegram RPC failure with redaction-safe diagnostics."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.RpcError"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L79"
aliases: ["miniproto.RpcError"]
module: "miniproto.errors"
---

## `miniproto.errors.RpcError`

```python
RpcError(message: str, code: int | None = None, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[MiniprotoError](#miniproto.errors.MiniprotoError)</code>

Raw or classified Telegram RPC failure with redaction-safe diagnostics.

**Attributes:**

- [**message**](#miniproto.errors.RpcError.message) (<code>[str](#str)</code>) – Telegram's symbolic or descriptive error text.
- [**code**](#miniproto.errors.RpcError.code) (<code>[int](#int) | None</code>) – Optional numeric RPC status code.
- [**request**](#miniproto.errors.RpcError.request) (<code>[object](#object) | None</code>) – Optional request object associated with the failure.
- [**context**](#miniproto.errors.RpcError.context) (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional diagnostic metadata rendered with secret redaction.
