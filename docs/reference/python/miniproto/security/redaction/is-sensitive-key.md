---
title: "miniproto.security.redaction.is_sensitive_key"
description: "Return whether a mapping key is recognized as sensitive."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.security.redaction.is_sensitive_key"
source_path: "src/miniproto/security/redaction.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/security/redaction.py#L47"
aliases: ["miniproto.security.is_sensitive_key"]
module: "miniproto.security.redaction"
---

## `miniproto.security.redaction.is_sensitive_key`

```python
is_sensitive_key(key: object) -> bool
```

Return whether a mapping key is recognized as sensitive.

**Parameters:**

- **key** (<code>[object](#object)</code>) – Arbitrary mapping key converted to text for normalization.

**Returns:**

- <code>[bool](#bool)</code> – ``True`` for known secret-bearing key names or compound variants.
