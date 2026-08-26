---
title: "miniproto.session.peer_merge.merge_peer_entry_map_with_metadata"
description: "Merge entries and report affected, canonical and newly appended keys."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.peer_merge.merge_peer_entry_map_with_metadata"
source_path: "src/miniproto/session/peer_merge.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/peer_merge.py#L77"
module: "miniproto.session.peer_merge"
---

## `miniproto.session.peer_merge.merge_peer_entry_map_with_metadata`

```python
merge_peer_entry_map_with_metadata(existing: Iterable[PeerCacheEntry], incoming: Iterable[PeerCacheEntry]) -> PeerEntryMapMerge
```

Merge entries and report affected, canonical and newly appended keys.

Self entries replace an equivalent user key, preserving the cache's single
canonical representation for the authenticated account.

**Parameters:**

- **existing** (<code>[Iterable](#collections.abc.Iterable)[[PeerCacheEntry](#miniproto.session.models.PeerCacheEntry)]</code>) – Current peer entries in insertion order.
- **incoming** (<code>[Iterable](#collections.abc.Iterable)[[PeerCacheEntry](#miniproto.session.models.PeerCacheEntry)]</code>) – New peer entries whose effects are tracked.
