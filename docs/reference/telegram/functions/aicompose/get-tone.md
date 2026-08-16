---
title: "aicompose.getTone"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "aicompose.getTone"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "aicompose"
layer: 228
schema_source: "tdlib"
constructor_id: "0xb2e8ba03"
---

# `aicompose.getTone`

No description provided by the pinned schema.

## Signature

```tl
aicompose.getTone#b2e8ba03 tone:InputAiComposeTone = aicompose.Tones;
```

## Result type

`aicompose.Tones`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| tone | InputAiComposeTone | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AicomposeGetTone
```

Public access: `miniproto.raw.functions.AicomposeGetTone`.

## Safe usage shape

```python
from miniproto.raw.functions import AicomposeGetTone

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AicomposeGetTone
```

## Result family

[`aicompose.Tones`](/reference/telegram/types/results/aicompose-tones/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`AICOMPOSE_TONE_INVALID`](/reference/telegram/errors/aicompose-tone-invalid/) | The specified tone is invalid. |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputAiComposeTone`](/reference/telegram/types/results/input-ai-compose-tone/)
Known selected constructors: [`inputAiComposeToneDefault`](/reference/telegram/types/base/input-ai-compose-tone-default/), [`inputAiComposeToneID`](/reference/telegram/types/base/input-ai-compose-tone-id/), [`inputAiComposeToneSingleUse`](/reference/telegram/types/base/input-ai-compose-tone-single-use/), [`inputAiComposeToneSlug`](/reference/telegram/types/base/input-ai-compose-tone-slug/)

## Returned types

[`aicompose.Tones`](/reference/telegram/types/results/aicompose-tones/)
Known selected constructors: [`aicompose.tones`](/reference/telegram/types/aicompose/tones/), [`aicompose.tonesNotModified`](/reference/telegram/types/aicompose/tones-not-modified/)

## Related methods

[`aicompose.deleteTone`](/reference/telegram/functions/aicompose/delete-tone/), [`aicompose.getToneExample`](/reference/telegram/functions/aicompose/get-tone-example/), [`aicompose.getTones`](/reference/telegram/functions/aicompose/get-tones/), [`aicompose.saveTone`](/reference/telegram/functions/aicompose/save-tone/), [`aicompose.updateTone`](/reference/telegram/functions/aicompose/update-tone/), [`messages.composeMessageWithAI`](/reference/telegram/functions/messages/compose-message-with-ai/), [`messages.composeRichMessageWithAI`](/reference/telegram/functions/messages/compose-rich-message-with-ai/)

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
