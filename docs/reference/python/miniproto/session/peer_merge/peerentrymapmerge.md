---
title: "miniproto.session.peer_merge.PeerEntryMapMerge"
description: "Merged peer map plus keys needed for incremental index reconciliation."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.session.peer_merge.PeerEntryMapMerge"
source_path: "src/miniproto/session/peer_merge.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/peer_merge.py#L14"
module: "miniproto.session.peer_merge"
---

## `miniproto.session.peer_merge.PeerEntryMapMerge`

```python
PeerEntryMapMerge(entries: dict[PeerKey, PeerCacheEntry], affected_keys: tuple[PeerKey, ...], canonical_affected_keys: tuple[PeerKey, ...], appended_keys: tuple[PeerKey, ...]) -> None
```

Merged peer map plus keys needed for incremental index reconciliation.

**Attributes:**

- [**entries**](#miniproto.session.peer_merge.PeerEntryMapMerge.entries) (<code>[dict](#dict)[[PeerKey](#miniproto.session.peer_merge.PeerKey), [PeerCacheEntry](#miniproto.session.models.PeerCacheEntry)]</code>) – Canonical peer map after applying incoming entries.
- [**affected_keys**](#miniproto.session.peer_merge.PeerEntryMapMerge.affected_keys) (<code>[tuple](#tuple)[[PeerKey](#miniproto.session.peer_merge.PeerKey), ...]</code>) – Input keys whose updates may require index reconciliation.
- [**canonical_affected_keys**](#miniproto.session.peer_merge.PeerEntryMapMerge.canonical_affected_keys) (<code>[tuple](#tuple)[[PeerKey](#miniproto.session.peer_merge.PeerKey), ...]</code>) – Existing canonical keys affected by updates.
- [**appended_keys**](#miniproto.session.peer_merge.PeerEntryMapMerge.appended_keys) (<code>[tuple](#tuple)[[PeerKey](#miniproto.session.peer_merge.PeerKey), ...]</code>) – Canonical keys newly appended to the map.
