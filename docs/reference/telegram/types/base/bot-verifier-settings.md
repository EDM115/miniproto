---
title: "botVerifierSettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "botVerifierSettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xb0cd6617"
---

# `botVerifierSettings`

No description provided by the pinned schema.

## Signature

```tl
botVerifierSettings#b0cd6617 flags:# can_modify_custom_description:flags.1?true icon:long company:string custom_description:flags.0?string = BotVerifierSettings;
```

## Result type

`BotVerifierSettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| can_modify_custom_description | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| icon | long | — | — | No description provided by the pinned schema. |
| company | string | — | — | No description provided by the pinned schema. |
| custom_description | flags.0?string | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| can_modify_custom_description | 1 | Controlled by `flags`; present when this bit is set. |
| custom_description | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import BotVerifierSettings
```

Public access: `miniproto.raw.types.BotVerifierSettings`.

## Safe usage shape

```python
from miniproto.raw.types import BotVerifierSettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotVerifierSettings
```

## Result family

[`BotVerifierSettings`](/reference/telegram/types/results/bot-verifier-settings/)

## Relationships

- Result family: [`BotVerifierSettings`](/reference/telegram/types/results/bot-verifier-settings/)
- Accepted by: [`botInfo`](/reference/telegram/types/base/bot-info/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
