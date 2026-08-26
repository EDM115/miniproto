---
title: "miniproto.peers.PeerCache.resolve_peer"
description: "Resolve a peer object, numeric ID, phone number, self alias or username."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.peers.PeerCache.resolve_peer"
source_path: "src/miniproto/peers.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/peers.py#L131"
module: "miniproto.peers"
---

## `miniproto.peers.PeerCache.resolve_peer`

```python
resolve_peer(peer: Peer | str | int) -> Peer
```

Resolve a peer object, numeric ID, phone number, self alias or username.

Numeric IDs use cached peers first, then seed from dialogs. Usernames may
call Telegram after the 24-hour local username cache expires.

**Raises:**

- <code>[NotFound](#miniproto.errors.NotFound)</code> – If the reference is empty, unknown or lacks an access hash.
- <code>[RpcError](#miniproto.errors.RpcError)</code> – If remote username resolution returns an unexpected result.

**Parameters:**

- **peer** (<code>[Peer](#miniproto.types.Peer) | [str](#str) | [int](#int)</code>) – Existing peer, signed/numeric ID, self alias, phone or username.
