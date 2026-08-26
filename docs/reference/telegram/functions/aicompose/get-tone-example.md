---
title: "aicompose.getToneExample"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "aicompose.getToneExample"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "aicompose"
schema_source: "tdlib"
constructor_id: "0xd1b4ab14"
---

# `aicompose.getToneExample`

No description provided by the pinned schema.

## Signature

```tl
aicompose.getToneExample#d1b4ab14 tone:InputAiComposeTone num:int = AiComposeToneExample;
```

## Result type

`AiComposeToneExample`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| tone | InputAiComposeTone | — | — | No description provided by the pinned schema. |
| num | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AicomposeGetToneExample
```

Public access: `miniproto.raw.functions.AicomposeGetToneExample`.

## Safe usage shape

```python
from miniproto.raw.functions import AicomposeGetToneExample

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AicomposeGetToneExample
```

## Result family

[`AiComposeToneExample`](/reference/telegram/types/results/ai-compose-tone-example/)

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

[`AiComposeToneExample`](/reference/telegram/types/results/ai-compose-tone-example/)
Known selected constructors: [`aiComposeToneExample`](/reference/telegram/types/base/ai-compose-tone-example/)

## Related methods

[`aicompose.deleteTone`](/reference/telegram/functions/aicompose/delete-tone/), [`aicompose.getTone`](/reference/telegram/functions/aicompose/get-tone/), [`aicompose.saveTone`](/reference/telegram/functions/aicompose/save-tone/), [`aicompose.updateTone`](/reference/telegram/functions/aicompose/update-tone/), [`messages.composeMessageWithAI`](/reference/telegram/functions/messages/compose-message-with-ai/), [`messages.composeRichMessageWithAI`](/reference/telegram/functions/messages/compose-rich-message-with-ai/)

## Availability evidence

- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
