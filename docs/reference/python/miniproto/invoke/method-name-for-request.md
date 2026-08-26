---
title: "miniproto.invoke.method_name_for_request"
description: "Return the innermost wrapped request class's Telegram-qualified method name."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.method_name_for_request"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L436"
module: "miniproto.invoke"
---

## `miniproto.invoke.method_name_for_request`

```python
method_name_for_request(request: object) -> str
```

Return the innermost wrapped request class's Telegram-qualified method name.

**Parameters:**

- **request** (<code>[object](#object)</code>) – Raw request, optionally nested in Telegram invocation envelopes.
