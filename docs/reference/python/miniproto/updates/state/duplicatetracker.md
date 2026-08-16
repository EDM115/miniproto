---
title: "miniproto.updates.state.DuplicateTracker"
description: "Bounded insertion-ordered set for duplicate suppression across persisted update state."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.updates.state.DuplicateTracker"
source_path: "src/miniproto/updates/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/state.py#L249"
aliases: ["miniproto.updates.DuplicateTracker"]
module: "miniproto.updates.state"
---

## `miniproto.updates.state.DuplicateTracker`

```python
DuplicateTracker(keys: Iterable[str] = (), *, max_size: int = DEFAULT_DUPLICATE_WINDOW) -> None
```

Bounded insertion-ordered set for duplicate suppression across persisted update state.

**Parameters:**

- **keys** (<code>[Iterable](#collections.abc.Iterable)[[str](#str)]</code>) – Existing keys restored from session metadata.
- **max_size** (<code>[int](#int)</code>) – Positive maximum number of keys retained, defaulting to 2048.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``max_size`` is not positive.

Restore optional keys while retaining only the most recent ``max_size`` distinct values.

**Parameters:**

- **keys** (<code>[Iterable](#collections.abc.Iterable)[[str](#str)]</code>) – Existing persisted duplicate keys to restore.
- **max_size** (<code>[int](#int)</code>) – Positive maximum count retained in the duplicate window.
