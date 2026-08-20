---
title: "miniproto.session.peer_merge.merge_peer_entries"
description: "Merge peer collections into canonical map insertion order."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.peer_merge.merge_peer_entries"
source_path: "src/miniproto/session/peer_merge.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/peer_merge.py#L53"
module: "miniproto.session.peer_merge"
---

## `miniproto.session.peer_merge.merge_peer_entries`

```python
merge_peer_entries(existing: Iterable[PeerCacheEntry], incoming: Iterable[PeerCacheEntry]) -> tuple[PeerCacheEntry, ...]
```

Merge peer collections into canonical map insertion order.

**Parameters:**

- **existing** (<code>[Iterable](#collections.abc.Iterable)[[PeerCacheEntry](#miniproto.session.models.PeerCacheEntry)]</code>) – Current peer entries in canonical order.
- **incoming** (<code>[Iterable](#collections.abc.Iterable)[[PeerCacheEntry](#miniproto.session.models.PeerCacheEntry)]</code>) – New peer entries to merge.
