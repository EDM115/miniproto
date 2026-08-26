---
title: "miniproto.observability.configure_logging"
description: "Install one redacting handler on the miniproto root logger."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.observability.configure_logging"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L257"
aliases: ["miniproto.configure_logging"]
module: "miniproto.observability"
---

## `miniproto.observability.configure_logging`

```python
configure_logging(level: str | int = 'INFO', *, format: LogFormat = 'text', stream: TextIO | None = None) -> None
```

Install one redacting handler on the miniproto root logger.

**Parameters:**

- **level** (<code>[str](#str) | [int](#int)</code>) – Logging level name or numeric level, defaulting to ``"INFO"``.
- **format** (<code>[LogFormat](#miniproto.observability.LogFormat)</code>) – Event format, either ``"text"`` (default) or ``"json"``.
- **stream** (<code>[TextIO](#typing.TextIO) | None</code>) – Optional handler output stream; defaults to standard error.
