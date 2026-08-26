---
title: "miniproto.updates.state.UpdateCursor.from_record"
description: "Build a cursor from persisted session state and bounded update metadata."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.updates.state.UpdateCursor.from_record"
source_path: "src/miniproto/updates/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/state.py#L128"
aliases: ["miniproto.updates.UpdateCursor.from_record"]
module: "miniproto.updates.state"
---

## `miniproto.updates.state.UpdateCursor.from_record`

```python
from_record(record: SessionRecord, *, duplicate_window: int = DEFAULT_DUPLICATE_WINDOW) -> UpdateCursor
```

Build a cursor from persisted session state and bounded update metadata.

**Parameters:**

- **record** (<code>[SessionRecord](#miniproto.session.models.SessionRecord)</code>) – Session record containing update state, peer cache and metadata.
- **duplicate_window** (<code>[int](#int)</code>) – Maximum recent duplicate keys to restore.

**Returns:**

- <code>[UpdateCursor](#miniproto.updates.state.UpdateCursor)</code> – A cursor containing global state, channel cursors, cached entities and the newest retained keys.
