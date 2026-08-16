---
title: "messages.composeMessageWithAI"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "messages.composeMessageWithAI"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0xdaecc589"
---

# `messages.composeMessageWithAI`

No description provided by the pinned schema.

## Signature

```tl
messages.composeMessageWithAI#daecc589 flags:# proofread:flags.0?true emojify:flags.3?true text:TextWithEntities translate_to_lang:flags.1?string tone:flags.2?InputAiComposeTone = messages.ComposedMessageWithAI;
```

## Result type

`messages.ComposedMessageWithAI`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| proofread | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| emojify | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| text | TextWithEntities | — | — | No description provided by the pinned schema. |
| translate_to_lang | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| tone | flags.2?InputAiComposeTone | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| proofread | 0 | Controlled by `flags`; present when this bit is set. |
| emojify | 3 | Controlled by `flags`; present when this bit is set. |
| translate_to_lang | 1 | Controlled by `flags`; present when this bit is set. |
| tone | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import MessagesComposeMessageWithAI
```

Public access: `miniproto.raw.functions.MessagesComposeMessageWithAI`.

## Safe usage shape

```python
from miniproto.raw.functions import MessagesComposeMessageWithAI

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = MessagesComposeMessageWithAI
```

## Result family

[`messages.ComposedMessageWithAI`](/reference/telegram/types/results/messages-composed-message-with-ai/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`AICOMPOSE_FLOOD_PREMIUM`](/reference/telegram/errors/aicompose-flood-premium/) | You've reached the daily limit of AI text transformations, upgrade to [Telegram Premium](https://core.telegram.org/api/premium) to get **50x** times more AI text transformations per day! |
| 400 | [`AI_COMPOSE_TASK_MISSING`](/reference/telegram/errors/ai-compose-task-missing/) | No AI task was specified. The caller must provide at least one of: proofread, translate (with a target language), tone, or emojify. |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`MESSAGE_EMPTY`](/reference/telegram/errors/message-empty/) | The provided message is empty. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 500 | [`AICOMPOSE_TIMEOUT`](/reference/telegram/errors/aicompose-timeout/) | A timeout occurred while composing the message. |

## Accepted types

[`InputAiComposeTone`](/reference/telegram/types/results/input-ai-compose-tone/), [`TextWithEntities`](/reference/telegram/types/results/text-with-entities/)
Known selected constructors: [`inputAiComposeToneDefault`](/reference/telegram/types/base/input-ai-compose-tone-default/), [`inputAiComposeToneID`](/reference/telegram/types/base/input-ai-compose-tone-id/), [`inputAiComposeToneSingleUse`](/reference/telegram/types/base/input-ai-compose-tone-single-use/), [`inputAiComposeToneSlug`](/reference/telegram/types/base/input-ai-compose-tone-slug/), [`textWithEntities`](/reference/telegram/types/base/text-with-entities/)

## Returned types

[`messages.ComposedMessageWithAI`](/reference/telegram/types/results/messages-composed-message-with-ai/)
Known selected constructors: [`messages.composedMessageWithAI`](/reference/telegram/types/messages/composed-message-with-ai/)

## Related methods

[`aicompose.deleteTone`](/reference/telegram/functions/aicompose/delete-tone/), [`aicompose.getTone`](/reference/telegram/functions/aicompose/get-tone/), [`aicompose.getToneExample`](/reference/telegram/functions/aicompose/get-tone-example/), [`aicompose.saveTone`](/reference/telegram/functions/aicompose/save-tone/), [`aicompose.updateTone`](/reference/telegram/functions/aicompose/update-tone/), [`contacts.addContact`](/reference/telegram/functions/contacts/add-contact/), [`contacts.updateContactNote`](/reference/telegram/functions/contacts/update-contact-note/), [`messages.composeRichMessageWithAI`](/reference/telegram/functions/messages/compose-rich-message-with-ai/), [`messages.editFactCheck`](/reference/telegram/functions/messages/edit-fact-check/), [`messages.summarizeText`](/reference/telegram/functions/messages/summarize-text/), [`messages.translateText`](/reference/telegram/functions/messages/translate-text/), [`phone.sendGroupCallMessage`](/reference/telegram/functions/phone/send-group-call-message/)

## Availability evidence

- user only

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
