---
title: "miniproto.peers.PeerCache.get_me"
description: "Return the authenticated user, reading cache unless ``refresh`` is true."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.peers.PeerCache.get_me"
source_path: "src/miniproto/peers.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/peers.py#L101"
module: "miniproto.peers"
---

## `miniproto.peers.PeerCache.get_me`

```python
get_me(*, refresh: bool = False) -> User
```

Return the authenticated user, reading cache unless ``refresh`` is true.

**Parameters:**

- **refresh** (<code>[bool](#bool)</code>) – When true, try ``users.getUsers(inputUserSelf)`` first. If
its result lacks a self user, return a cached identity when one
exists; otherwise raise ``Unauthorized``.

**Raises:**

- <code>[Unauthorized](#miniproto.errors.Unauthorized)</code> – If Telegram does not return a concrete self user and
no cached identity is available.
