---
title: "miniproto.peers.PeerCache.resolve_peer"
description: "Resolve a peer object, numeric ID, phone number, self alias or username."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.peers.PeerCache.resolve_peer"
source_path: "src/miniproto/peers.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/peers.py#L128"
module: "miniproto.peers"
---

## `miniproto.peers.PeerCache.resolve_peer`

```python
resolve_peer(peer: Peer | str | int) -> Peer
```

Resolve a peer object, numeric ID, phone number, self alias or username.

Numeric IDs use cached peers first, then seed from up to 100 unpinned dialogs. Usernames call Telegram when no fresh entry exists in the 24-hour cache. Phone references beginning with ``+`` use cached data only.

Positive IDs shared by several kinds prefer self, user, chat, then channel. Negative chat IDs use ``-id``, channel IDs use ``-(1_000_000_000_000 + id)``.

**Raises:**

- <code>[NotFound](#miniproto.errors.NotFound)</code> – If the reference is empty or unknown, or an explicit user/channel ``Peer`` requires an uncached access hash.
- <code>[RpcError](#miniproto.errors.RpcError)</code> – If remote username resolution returns an unexpected result.

**Parameters:**

- **peer** (<code>[Peer](#miniproto.types.Peer) | [str](#str) | [int](#int)</code>) – Existing peer, signed/numeric ID, self alias, phone or username.

**Returns:**

- <code>[Peer](#miniproto.types.Peer)</code> – The resolved peer. Numeric, phone and username paths can return an entry without an access hash. ``resolve_input_peer`` checks it before constructing an input peer.
