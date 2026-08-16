---
title: "miniproto.observability.get_logger"
description: "Return the root miniproto logger or a named child logger."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.observability.get_logger"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L245"
aliases: ["miniproto.get_logger"]
module: "miniproto.observability"
---

## `miniproto.observability.get_logger`

```python
get_logger(name: str | None = None) -> logging.Logger
```

Return the root miniproto logger or a named child logger.

**Parameters:**

- **name** (<code>[str](#str) | None</code>) – Optional child-name suffix.

**Returns:**

- <code>[Logger](#logging.Logger)</code> – The requested standard-library logger.
