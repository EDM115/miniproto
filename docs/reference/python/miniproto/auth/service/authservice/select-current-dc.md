---
title: "miniproto.auth.service.AuthService.select_current_dc"
description: "Select an endpoint for the persisted DC, preferring non-media candidates."
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

Select an endpoint for the persisted DC, preferring non-media candidates.

**Raises:**

- <code>[InvalidDatacenter](#miniproto.errors.InvalidDatacenter)</code> – If the session has no saved DC options.
- <code>[ValueError](#ValueError)</code> – If the saved options contain no endpoint for the current DC.
