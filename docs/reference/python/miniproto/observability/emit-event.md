---
title: "miniproto.observability.emit_event"
description: "Emit one structured miniproto event if the level is enabled."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.observability.emit_event"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L274"
aliases: ["miniproto.emit_event"]
module: "miniproto.observability"
---

## `miniproto.observability.emit_event`

```python
emit_event(logger: logging.Logger, level: int, event: str, **fields: object) -> None
```

Emit one structured miniproto event if the level is enabled.

**Parameters:**

- **logger** (<code>[Logger](#logging.Logger)</code>) – Destination logger.
- **level** (<code>[int](#int)</code>) – Standard-library numeric log level.
- **event** (<code>[str](#str)</code>) – Stable event name used as the log message and event field.
- ****fields** (<code>[object](#object)</code>) – Additional fields passed to the redacting formatter.
