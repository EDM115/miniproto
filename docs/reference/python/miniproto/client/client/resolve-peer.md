---
title: "miniproto.client.Client.resolve_peer"
description: "Resolve a peer object, numeric ID, username, self alias or cached phone number."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.resolve_peer"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L643"
aliases: ["miniproto.Client.resolve_peer"]
module: "miniproto.client"
---

## `miniproto.client.Client.resolve_peer`

```python
resolve_peer(peer: Peer | str | int) -> Peer
```

Resolve a peer object, numeric ID, username, self alias or cached phone number.

**Parameters:**

- **peer** (<code>[Peer](#miniproto.types.Peer) | [str](#str) | [int](#int)</code>) – Existing peer, signed numeric ID, username or t.me URL, self alias such as ``"me"``, or phone reference beginning with ``+``. Phone lookup requires cached data. Missing numeric IDs trigger a lookup of up to 100 unpinned dialogs.

**Returns:**

- <code>[Peer](#miniproto.types.Peer)</code> – A ``Peer`` identifying the conversation. Numeric and username lookup can return a peer without an access hash. Input-peer conversion rejects users/channels without one.

**Raises:**

- <code>[Exception](#Exception)</code> – Propagates resolution failures such as missing access data or invalid usernames.
