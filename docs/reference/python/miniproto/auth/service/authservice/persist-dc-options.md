---
title: "miniproto.auth.service.AuthService.persist_dc_options"
description: "Normalize ``help.Config`` DC options and atomically store them in the session."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.service.AuthService.persist_dc_options"
source_path: "src/miniproto/auth/service.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/service.py#L188"
aliases: ["miniproto.AuthService.persist_dc_options","miniproto.auth.AuthService.persist_dc_options"]
module: "miniproto.auth.service"
---

## `miniproto.auth.service.AuthService.persist_dc_options`

```python
persist_dc_options(raw_config: object) -> tuple[DCOption, ...]
```

Normalize ``help.Config`` DC options and atomically store them in the session.

**Parameters:**

- **raw_config** (<code>[object](#object)</code>) – Telegram configuration result exposing ``dc_options`` and optional ``this_dc``.

**Returns:**

- <code>[tuple](#tuple)[[DCOption](#miniproto.session.models.DCOption), ...]</code> – The normalized, persisted data-center options.
