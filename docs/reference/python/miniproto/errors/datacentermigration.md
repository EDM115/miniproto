---
title: "miniproto.errors.DatacenterMigration"
description: "Telegram directs the request to ``dc_id`` for a named migration kind."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.errors.DatacenterMigration"
source_path: "src/miniproto/errors.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/errors.py#L468"
aliases: ["miniproto.DatacenterMigration"]
module: "miniproto.errors"
---

## `miniproto.errors.DatacenterMigration`

```python
DatacenterMigration(dc_id: int, *, kind: str = 'MIGRATE', message: str | None = None, request: object | None = None, context: Mapping[str, Any] | None = None) -> None
```

Bases: <code>[InvalidDatacenter](#miniproto.errors.InvalidDatacenter)</code>

Telegram directs the request to ``dc_id`` for a named migration kind.

Create a migration error from the target DC and migration kind.

**Parameters:**

- **dc_id** (<code>[int](#int)</code>) – Target Telegram data-center ID.
- **kind** (<code>[str](#str)</code>) – Migration family extracted from Telegram's symbolic error name.
- **message** (<code>[str](#str) | None</code>) – Optional raw error text; a migration name is generated when absent.
- **request** (<code>[object](#object) | None</code>) – Optional request that Telegram directed to another DC.
- **context** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)] | None</code>) – Optional secret-safe diagnostic metadata.
