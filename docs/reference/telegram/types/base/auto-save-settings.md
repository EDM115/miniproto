---
title: "autoSaveSettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "autoSaveSettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xc84834ce"
---

# `autoSaveSettings`

No description provided by the pinned schema.

## Signature

```tl
autoSaveSettings#c84834ce flags:# photos:flags.0?true videos:flags.1?true video_max_size:flags.2?long = AutoSaveSettings;
```

## Result type

`AutoSaveSettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| photos | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| videos | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| video_max_size | flags.2?long | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| photos | 0 | Controlled by `flags`; present when this bit is set. |
| videos | 1 | Controlled by `flags`; present when this bit is set. |
| video_max_size | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import AutoSaveSettings
```

Public access: `miniproto.raw.types.AutoSaveSettings`.

## Safe usage shape

```python
from miniproto.raw.types import AutoSaveSettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AutoSaveSettings
```

## Result family

[`AutoSaveSettings`](/reference/telegram/types/results/auto-save-settings/)

## Relationships

- Result family: [`AutoSaveSettings`](/reference/telegram/types/results/auto-save-settings/)
- Accepted by: [`account.saveAutoSaveSettings`](/reference/telegram/functions/account/save-auto-save-settings/), [`account.autoSaveSettings`](/reference/telegram/types/account/auto-save-settings/), [`autoSaveException`](/reference/telegram/types/base/auto-save-exception/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
