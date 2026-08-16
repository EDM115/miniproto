---
title: "miniproto.auth.service.AuthService.select_current_dc"
description: "Return the preferred non-media endpoint for the persisted current DC."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.service.AuthService.select_current_dc"
source_path: "src/miniproto/auth/service.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/service.py#L213"
aliases: ["miniproto.AuthService.select_current_dc","miniproto.auth.AuthService.select_current_dc"]
module: "miniproto.auth.service"
---

## `miniproto.auth.service.AuthService.select_current_dc`

```python
select_current_dc() -> DCOption
```

Return the preferred non-media endpoint for the persisted current DC.

**Raises:**

- <code>[InvalidDatacenter](#miniproto.errors.InvalidDatacenter)</code> – If the session has no saved endpoint for its current DC.
