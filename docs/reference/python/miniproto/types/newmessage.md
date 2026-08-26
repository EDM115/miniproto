---
title: "miniproto.types.NewMessage"
description: "Update emitted for a newly received message."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.types.NewMessage"
source_path: "src/miniproto/types.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/types.py#L138"
aliases: ["miniproto.NewMessage"]
module: "miniproto.types"
---

## `miniproto.types.NewMessage`

```python
NewMessage(date: datetime = _utc_now(), raw: object | None = None, message: Message | None = None, metadata: dict[str, Any] = dict()) -> None
```

Bases: <code>[Update](#miniproto.types.Update)</code>

Update emitted for a newly received message.

**Attributes:**

- [**date**](#miniproto.types.NewMessage.date) (<code>[datetime](#datetime.datetime)</code>) – Inherited update timestamp, generated as current UTC time when omitted.
- [**raw**](#miniproto.types.NewMessage.raw) (<code>[object](#object) | None</code>) – Inherited optional original Telegram TL object.
- [**message**](#miniproto.types.NewMessage.message) (<code>[Message](#miniproto.types.Message) | None</code>) – Normalized message when conversion succeeded.
- [**metadata**](#miniproto.types.NewMessage.metadata) (<code>[dict](#dict)[[str](#str), [Any](#typing.Any)]</code>) – Additional update-specific values.
