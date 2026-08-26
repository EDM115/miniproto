---
title: "miniproto.peers.input_peer_from_peer"
description: "Convert a resolved peer to its MTProto ``InputPeer`` representation."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.peers.input_peer_from_peer"
source_path: "src/miniproto/peers.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/peers.py#L578"
module: "miniproto.peers"
---

## `miniproto.peers.input_peer_from_peer`

```python
input_peer_from_peer(peer: Peer) -> object
```

Convert a resolved peer to its MTProto ``InputPeer`` representation.

Chats need no hash; users and channels must carry a cached access hash.

**Raises:**

- <code>[NotFound](#miniproto.errors.NotFound)</code> – If the peer kind is unsupported or its required hash is absent.

**Parameters:**

- **peer** (<code>[Peer](#miniproto.types.Peer)</code>) – Resolved public peer to convert.
