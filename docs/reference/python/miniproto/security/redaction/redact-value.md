---
title: "miniproto.security.redaction.redact_value"
description: "Replace a value with the fixed redaction marker."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.security.redaction.redact_value"
source_path: "src/miniproto/security/redaction.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/security/redaction.py#L64"
aliases: ["miniproto.security.redact_value"]
module: "miniproto.security.redaction"
---

## `miniproto.security.redaction.redact_value`

```python
redact_value(value: object) -> str
```

Replace a value with the fixed redaction marker.

**Parameters:**

- **value** (<code>[object](#object)</code>) – Value deliberately ignored so secrets never reach output.

**Returns:**

- <code>[str](#str)</code> – The constant ``"[redacted]"`` marker.
