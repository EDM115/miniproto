---
title: "webViewMessageSent"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "webViewMessageSent"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x0c94511c"
---

# `webViewMessageSent`

No description provided by the pinned schema.

## Signature

```tl
webViewMessageSent#0c94511c flags:# msg_id:flags.0?InputBotInlineMessageID = WebViewMessageSent;
```

## Result type

`WebViewMessageSent`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| msg_id | flags.0?InputBotInlineMessageID | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| msg_id | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import WebViewMessageSent
```

Public access: `miniproto.raw.types.WebViewMessageSent`.

## Safe usage shape

```python
from miniproto.raw.types import WebViewMessageSent

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = WebViewMessageSent
```

## Result family

[`WebViewMessageSent`](/reference/telegram/types/results/web-view-message-sent/)

## Relationships

- Result family: [`WebViewMessageSent`](/reference/telegram/types/results/web-view-message-sent/)
- Returned by: [`messages.sendWebViewResultMessage`](/reference/telegram/functions/messages/send-web-view-result-message/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
