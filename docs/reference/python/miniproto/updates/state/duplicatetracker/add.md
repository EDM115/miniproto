---
title: "miniproto.updates.state.DuplicateTracker.add"
description: "Remember a new key, evicting the oldest retained key when the window is full."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.updates.state.DuplicateTracker.add"
source_path: "src/miniproto/updates/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/state.py#L283"
aliases: ["miniproto.updates.DuplicateTracker.add"]
module: "miniproto.updates.state"
---

## `miniproto.updates.state.DuplicateTracker.add`

```python
add(key: str) -> None
```

Remember a new key, evicting the oldest retained key when the window is full.

**Parameters:**

- **key** (<code>[str](#str)</code>) – Raw update identity key to retain.
