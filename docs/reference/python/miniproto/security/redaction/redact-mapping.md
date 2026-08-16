---
title: "miniproto.security.redaction.redact_mapping"
description: "Return a recursively sanitized copy of a mapping."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.security.redaction.redact_mapping"
source_path: "src/miniproto/security/redaction.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/security/redaction.py#L74"
aliases: ["miniproto.security.redact_mapping"]
module: "miniproto.security.redaction"
---

## `miniproto.security.redaction.redact_mapping`

```python
redact_mapping(data: Mapping[Any, Any]) -> dict[str, Any]
```

Return a recursively sanitized copy of a mapping.

**Parameters:**

- **data** (<code>[Mapping](#collections.abc.Mapping)[[Any](#typing.Any), [Any](#typing.Any)]</code>) – Mapping whose keys and nested values may contain credentials.

**Returns:**

- <code>[dict](#dict)[[str](#str), [Any](#typing.Any)]</code> – A string-keyed mapping with recognized sensitive values replaced.
