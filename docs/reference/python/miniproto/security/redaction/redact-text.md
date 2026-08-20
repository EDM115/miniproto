---
title: "miniproto.security.redaction.redact_text"
description: "Mask recognized ``key=value`` and ``key: value`` secrets in text."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.security.redaction.redact_text"
source_path: "src/miniproto/security/redaction.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/security/redaction.py#L90"
aliases: ["miniproto.security.redact_text"]
module: "miniproto.security.redaction"
---

## `miniproto.security.redaction.redact_text`

```python
redact_text(text: str) -> str
```

Mask recognized ``key=value`` and ``key: value`` secrets in text.

**Parameters:**

- **text** (<code>[str](#str)</code>) – Text that may contain supported sensitive assignments.

**Returns:**

- <code>[str](#str)</code> – Text with matched values replaced by the redaction marker.
