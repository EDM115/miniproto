---
title: "miniproto.invoke.sender_needs_init"
description: "Return whether ``sender`` still needs its first init-connection envelope."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.sender_needs_init"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L181"
module: "miniproto.invoke"
---

## `miniproto.invoke.sender_needs_init`

```python
sender_needs_init(sender: object) -> bool
```

Return whether ``sender`` still needs its first init-connection envelope.

**Parameters:**

- **sender** (<code>[object](#object)</code>) – Sender or compatible object carrying optional initialization state.
