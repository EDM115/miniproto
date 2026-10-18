---
title: "miniproto.session.peer_merge.merge_peer_entry"
description: "Apply incoming peer metadata while preserving a missing access hash."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.peer_merge.merge_peer_entry"
source_path: "src/miniproto/session/peer_merge.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/peer_merge.py#L43"
module: "miniproto.session.peer_merge"
---

## `miniproto.session.peer_merge.merge_peer_entry`

```python
merge_peer_entry(current: PeerCacheEntry, incoming: PeerCacheEntry) -> PeerCacheEntry
```

Apply incoming peer metadata while preserving a missing access hash.

A full entry marked ``_miniproto_complete`` replaces raw metadata and may clear username or phone values. Partial entries retain existing values where incoming aliases are empty, including their original alias observation times. An internal full-observation revision advances on full merges and survives partial merges, preserving knowledge of absent aliases.

**Parameters:**

- **current** (<code>[PeerCacheEntry](#miniproto.session.models.PeerCacheEntry)</code>) – Existing canonical peer cache entry.
- **incoming** (<code>[PeerCacheEntry](#miniproto.session.models.PeerCacheEntry)</code>) – New entry whose completeness marker determines whether missing aliases clear existing values.
