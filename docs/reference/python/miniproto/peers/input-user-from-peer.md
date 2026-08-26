---
title: "miniproto.peers.input_user_from_peer"
description: "Convert self or a hash-bearing user peer to MTProto ``InputUser``."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.peers.input_user_from_peer"
source_path: "src/miniproto/peers.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/peers.py#L602"
module: "miniproto.peers"
---

## `miniproto.peers.input_user_from_peer`

```python
input_user_from_peer(peer: Peer) -> object
```

Convert self or a hash-bearing user peer to MTProto ``InputUser``.

**Raises:**

- <code>[NotFound](#miniproto.errors.NotFound)</code> – If ``peer`` is not self or a user with an access hash.

**Parameters:**

- **peer** (<code>[Peer](#miniproto.types.Peer)</code>) – Self or resolved user peer to convert.
