---
title: "miniproto.types"
description: "Small immutable public value types produced by high-level client helpers."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.types"
source_path: "src/miniproto/types.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/types.py"
module: "miniproto.types"
---

## `miniproto.types`

Small immutable public value types produced by high-level client helpers.

## Public objects

- [`PeerKind`](./peerkind/) — Public attribute `miniproto.types.PeerKind`.
- [`Peer`](./peer/) — Telegram peer reference suitable for high-level client operations.
- [`User`](./user/) — Normalized Telegram user returned by peer and authorization helpers.
- [`Media`](./media/) — Normalized Telegram media descriptor used for upload and download helpers.
- [`Message`](./message/) — Normalized Telegram message returned by high-level messaging helpers.
- [`Update`](./update/) — Base normalized update with a UTC creation timestamp and optional raw payload.
- [`NewMessage`](./newmessage/) — Update emitted for a newly received message.
