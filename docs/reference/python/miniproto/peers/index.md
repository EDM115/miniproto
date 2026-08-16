---
title: "miniproto.peers"
description: "Resolve, normalize, and persist Telegram peers with revision-aware indexes."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.peers"
source_path: "src/miniproto/peers.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/peers.py"
module: "miniproto.peers"
---

## `miniproto.peers`

Resolve, normalize, and persist Telegram peers with revision-aware indexes.

## Public objects

- [`PeerCache`](./peercache/) — Revision-aware session peer cache with local and remote resolution paths.
- [`input_peer_from_peer`](./input-peer-from-peer/) — Convert a resolved peer to its MTProto ``InputPeer`` representation.
- [`input_user_from_peer`](./input-user-from-peer/) — Convert self or a hash-bearing user peer to MTProto ``InputUser``.
- [`input_channel_from_peer`](./input-channel-from-peer/) — Convert a hash-bearing channel peer to MTProto ``InputChannel``.
