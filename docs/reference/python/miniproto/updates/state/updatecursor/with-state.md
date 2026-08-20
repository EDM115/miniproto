---
title: "miniproto.updates.state.UpdateCursor.with_state"
description: "Return a cursor with selected global state fields replaced."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.updates.state.UpdateCursor.with_state"
source_path: "src/miniproto/updates/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/state.py#L156"
aliases: ["miniproto.updates.UpdateCursor.with_state"]
module: "miniproto.updates.state"
---

## `miniproto.updates.state.UpdateCursor.with_state`

```python
with_state(*, pts: int | None = None, qts: int | None = None, seq: int | None = None, date: datetime | int | float | str | None = None) -> UpdateCursor
```

Return a cursor with selected global state fields replaced.

``date`` accepts the same representations as ``coerce_update_datetime``; omitted fields retain their current values.

**Parameters:**

- **pts** (<code>[int](#int) | None</code>) – Optional replacement global persistent timestamp.
- **qts** (<code>[int](#int) | None</code>) – Optional replacement secret-chat timestamp.
- **seq** (<code>[int](#int) | None</code>) – Optional replacement global sequence number.
- **date** (<code>[datetime](#datetime.datetime) | [int](#int) | [float](#float) | [str](#str) | None</code>) – Optional datetime/string/Unix timestamp; aware values retain their timezone.
