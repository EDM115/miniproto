---
title: "messages.composeRichMessageWithAI"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "messages.composeRichMessageWithAI"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x8d7ae6af"
---

# `messages.composeRichMessageWithAI`

No description provided by the pinned schema.

## Signature

```tl
messages.composeRichMessageWithAI#8d7ae6af flags:# proofread:flags.0?true emojify:flags.3?true text:flags.4?InputRichMessage translate_to_lang:flags.1?string tone:flags.2?InputAiComposeTone = messages.ComposedRichMessageWithAI;
```

## Result type

`messages.ComposedRichMessageWithAI`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| proofread | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| emojify | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| text | flags.4?InputRichMessage | flags.4 | — | No description provided by the pinned schema. |
| translate_to_lang | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| tone | flags.2?InputAiComposeTone | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| proofread | 0 | Controlled by `flags`; present when this bit is set. |
| emojify | 3 | Controlled by `flags`; present when this bit is set. |
| text | 4 | Controlled by `flags`; present when this bit is set. |
| translate_to_lang | 1 | Controlled by `flags`; present when this bit is set. |
| tone | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import MessagesComposeRichMessageWithAI
```

Public access: `miniproto.raw.functions.MessagesComposeRichMessageWithAI`.

## Safe usage shape

```python
from miniproto.raw.functions import MessagesComposeRichMessageWithAI

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = MessagesComposeRichMessageWithAI
```

## Result family

[`messages.ComposedRichMessageWithAI`](/reference/telegram/types/results/messages-composed-rich-message-with-ai/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

[`InputAiComposeTone`](/reference/telegram/types/results/input-ai-compose-tone/), [`InputRichMessage`](/reference/telegram/types/results/input-rich-message/)
Known selected constructors: [`inputAiComposeToneDefault`](/reference/telegram/types/base/input-ai-compose-tone-default/), [`inputAiComposeToneID`](/reference/telegram/types/base/input-ai-compose-tone-id/), [`inputAiComposeToneSingleUse`](/reference/telegram/types/base/input-ai-compose-tone-single-use/), [`inputAiComposeToneSlug`](/reference/telegram/types/base/input-ai-compose-tone-slug/), [`inputRichMessage`](/reference/telegram/types/base/input-rich-message/), [`inputRichMessageHTML`](/reference/telegram/types/base/input-rich-message-html/), [`inputRichMessageMarkdown`](/reference/telegram/types/base/input-rich-message-markdown/)

## Returned types

[`messages.ComposedRichMessageWithAI`](/reference/telegram/types/results/messages-composed-rich-message-with-ai/)
Known selected constructors: [`messages.composedRichMessageWithAI`](/reference/telegram/types/messages/composed-rich-message-with-ai/)

## Related methods

[`aicompose.deleteTone`](/reference/telegram/functions/aicompose/delete-tone/), [`aicompose.getTone`](/reference/telegram/functions/aicompose/get-tone/), [`aicompose.getToneExample`](/reference/telegram/functions/aicompose/get-tone-example/), [`aicompose.saveTone`](/reference/telegram/functions/aicompose/save-tone/), [`aicompose.updateTone`](/reference/telegram/functions/aicompose/update-tone/), [`ephemeral.editMessage`](/reference/telegram/functions/ephemeral/edit-message/), [`ephemeral.sendMessage`](/reference/telegram/functions/ephemeral/send-message/), [`messages.composeMessageWithAI`](/reference/telegram/functions/messages/compose-message-with-ai/), [`messages.editInlineBotMessage`](/reference/telegram/functions/messages/edit-inline-bot-message/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), [`messages.saveDraft`](/reference/telegram/functions/messages/save-draft/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.translateRichMessage`](/reference/telegram/functions/messages/translate-rich-message/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
