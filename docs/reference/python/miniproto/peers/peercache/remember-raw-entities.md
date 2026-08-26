---
title: "miniproto.peers.PeerCache.remember_raw_entities"
description: "Extract peer-bearing raw objects and merge their cache entries durably."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.peers.PeerCache.remember_raw_entities"
source_path: "src/miniproto/peers.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/peers.py#L172"
module: "miniproto.peers"
---

## `miniproto.peers.PeerCache.remember_raw_entities`

```python
remember_raw_entities(raw: object) -> None
```

Extract peer-bearing raw objects and merge their cache entries durably.

**Parameters:**

- **raw** (<code>[object](#object)</code>) – Raw Telegram object, container or sequence that may expose users/chats.
