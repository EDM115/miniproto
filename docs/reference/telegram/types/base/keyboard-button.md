---
title: "keyboardButton"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "keyboardButton"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x2f67a72f"
---

# `keyboardButton`

No description provided by the pinned schema.

## Signature

```tl
keyboardButton#2f67a72f flags:# style:flags.10?KeyboardButtonStyle text:string type:ButtonType = KeyboardButton;
```

## Result type

`KeyboardButton`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| style | flags.10?KeyboardButtonStyle | flags.10 | — | No description provided by the pinned schema. |
| text | string | — | — | No description provided by the pinned schema. |
| type | ButtonType | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| style | 10 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import KeyboardButton
```

Public access: `miniproto.raw.types.KeyboardButton`.

## Safe usage shape

```python
from miniproto.raw.types import KeyboardButton

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = KeyboardButton
```

## Result family

[`KeyboardButton`](/reference/telegram/types/results/keyboard-button/)

## Relationships

- Result family: [`KeyboardButton`](/reference/telegram/types/results/keyboard-button/)
- Accepted by: [`bots.requestWebViewButton`](/reference/telegram/functions/bots/request-web-view-button/), [`keyboardButtonRow`](/reference/telegram/types/base/keyboard-button-row/)
- Returned by: [`bots.getRequestedWebViewButton`](/reference/telegram/functions/bots/get-requested-web-view-button/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
