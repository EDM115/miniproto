---
title: "keyboardButtonRequestPhone"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "keyboardButtonRequestPhone"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x417efd8f"
---

# `keyboardButtonRequestPhone`

No description provided by the pinned schema.

## Signature

```tl
keyboardButtonRequestPhone#417efd8f flags:# style:flags.10?KeyboardButtonStyle text:string = KeyboardButton;
```

## Result type

`KeyboardButton`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| style | flags.10?KeyboardButtonStyle | flags.10 | — | No description provided by the pinned schema. |
| text | string | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| style | 10 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import KeyboardButtonRequestPhone
```

Public access: `miniproto.raw.types.KeyboardButtonRequestPhone`.

## Safe usage shape

```python
from miniproto.raw.types import KeyboardButtonRequestPhone

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = KeyboardButtonRequestPhone
```

## Result family

[`KeyboardButton`](/reference/telegram/types/results/keyboard-button/)

## Relationships

- Result family: [`KeyboardButton`](/reference/telegram/types/results/keyboard-button/)
- Related constructors: [`inputKeyboardButtonRequestPeer`](/reference/telegram/types/base/input-keyboard-button-request-peer/), [`inputKeyboardButtonUrlAuth`](/reference/telegram/types/base/input-keyboard-button-url-auth/), [`inputKeyboardButtonUserProfile`](/reference/telegram/types/base/input-keyboard-button-user-profile/), [`keyboardButton`](/reference/telegram/types/base/keyboard-button/), [`keyboardButtonBuy`](/reference/telegram/types/base/keyboard-button-buy/), [`keyboardButtonCallback`](/reference/telegram/types/base/keyboard-button-callback/), [`keyboardButtonCopy`](/reference/telegram/types/base/keyboard-button-copy/), [`keyboardButtonGame`](/reference/telegram/types/base/keyboard-button-game/), [`keyboardButtonRequestGeoLocation`](/reference/telegram/types/base/keyboard-button-request-geo-location/), [`keyboardButtonRequestPeer`](/reference/telegram/types/base/keyboard-button-request-peer/), [`keyboardButtonRequestPoll`](/reference/telegram/types/base/keyboard-button-request-poll/), [`keyboardButtonSimpleWebView`](/reference/telegram/types/base/keyboard-button-simple-web-view/), [`keyboardButtonSwitchInline`](/reference/telegram/types/base/keyboard-button-switch-inline/), [`keyboardButtonUrl`](/reference/telegram/types/base/keyboard-button-url/), [`keyboardButtonUrlAuth`](/reference/telegram/types/base/keyboard-button-url-auth/), [`keyboardButtonUserProfile`](/reference/telegram/types/base/keyboard-button-user-profile/), [`keyboardButtonWebView`](/reference/telegram/types/base/keyboard-button-web-view/)
- Accepted by: [`bots.requestWebViewButton`](/reference/telegram/functions/bots/request-web-view-button/), [`keyboardButtonRow`](/reference/telegram/types/base/keyboard-button-row/)
- Returned by: [`bots.getRequestedWebViewButton`](/reference/telegram/functions/bots/get-requested-web-view-button/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
