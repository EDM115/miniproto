---
title: "inputBotAppShortName"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputBotAppShortName"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x908c0407"
---

# `inputBotAppShortName`

No description provided by the pinned schema.

## Signature

```tl
inputBotAppShortName#908c0407 bot_id:InputUser short_name:string = InputBotApp;
```

## Result type

`InputBotApp`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| bot_id | InputUser | — | — | No description provided by the pinned schema. |
| short_name | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputBotAppShortName
```

Public access: `miniproto.raw.types.InputBotAppShortName`.

## Safe usage shape

```python
from miniproto.raw.types import InputBotAppShortName

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputBotAppShortName
```

## Result family

[`InputBotApp`](/reference/telegram/types/results/input-bot-app/)

## Relationships

- Result family: [`InputBotApp`](/reference/telegram/types/results/input-bot-app/)
- Related constructors: [`inputBotAppID`](/reference/telegram/types/base/input-bot-app-id/)
- Accepted by: [`messages.getBotApp`](/reference/telegram/functions/messages/get-bot-app/), [`messages.requestAppWebView`](/reference/telegram/functions/messages/request-app-web-view/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
