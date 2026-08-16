---
title: "miniproto.auth.service.AuthService.export_authorization"
description: "Export the current user authorization for import at another data center."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.service.AuthService.export_authorization"
source_path: "src/miniproto/auth/service.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/service.py#L155"
aliases: ["miniproto.AuthService.export_authorization","miniproto.auth.AuthService.export_authorization"]
module: "miniproto.auth.service"
---

## `miniproto.auth.service.AuthService.export_authorization`

```python
export_authorization(dc_id: int) -> types.AuthExportedAuthorization
```

Export the current user authorization for import at another data center.

**Parameters:**

- **dc_id** (<code>[int](#int)</code>) – Target data-center identifier.

**Returns:**

- <code>[AuthExportedAuthorization](#miniproto.raw.types.AuthExportedAuthorization)</code> – Telegram's short-lived exported authorization payload.

**Raises:**

- <code>[RpcError](#miniproto.errors.RpcError)</code> – If Telegram returns an unexpected export response.
