---
title: "miniproto.peers.PeerCache.resolve_input_peer"
description: "Resolve a reference then return the matching MTProto ``InputPeer``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.peers.PeerCache.resolve_input_peer"
source_path: "src/miniproto/peers.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/peers.py#L161"
module: "miniproto.peers"
---

## `miniproto.peers.PeerCache.resolve_input_peer`

```python
resolve_input_peer(peer: Peer | str | int) -> object
```

Resolve a reference then return the matching MTProto ``InputPeer``.

**Raises:**

- <code>[NotFound](#miniproto.errors.NotFound)</code> – If resolution fails or the resolved peer needs an uncached hash.

**Parameters:**

- **peer** (<code>[Peer](#miniproto.types.Peer) | [str](#str) | [int](#int)</code>) – Any reference accepted by :meth:`resolve_peer`.
