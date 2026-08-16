---
title: "miniproto.invoke.mark_sender_initialized"
description: "Mark a sender as initialized when it permits dynamic state attributes."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.mark_sender_initialized"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L190"
module: "miniproto.invoke"
---

## `miniproto.invoke.mark_sender_initialized`

```python
mark_sender_initialized(sender: object) -> None
```

Mark a sender as initialized when it permits dynamic state attributes.

Slot-only test doubles intentionally keep the default always-wrap behavior.

**Parameters:**

- **sender** (<code>[object](#object)</code>) – Sender or compatible object to mark when it accepts dynamic attributes.
