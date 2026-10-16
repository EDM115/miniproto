---
title: "inputBusinessGreetingMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputBusinessGreetingMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x0194cb3b"
---

# `inputBusinessGreetingMessage`

No description provided by the pinned schema.

## Signature

```tl
inputBusinessGreetingMessage#0194cb3b shortcut_id:int recipients:InputBusinessRecipients no_activity_days:int = InputBusinessGreetingMessage;
```

## Result type

`InputBusinessGreetingMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| shortcut_id | int | — | — | No description provided by the pinned schema. |
| recipients | InputBusinessRecipients | — | — | No description provided by the pinned schema. |
| no_activity_days | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputBusinessGreetingMessage
```

Public access: `miniproto.raw.types.InputBusinessGreetingMessage`.

## Class reference

```python
from miniproto.raw.types import InputBusinessGreetingMessage

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = InputBusinessGreetingMessage
```

## Result family

[`InputBusinessGreetingMessage`](/reference/telegram/types/results/input-business-greeting-message/)

## Relationships

- Result family: [`InputBusinessGreetingMessage`](/reference/telegram/types/results/input-business-greeting-message/)
- Accepted by: [`account.updateBusinessGreetingMessage`](/reference/telegram/functions/account/update-business-greeting-message/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
