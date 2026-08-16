---
title: "miniproto.updates.state.UpdateCursor.with_entities"
description: "Return a cursor with incoming entities merged by peer kind and identifier."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.updates.state.UpdateCursor.with_entities"
source_path: "src/miniproto/updates/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/state.py#L215"
aliases: ["miniproto.updates.UpdateCursor.with_entities"]
module: "miniproto.updates.state"
---

## `miniproto.updates.state.UpdateCursor.with_entities`

```python
with_entities(entities: Iterable[EntityReference]) -> UpdateCursor
```

Return a cursor with incoming entities merged by peer kind and identifier.

**Parameters:**

- **entities** (<code>[Iterable](#collections.abc.Iterable)[[EntityReference](#miniproto.updates.state.EntityReference)]</code>) – Entity references observed in newly processed update data.
