---
title: "miniproto.errors.AmbiguousRpcResult"
description: "The transport failed after an RPC may already have reached Telegram."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.AmbiguousRpcResult"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L43"
aliases: ["miniproto.AmbiguousRpcResult"]
module: "miniproto.errors"
---

## `miniproto.errors.AmbiguousRpcResult`

```python
AmbiguousRpcResult(message: str = 'RPC result is ambiguous; the request may have executed', *, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[MiniprotoError](#miniproto.errors.MiniprotoError)</code>

The transport failed after an RPC may already have reached Telegram.

Capture a possibly executed request without exposing secret text.

**Parameters:**

- **message** (<code>[str](#str)</code>) – Human-readable ambiguity explanation, redacted for exception output.
- **request** (<code>[object](#object) | None</code>) – Optional raw request that may have reached Telegram.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional diagnostic fields rendered with secret redaction.
