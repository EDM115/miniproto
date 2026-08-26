---
title: "miniproto.auth.service.AuthService.handle_dc_migration"
description: "Persist Telegram's requested DC migration and export user authorization when needed."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.service.AuthService.handle_dc_migration"
source_path: "src/miniproto/auth/service.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/service.py#L225"
aliases: ["miniproto.AuthService.handle_dc_migration","miniproto.auth.AuthService.handle_dc_migration"]
module: "miniproto.auth.service"
---

## `miniproto.auth.service.AuthService.handle_dc_migration`

```python
handle_dc_migration(error: DatacenterMigration) -> types.AuthExportedAuthorization | None
```

Persist Telegram's requested DC migration and export user authorization when needed.

An unauthenticated session only changes its target DC. An authenticated session also
obtains an exported authorization, which the caller must import through a sender for
the target DC.

**Parameters:**

- **error** (<code>[DatacenterMigration](#miniproto.errors.DatacenterMigration)</code>) – Classified Telegram migration response with the target ``dc_id``.

**Returns:**

- <code>[AuthExportedAuthorization](#miniproto.raw.types.AuthExportedAuthorization) | None</code> – An exported authorization for authenticated sessions, otherwise ``None``.

**Raises:**

- <code>[InvalidDatacenter](#miniproto.errors.InvalidDatacenter)</code> – If Telegram requests the already-selected DC.
