---
title: "miniproto.client.Client.resolve_peer"
description: "Resolve a peer object, numeric ID, or username to a normalized ``Peer``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.resolve_peer"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L616"
aliases: ["miniproto.Client.resolve_peer"]
module: "miniproto.client"
---

## `miniproto.client.Client.resolve_peer`

```python
resolve_peer(peer: Peer | str | int) -> Peer
```

Resolve a peer object, numeric ID, or username to a normalized ``Peer``.

**Parameters:**

- **peer** (<code>[Peer](#miniproto.types.Peer) | [str](#str) | [int](#int)</code>) – Existing normalized peer, numeric identifier, or username to resolve through the peer cache.

**Raises:**

- <code>[Exception](#Exception)</code> – Propagates resolution failures such as missing access data or invalid usernames.
