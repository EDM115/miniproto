---
title: "miniproto.auth.service.AuthService.import_authorization"
description: "Import an exported authorization and persist it when it includes user data."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.service.AuthService.import_authorization"
source_path: "src/miniproto/auth/service.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/service.py#L172"
aliases: ["miniproto.AuthService.import_authorization","miniproto.auth.AuthService.import_authorization"]
module: "miniproto.auth.service"
---

## `miniproto.auth.service.AuthService.import_authorization`

```python
import_authorization(exported: types.AuthExportedAuthorization) -> object
```

Import an exported authorization and persist it when it includes user data.

**Parameters:**

- **exported** (<code>[AuthExportedAuthorization](#miniproto.raw.types.AuthExportedAuthorization)</code>) – Authorization previously exported for this data center.

**Returns:**

- <code>[object](#object)</code> – Telegram's import result, which may or may not include an authorization object.
