---
title: "miniproto.types.Message"
description: "Normalized Telegram message returned by high-level messaging helpers."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.types.Message"
source_path: "src/miniproto/types.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/types.py#L102"
aliases: ["miniproto.Message"]
module: "miniproto.types"
---

## `miniproto.types.Message`

```python
Message(id: int, peer: Peer, text: str, date: datetime, media: Media | None = None, entities: tuple[object, ...] = (), raw: object | None = None) -> None
```

Normalized Telegram message returned by high-level messaging helpers.

**Attributes:**

- [**id**](#miniproto.types.Message.id) (<code>[int](#int)</code>) – Telegram message identifier within ``peer``.
- [**peer**](#miniproto.types.Message.peer) (<code>[Peer](#miniproto.types.Peer)</code>) – Conversation containing the message.
- [**text**](#miniproto.types.Message.text) (<code>[str](#str)</code>) – Parsed message text.
- [**date**](#miniproto.types.Message.date) (<code>[datetime](#datetime.datetime)</code>) – Telegram timestamp.
- [**media**](#miniproto.types.Message.media) (<code>[Media](#miniproto.types.Media) | None</code>) – Optional normalized attachment.
- [**entities**](#miniproto.types.Message.entities) (<code>[tuple](#tuple)[[object](#object), ...]</code>) – Parsed text entities.
- [**raw**](#miniproto.types.Message.raw) (<code>[object](#object) | None</code>) – Optional underlying TL message.
