---
title: "miniproto.session.peer_merge"
description: "Merge durable peer entries according to full-entity and partial-entity metadata rules."
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

Merge durable peer entries according to full-entity and partial-entity metadata rules.

## Public objects

- [`PeerKey`](./peerkey/) — Public attribute `miniproto.session.peer_merge.PeerKey`.
- [`PeerEntryMapMerge`](./peerentrymapmerge/) — Merged peer map plus keys needed for incremental index reconciliation.
- [`merge_peer_entry`](./merge-peer-entry/) — Apply incoming peer metadata while preserving a missing access hash.
- [`merge_peer_entries`](./merge-peer-entries/) — Merge peer collections into canonical map insertion order.
- [`merge_peer_entry_map`](./merge-peer-entry-map/) — Merge peer collections into a map keyed by kind and Telegram ID.
- [`merge_peer_entry_map_with_metadata`](./merge-peer-entry-map-with-metadata/) — Merge entries and report affected, canonical and newly appended keys.
