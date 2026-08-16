---
title: "messageExtendedMedia"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messageExtendedMedia"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xee479c64"
---

# `messageExtendedMedia`

No description provided by the pinned schema.

## Signature

```tl
messageExtendedMedia#ee479c64 media:MessageMedia = MessageExtendedMedia;
```

## Result type

`MessageExtendedMedia`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| media | MessageMedia | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessageExtendedMedia
```

Public access: `miniproto.raw.types.MessageExtendedMedia`.

## Safe usage shape

```python
from miniproto.raw.types import MessageExtendedMedia

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessageExtendedMedia
```

## Result family

[`MessageExtendedMedia`](/reference/telegram/types/results/message-extended-media/)

## Relationships

- Result family: [`MessageExtendedMedia`](/reference/telegram/types/results/message-extended-media/)
- Related constructors: [`messageExtendedMediaPreview`](/reference/telegram/types/base/message-extended-media-preview/)
- Accepted by: [`messageMediaInvoice`](/reference/telegram/types/base/message-media-invoice/), [`messageMediaPaidMedia`](/reference/telegram/types/base/message-media-paid-media/), [`updateMessageExtendedMedia`](/reference/telegram/types/base/update-message-extended-media/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
