---
title: "miniproto.session.peer_merge.merge_peer_entry_map"
description: "Merge peer collections into a map keyed by kind and Telegram ID."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.peer_merge.merge_peer_entry_map"
source_path: "src/miniproto/session/peer_merge.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/peer_merge.py#L65"
module: "miniproto.session.peer_merge"
---

## `miniproto.session.peer_merge.merge_peer_entry_map`

```python
merge_peer_entry_map(existing: Iterable[PeerCacheEntry], incoming: Iterable[PeerCacheEntry]) -> dict[PeerKey, PeerCacheEntry]
```

Merge peer collections into a map keyed by kind and Telegram ID.

**Parameters:**

- **existing** (<code>[Iterable](#collections.abc.Iterable)[[PeerCacheEntry](#miniproto.session.models.PeerCacheEntry)]</code>) – Current peer entries.
- **incoming** (<code>[Iterable](#collections.abc.Iterable)[[PeerCacheEntry](#miniproto.session.models.PeerCacheEntry)]</code>) – New peer entries to merge.
