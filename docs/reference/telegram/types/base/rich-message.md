---
title: "richMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "richMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xbaf39d8b"
---

# `richMessage`

No description provided by the pinned schema.

## Signature

```tl
richMessage#baf39d8b flags:# rtl:flags.0?true part:flags.1?true blocks:Vector<PageBlock> photos:Vector<Photo> documents:Vector<Document> = RichMessage;
```

## Result type

`RichMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| rtl | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| part | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| blocks | Vector<PageBlock> | — | — | No description provided by the pinned schema. |
| photos | Vector<Photo> | — | — | No description provided by the pinned schema. |
| documents | Vector<Document> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| rtl | 0 | Controlled by `flags`; present when this bit is set. |
| part | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import RichMessage
```

Public access: `miniproto.raw.types.RichMessage`.

## Safe usage shape

```python
from miniproto.raw.types import RichMessage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = RichMessage
```

## Result family

[`RichMessage`](/reference/telegram/types/results/rich-message/)

## Relationships

- Result family: [`RichMessage`](/reference/telegram/types/results/rich-message/)
- Accepted by: [`botInlineMessageRichMessage`](/reference/telegram/types/base/bot-inline-message-rich-message/), [`draftMessage`](/reference/telegram/types/base/draft-message/), [`ephemeralMessage`](/reference/telegram/types/base/ephemeral-message/), [`message`](/reference/telegram/types/base/message/), [`messages.composedRichMessageWithAI`](/reference/telegram/types/messages/composed-rich-message-with-ai/), [`messages.translatedRichMessage`](/reference/telegram/types/messages/translated-rich-message/), [`sendMessageRichMessageDraftAction`](/reference/telegram/types/base/send-message-rich-message-draft-action/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
