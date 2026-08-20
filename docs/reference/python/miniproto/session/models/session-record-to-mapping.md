---
title: "miniproto.session.models.session_record_to_mapping"
description: "Serialize a typed record to the canonical storage-compatible mapping."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.models.session_record_to_mapping"
source_path: "src/miniproto/session/models.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/models.py#L254"
aliases: ["miniproto.session.session_record_to_mapping"]
module: "miniproto.session.models"
---

## `miniproto.session.models.session_record_to_mapping`

```python
session_record_to_mapping(record: SessionRecord) -> dict[str, Any]
```

Serialize a typed record to the canonical storage-compatible mapping.

**Parameters:**

- **record** (<code>[SessionRecord](#miniproto.session.models.SessionRecord)</code>) – Validated immutable session state.

**Returns:**

- <code>[dict](#dict)[[str](#str), [Any](#typing.Any)]</code> – A new mapping retaining bytes and datetimes for storage encoding.
