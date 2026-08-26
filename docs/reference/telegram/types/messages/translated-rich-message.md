---
title: "messages.translatedRichMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.translatedRichMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x4203998f"
---

# `messages.translatedRichMessage`

No description provided by the pinned schema.

## Signature

```tl
messages.translatedRichMessage#4203998f result:Vector<RichMessage> = messages.TranslatedRichMessage;
```

## Result type

`messages.TranslatedRichMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| result | Vector<RichMessage> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesTranslatedRichMessage
```

Public access: `miniproto.raw.types.MessagesTranslatedRichMessage`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesTranslatedRichMessage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesTranslatedRichMessage
```

## Result family

[`messages.TranslatedRichMessage`](/reference/telegram/types/results/messages-translated-rich-message/)

## Relationships

- Result family: [`messages.TranslatedRichMessage`](/reference/telegram/types/results/messages-translated-rich-message/)
- Returned by: [`messages.translateRichMessage`](/reference/telegram/functions/messages/translate-rich-message/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
