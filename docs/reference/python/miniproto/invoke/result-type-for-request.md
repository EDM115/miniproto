---
title: "miniproto.invoke.result_type_for_request"
description: "Return a raw request class's declared TL ``RESULT_TYPE``, when available."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.result_type_for_request"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L269"
module: "miniproto.invoke"
---

## `miniproto.invoke.result_type_for_request`

```python
result_type_for_request(raw_request: object) -> str | None
```

Return a raw request class's declared TL ``RESULT_TYPE``, when available.

**Parameters:**

- **raw_request** (<code>[object](#object)</code>) – Constructor-backed Telegram request whose class may declare a result type.
