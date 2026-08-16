---
title: "miniproto.session.peer_merge"
description: "Merge durable peer cache entries without discarding richer known metadata."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.session.peer_merge"
source_path: "src/miniproto/session/peer_merge.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/peer_merge.py"
module: "miniproto.session.peer_merge"
---

## `miniproto.session.peer_merge`

Merge durable peer cache entries without discarding richer known metadata.

## Public objects

- [`PeerKey`](./peerkey/) — Public attribute `miniproto.session.peer_merge.PeerKey`.
- [`PeerEntryMapMerge`](./peerentrymapmerge/) — Merged peer map plus keys needed for incremental index reconciliation.
- [`merge_peer_entry`](./merge-peer-entry/) — Prefer fresh fields while retaining existing hashes and populated metadata.
- [`merge_peer_entries`](./merge-peer-entries/) — Merge peer collections into canonical map insertion order.
- [`merge_peer_entry_map`](./merge-peer-entry-map/) — Merge peer collections into a map keyed by kind and Telegram ID.
- [`merge_peer_entry_map_with_metadata`](./merge-peer-entry-map-with-metadata/) — Merge entries and report affected, canonical, and newly appended keys.
