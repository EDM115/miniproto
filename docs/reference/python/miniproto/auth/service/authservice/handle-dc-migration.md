---
title: "miniproto.auth.service.AuthService.handle_dc_migration"
description: "Prepare Telegram's requested DC migration without changing the active session."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.service.AuthService.handle_dc_migration"
source_path: "src/miniproto/auth/service.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/service.py#L226"
aliases: ["miniproto.AuthService.handle_dc_migration","miniproto.auth.AuthService.handle_dc_migration"]
module: "miniproto.auth.service"
---

## `miniproto.auth.service.AuthService.handle_dc_migration`

```python
handle_dc_migration(error: DatacenterMigration) -> types.AuthExportedAuthorization | None
```

Prepare Telegram's requested DC migration without changing the active session.

Authenticated sessions export authorization through the source DC. The caller must prepare the target key, import the authorization when present and atomically activate the target DC, key and salt only after preparation succeeds.

**Parameters:**

- **error** (<code>[DatacenterMigration](#miniproto.errors.DatacenterMigration)</code>) – Classified Telegram migration response with the target ``dc_id``.

**Returns:**

- <code>[AuthExportedAuthorization](#miniproto.raw.types.AuthExportedAuthorization) | None</code> – An exported authorization for authenticated sessions, otherwise ``None``.

**Raises:**

- <code>[InvalidDatacenter](#miniproto.errors.InvalidDatacenter)</code> – If Telegram requests the already-selected DC.
