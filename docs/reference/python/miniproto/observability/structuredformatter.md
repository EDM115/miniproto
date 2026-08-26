---
title: "miniproto.observability.StructuredFormatter"
description: "Formatter that redacts structured events and optionally emits compact JSON."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.observability.StructuredFormatter"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L207"
aliases: ["miniproto.StructuredFormatter"]
module: "miniproto.observability"
---

## `miniproto.observability.StructuredFormatter`

```python
StructuredFormatter(*, fmt: LogFormat = 'text') -> None
```

Bases: <code>[Formatter](#logging.Formatter)</code>

Formatter that redacts structured events and optionally emits compact JSON.

Initialize the formatter.

**Parameters:**

- **fmt** (<code>[LogFormat](#miniproto.observability.LogFormat)</code>) – ``"text"`` (default) or compact ``"json"`` event output.
