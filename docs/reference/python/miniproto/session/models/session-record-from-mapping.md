---
title: "miniproto.session.models.session_record_from_mapping"
description: "Construct a validated record from a decoded canonical mapping."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.models.session_record_from_mapping"
source_path: "src/miniproto/session/models.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/models.py#L273"
aliases: ["miniproto.session.session_record_from_mapping"]
module: "miniproto.session.models"
---

## `miniproto.session.models.session_record_from_mapping`

```python
session_record_from_mapping(data: Mapping[str, Any]) -> SessionRecord
```

Construct a validated record from a decoded canonical mapping.

**Parameters:**

- **data** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)]</code>) – Canonical session mapping decoded from storage.

**Raises:**

- <code>[KeyError](#KeyError)</code> – If required nested fields are missing.
- <code>[TypeError](#TypeError)</code> – If nested mappings or byte fields have invalid shapes.
- <code>[ValueError](#ValueError)</code> – If model validation or peer-kind conversion fails.
