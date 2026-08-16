---
title: "miniproto.updates.state.UpdateCursor.with_duplicate_keys"
description: "Return a cursor with the supplied persisted duplicate-key sequence."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.updates.state.UpdateCursor.with_duplicate_keys"
source_path: "src/miniproto/updates/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/state.py#L232"
aliases: ["miniproto.updates.UpdateCursor.with_duplicate_keys"]
module: "miniproto.updates.state"
---

## `miniproto.updates.state.UpdateCursor.with_duplicate_keys`

```python
with_duplicate_keys(duplicate_keys: Iterable[str]) -> UpdateCursor
```

Return a cursor with the supplied persisted duplicate-key sequence.

**Parameters:**

- **duplicate_keys** (<code>[Iterable](#collections.abc.Iterable)[[str](#str)]</code>) – Recent update identity keys to persist in order.
