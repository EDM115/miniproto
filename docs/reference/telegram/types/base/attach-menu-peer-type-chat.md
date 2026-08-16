---
title: "attachMenuPeerTypeChat"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "attachMenuPeerTypeChat"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x0509113f"
---

# `attachMenuPeerTypeChat`

No description provided by the pinned schema.

## Signature

```tl
attachMenuPeerTypeChat#0509113f = AttachMenuPeerType;
```

## Result type

`AttachMenuPeerType`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import AttachMenuPeerTypeChat
```

Public access: `miniproto.raw.types.AttachMenuPeerTypeChat`.

## Safe usage shape

```python
from miniproto.raw.types import AttachMenuPeerTypeChat

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AttachMenuPeerTypeChat
```

## Result family

[`AttachMenuPeerType`](/reference/telegram/types/results/attach-menu-peer-type/)

## Relationships

- Result family: [`AttachMenuPeerType`](/reference/telegram/types/results/attach-menu-peer-type/)
- Related constructors: [`attachMenuPeerTypeBotPM`](/reference/telegram/types/base/attach-menu-peer-type-bot-pm/), [`attachMenuPeerTypeBroadcast`](/reference/telegram/types/base/attach-menu-peer-type-broadcast/), [`attachMenuPeerTypePM`](/reference/telegram/types/base/attach-menu-peer-type-pm/), [`attachMenuPeerTypeSameBotPM`](/reference/telegram/types/base/attach-menu-peer-type-same-bot-pm/)
- Accepted by: [`attachMenuBot`](/reference/telegram/types/base/attach-menu-bot/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
