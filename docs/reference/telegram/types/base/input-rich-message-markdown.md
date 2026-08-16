---
title: "inputRichMessageMarkdown"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputRichMessageMarkdown"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x004b572c"
---

# `inputRichMessageMarkdown`

No description provided by the pinned schema.

## Signature

```tl
inputRichMessageMarkdown#004b572c flags:# rtl:flags.0?true noautolink:flags.1?true markdown:string files:flags.2?Vector<InputRichFile> = InputRichMessage;
```

## Result type

`InputRichMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| rtl | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| noautolink | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| markdown | string | — | — | No description provided by the pinned schema. |
| files | flags.2?Vector<InputRichFile> | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| rtl | 0 | Controlled by `flags`; present when this bit is set. |
| noautolink | 1 | Controlled by `flags`; present when this bit is set. |
| files | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputRichMessageMarkdown
```

Public access: `miniproto.raw.types.InputRichMessageMarkdown`.

## Safe usage shape

```python
from miniproto.raw.types import InputRichMessageMarkdown

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputRichMessageMarkdown
```

## Result family

[`InputRichMessage`](/reference/telegram/types/results/input-rich-message/)

## Relationships

- Result family: [`InputRichMessage`](/reference/telegram/types/results/input-rich-message/)
- Related constructors: [`inputRichMessage`](/reference/telegram/types/base/input-rich-message/), [`inputRichMessageHTML`](/reference/telegram/types/base/input-rich-message-html/)
- Accepted by: [`ephemeral.sendMessage`](/reference/telegram/functions/ephemeral/send-message/), [`messages.composeRichMessageWithAI`](/reference/telegram/functions/messages/compose-rich-message-with-ai/), [`messages.editInlineBotMessage`](/reference/telegram/functions/messages/edit-inline-bot-message/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), [`messages.saveDraft`](/reference/telegram/functions/messages/save-draft/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.translateRichMessage`](/reference/telegram/functions/messages/translate-rich-message/), [`inputBotInlineMessageRichMessage`](/reference/telegram/types/base/input-bot-inline-message-rich-message/), [`inputSendMessageRichMessageDraftAction`](/reference/telegram/types/base/input-send-message-rich-message-draft-action/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
