---
title: "miniproto.session.peer_merge.merge_peer_entry"
description: "Prefer fresh fields while retaining existing hashes and populated metadata."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.peer_merge.merge_peer_entry"
source_path: "src/miniproto/session/peer_merge.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/peer_merge.py#L31"
module: "miniproto.session.peer_merge"
---

## `miniproto.session.peer_merge.merge_peer_entry`

```python
merge_peer_entry(current: PeerCacheEntry, incoming: PeerCacheEntry) -> PeerCacheEntry
```

Prefer fresh fields while retaining existing hashes and populated metadata.

**Parameters:**

- **current** (<code>[PeerCacheEntry](#miniproto.session.models.PeerCacheEntry)</code>) – Existing canonical peer cache entry.
- **incoming** (<code>[PeerCacheEntry](#miniproto.session.models.PeerCacheEntry)</code>) – New entry whose populated fields take precedence.
