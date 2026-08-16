---
title: "miniproto.types.Peer"
description: "Telegram peer reference suitable for high-level client operations."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.types.Peer"
source_path: "src/miniproto/types.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/types.py#L17"
aliases: ["miniproto.Peer"]
module: "miniproto.types"
---

## `miniproto.types.Peer`

```python
Peer(id: int, kind: PeerKind, access_hash: int | None = None) -> None
```

Telegram peer reference suitable for high-level client operations.

**Attributes:**

- [**id**](#miniproto.types.Peer.id) (<code>[int](#int)</code>) – Telegram peer identifier.
- [**kind**](#miniproto.types.Peer.kind) (<code>[PeerKind](#miniproto.types.PeerKind)</code>) – Peer category: user, chat, channel, or the current account.
- [**access_hash**](#miniproto.types.Peer.access_hash) (<code>[int](#int) | None</code>) – Optional Telegram access hash required for some peers.
