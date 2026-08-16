---
title: "attachMenuBotsNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "attachMenuBotsNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xf1d88a5c"
---

# `attachMenuBotsNotModified`

No description provided by the pinned schema.

## Signature

```tl
attachMenuBotsNotModified#f1d88a5c = AttachMenuBots;
```

## Result type

`AttachMenuBots`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import AttachMenuBotsNotModified
```

Public access: `miniproto.raw.types.AttachMenuBotsNotModified`.

## Safe usage shape

```python
from miniproto.raw.types import AttachMenuBotsNotModified

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AttachMenuBotsNotModified
```

## Result family

[`AttachMenuBots`](/reference/telegram/types/results/attach-menu-bots/)

## Relationships

- Result family: [`AttachMenuBots`](/reference/telegram/types/results/attach-menu-bots/)
- Related constructors: [`attachMenuBots`](/reference/telegram/types/base/attach-menu-bots/)
- Returned by: [`messages.getAttachMenuBots`](/reference/telegram/functions/messages/get-attach-menu-bots/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
