---
title: "miniproto.security.redaction.safe_repr"
description: "Return a representation after recursively redacting supported secret shapes."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.security.redaction.safe_repr"
source_path: "src/miniproto/security/redaction.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/security/redaction.py#L120"
aliases: ["miniproto.security.safe_repr"]
module: "miniproto.security.redaction"
---

## `miniproto.security.redaction.safe_repr`

```python
safe_repr(value: object) -> str
```

Return a representation after recursively redacting supported secret shapes.

**Parameters:**

- **value** (<code>[object](#object)</code>) – Arbitrary value intended for diagnostic output.

**Returns:**

- <code>[str](#str)</code> – The safe representation of the redacted value.
