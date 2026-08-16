---
title: "miniproto.peers.input_channel_from_peer"
description: "Convert a hash-bearing channel peer to MTProto ``InputChannel``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.peers.input_channel_from_peer"
source_path: "src/miniproto/peers.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/peers.py#L618"
module: "miniproto.peers"
---

## `miniproto.peers.input_channel_from_peer`

```python
input_channel_from_peer(peer: Peer) -> object
```

Convert a hash-bearing channel peer to MTProto ``InputChannel``.

**Raises:**

- <code>[NotFound](#miniproto.errors.NotFound)</code> – If ``peer`` is not a channel with an access hash.

**Parameters:**

- **peer** (<code>[Peer](#miniproto.types.Peer)</code>) – Resolved channel peer to convert.
