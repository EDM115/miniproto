---
title: "miniproto.updates.state.UpdateCursor.with_channel_state"
description: "Return a cursor with one channel's PTS state replaced or added."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.updates.state.UpdateCursor.with_channel_state"
source_path: "src/miniproto/updates/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/state.py#L190"
aliases: ["miniproto.updates.UpdateCursor.with_channel_state"]
module: "miniproto.updates.state"
---

## `miniproto.updates.state.UpdateCursor.with_channel_state`

```python
with_channel_state(channel_id: int, *, pts: int, date: datetime | int | float | str | None = None) -> UpdateCursor
```

Return a cursor with one channel's PTS state replaced or added.

**Parameters:**

- **channel_id** (<code>[int](#int)</code>) – Telegram channel identifier whose cursor is updated.
- **pts** (<code>[int](#int)</code>) – Replacement channel persistent timestamp.
- **date** (<code>[datetime](#datetime.datetime) | [int](#int) | [float](#float) | [str](#str) | None</code>) – Optional channel datetime/string/Unix timestamp; aware values retain their timezone.
