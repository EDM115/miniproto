---
title: "botPreviewMedia"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "botPreviewMedia"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x23e91ba3"
---

# `botPreviewMedia`

No description provided by the pinned schema.

## Signature

```tl
botPreviewMedia#23e91ba3 date:int media:MessageMedia = BotPreviewMedia;
```

## Result type

`BotPreviewMedia`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| date | int | — | — | No description provided by the pinned schema. |
| media | MessageMedia | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import BotPreviewMedia
```

Public access: `miniproto.raw.types.BotPreviewMedia`.

## Safe usage shape

```python
from miniproto.raw.types import BotPreviewMedia

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BotPreviewMedia
```

## Result family

[`BotPreviewMedia`](/reference/telegram/types/results/bot-preview-media/)

## Relationships

- Result family: [`BotPreviewMedia`](/reference/telegram/types/results/bot-preview-media/)
- Accepted by: [`bots.previewInfo`](/reference/telegram/types/bots/preview-info/)
- Returned by: [`bots.addPreviewMedia`](/reference/telegram/functions/bots/add-preview-media/), [`bots.editPreviewMedia`](/reference/telegram/functions/bots/edit-preview-media/), [`bots.getPreviewMedias`](/reference/telegram/functions/bots/get-preview-medias/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
