---
title: "miniproto.invoke.is_retryable_request"
description: "Determine whether retrying this request is protocol-safe."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.is_retryable_request"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L279"
module: "miniproto.invoke"
---

## `miniproto.invoke.is_retryable_request`

```python
is_retryable_request(raw_request: object, override: bool | None = None) -> bool
```

Determine whether retrying this request is protocol-safe.

``override`` takes precedence. Otherwise the innermost wrapped request is safe
only for known read prefixes or Telegram writes de-duplicated by ``random_id``.

**Parameters:**

- **raw_request** (<code>[object](#object)</code>) – Request, possibly wrapped in invocation envelopes.
- **override** (<code>[bool](#bool) | None</code>) – Explicit retry policy; ``None`` applies the built-in allowlist.

**Returns:**

- <code>[bool](#bool)</code> – Whether transport or timeout retry code may repeat the request.
