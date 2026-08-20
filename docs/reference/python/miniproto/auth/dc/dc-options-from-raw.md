---
title: "miniproto.auth.dc.dc_options_from_raw"
description: "Convert raw Telegram DC options to immutable session-model options."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.dc.dc_options_from_raw"
source_path: "src/miniproto/auth/dc.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/dc.py#L79"
aliases: ["miniproto.auth.dc_options_from_raw"]
module: "miniproto.auth.dc"
---

## `miniproto.auth.dc.dc_options_from_raw`

```python
dc_options_from_raw(raw_options: Iterable[RawDCOption]) -> tuple[DCOption, ...]
```

Convert raw Telegram DC options to immutable session-model options.

**Parameters:**

- **raw_options** (<code>[Iterable](#collections.abc.Iterable)[[RawDCOption](#miniproto.auth.dc.RawDCOption)]</code>) – Decoded Telegram configuration options.

**Returns:**

- <code>[tuple](#tuple)[[DCOption](#miniproto.session.models.DCOption), ...]</code> – Equivalent session options with optional raw flags normalized to booleans.
