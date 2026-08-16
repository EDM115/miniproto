---
title: "connectedBot"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "connectedBot"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x033ed001"
---

# `connectedBot`

No description provided by the pinned schema.

## Signature

```tl
connectedBot#033ed001 flags:# bot_id:long recipients:BusinessBotRecipients rights:BusinessBotRights device:flags.0?string date:flags.1?int location:flags.2?string = ConnectedBot;
```

## Result type

`ConnectedBot`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| bot_id | long | — | — | No description provided by the pinned schema. |
| recipients | BusinessBotRecipients | — | — | No description provided by the pinned schema. |
| rights | BusinessBotRights | — | — | No description provided by the pinned schema. |
| device | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| date | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| location | flags.2?string | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| device | 0 | Controlled by `flags`; present when this bit is set. |
| date | 1 | Controlled by `flags`; present when this bit is set. |
| location | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ConnectedBot
```

Public access: `miniproto.raw.types.ConnectedBot`.

## Safe usage shape

```python
from miniproto.raw.types import ConnectedBot

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ConnectedBot
```

## Result family

[`ConnectedBot`](/reference/telegram/types/results/connected-bot/)

## Relationships

- Result family: [`ConnectedBot`](/reference/telegram/types/results/connected-bot/)
- Accepted by: [`account.connectedBots`](/reference/telegram/types/account/connected-bots/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
