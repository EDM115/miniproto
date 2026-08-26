---
title: "miniproto.types.Update"
description: "Base normalized update with a UTC creation timestamp and optional raw payload."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.types.Update"
source_path: "src/miniproto/types.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/types.py#L125"
aliases: ["miniproto.Update"]
module: "miniproto.types"
---

## `miniproto.types.Update`

```python
Update(date: datetime = _utc_now(), raw: object | None = None) -> None
```

Base normalized update with a UTC creation timestamp and optional raw payload.

**Attributes:**

- [**date**](#miniproto.types.Update.date) (<code>[datetime](#datetime.datetime)</code>) – Time associated with the update, generated as current UTC time when omitted.
- [**raw**](#miniproto.types.Update.raw) (<code>[object](#object) | None</code>) – Optional original Telegram TL object retained for low-level inspection.
