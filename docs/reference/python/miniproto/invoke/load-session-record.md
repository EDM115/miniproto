---
title: "miniproto.invoke.load_session_record"
description: "Load current structured or legacy session data into a ``SessionRecord``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.invoke.load_session_record"
source_path: "src/miniproto/invoke.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/invoke.py#L460"
module: "miniproto.invoke"
---

## `miniproto.invoke.load_session_record`

```python
load_session_record(payload: Mapping[str, Any] | None, default_dc_id: int) -> SessionRecord
```

Load current structured or legacy session data into a ``SessionRecord``.

**Parameters:**

- **payload** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Stored session mapping or ``None`` for a new session.
- **default_dc_id** (<code>[int](#int)</code>) – Fallback Telegram DC for empty or legacy mappings.

**Returns:**

- <code>[SessionRecord](#miniproto.session.models.SessionRecord)</code> – A normalized session record without mutating the supplied mapping.
