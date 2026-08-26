---
title: "miniproto.observability.StructuredFormatter.format"
description: "Format a record while redacting event fields and exception text."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.observability.StructuredFormatter.format"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L219"
aliases: ["miniproto.StructuredFormatter.format"]
module: "miniproto.observability"
---

## `miniproto.observability.StructuredFormatter.format`

```python
format(record: logging.LogRecord) -> str
```

Format a record while redacting event fields and exception text.

**Parameters:**

- **record** (<code>[LogRecord](#logging.LogRecord)</code>) – Standard-library log record.

**Returns:**

- <code>[str](#str)</code> – Redacted text or compact JSON according to the configured format.
