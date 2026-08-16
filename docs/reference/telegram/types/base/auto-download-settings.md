---
title: "autoDownloadSettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "autoDownloadSettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xbaa57628"
---

# `autoDownloadSettings`

No description provided by the pinned schema.

## Signature

```tl
autoDownloadSettings#baa57628 flags:# disabled:flags.0?true video_preload_large:flags.1?true audio_preload_next:flags.2?true phonecalls_less_data:flags.3?true stories_preload:flags.4?true photo_size_max:int video_size_max:long file_size_max:long video_upload_maxbitrate:int small_queue_active_operations_max:int large_queue_active_operations_max:int = AutoDownloadSettings;
```

## Result type

`AutoDownloadSettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| disabled | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| video_preload_large | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| audio_preload_next | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| phonecalls_less_data | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| stories_preload | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| photo_size_max | int | — | — | No description provided by the pinned schema. |
| video_size_max | long | — | — | No description provided by the pinned schema. |
| file_size_max | long | — | — | No description provided by the pinned schema. |
| video_upload_maxbitrate | int | — | — | No description provided by the pinned schema. |
| small_queue_active_operations_max | int | — | — | No description provided by the pinned schema. |
| large_queue_active_operations_max | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| disabled | 0 | Controlled by `flags`; present when this bit is set. |
| video_preload_large | 1 | Controlled by `flags`; present when this bit is set. |
| audio_preload_next | 2 | Controlled by `flags`; present when this bit is set. |
| phonecalls_less_data | 3 | Controlled by `flags`; present when this bit is set. |
| stories_preload | 4 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import AutoDownloadSettings
```

Public access: `miniproto.raw.types.AutoDownloadSettings`.

## Safe usage shape

```python
from miniproto.raw.types import AutoDownloadSettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AutoDownloadSettings
```

## Result family

[`AutoDownloadSettings`](/reference/telegram/types/results/auto-download-settings/)

## Relationships

- Result family: [`AutoDownloadSettings`](/reference/telegram/types/results/auto-download-settings/)
- Accepted by: [`account.saveAutoDownloadSettings`](/reference/telegram/functions/account/save-auto-download-settings/), [`account.autoDownloadSettings`](/reference/telegram/types/account/auto-download-settings/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
