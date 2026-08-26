---
title: "botInfo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "botInfo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x4d8a0299"
---

# `botInfo`

No description provided by the pinned schema.

## Signature

```tl
botInfo#4d8a0299 flags:# has_preview_medias:flags.6?true user_id:flags.0?long description:flags.1?string description_photo:flags.4?Photo description_document:flags.5?Document commands:flags.2?Vector<BotCommand> menu_button:flags.3?BotMenuButton privacy_policy_url:flags.7?string app_settings:flags.8?BotAppSettings verifier_settings:flags.9?BotVerifierSettings = BotInfo;
```

## Result type

`BotInfo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| has_preview_medias | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| user_id | flags.0?long | flags.0 | — | No description provided by the pinned schema. |
| description | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| description_photo | flags.4?Photo | flags.4 | — | No description provided by the pinned schema. |
| description_document | flags.5?Document | flags.5 | — | No description provided by the pinned schema. |
| commands | flags.2?Vector<BotCommand> | flags.2 | — | No description provided by the pinned schema. |
| menu_button | flags.3?BotMenuButton | flags.3 | — | No description provided by the pinned schema. |
| privacy_policy_url | flags.7?string | flags.7 | — | No description provided by the pinned schema. |
| app_settings | flags.8?BotAppSettings | flags.8 | — | No description provided by the pinned schema. |
| verifier_settings | flags.9?BotVerifierSettings | flags.9 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| has_preview_medias | 6 | Controlled by `flags`; present when this bit is set. |
| user_id | 0 | Controlled by `flags`; present when this bit is set. |
| description | 1 | Controlled by `flags`; present when this bit is set. |
| description_photo | 4 | Controlled by `flags`; present when this bit is set. |
| description_document | 5 | Controlled by `flags`; present when this bit is set. |
| commands | 2 | Controlled by `flags`; present when this bit is set. |
| menu_button | 3 | Controlled by `flags`; present when this bit is set. |
| privacy_policy_url | 7 | Controlled by `flags`; present when this bit is set. |
| app_settings | 8 | Controlled by `flags`; present when this bit is set. |
| verifier_settings | 9 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import BotInfo
```

Public access: `miniproto.raw.types.BotInfo`.

## Safe usage shape

```python
from miniproto.raw.types import BotInfo

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotInfo
```

## Result family

[`BotInfo`](/reference/telegram/types/results/bot-info/)

## Relationships

- Result family: [`BotInfo`](/reference/telegram/types/results/bot-info/)
- Accepted by: [`channelFull`](/reference/telegram/types/base/channel-full/), [`chatFull`](/reference/telegram/types/base/chat-full/), [`userFull`](/reference/telegram/types/base/user-full/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
