---
title: "buttonTypeRequestPeer"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "buttonTypeRequestPeer"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x4f58a237"
---

# `buttonTypeRequestPeer`

No description provided by the pinned schema.

## Signature

```tl
buttonTypeRequestPeer#4f58a237 flags:# button_id:int peer_type:RequestPeerType max_quantity:int = ButtonType;
```

## Result type

`ButtonType`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| button_id | int | — | — | No description provided by the pinned schema. |
| peer_type | RequestPeerType | — | — | No description provided by the pinned schema. |
| max_quantity | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ButtonTypeRequestPeer
```

Public access: `miniproto.raw.types.ButtonTypeRequestPeer`.

## Class reference

```python
from miniproto.raw.types import ButtonTypeRequestPeer

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = ButtonTypeRequestPeer
```

## Result family

[`ButtonType`](/reference/telegram/types/results/button-type/)

## Relationships

- Result family: [`ButtonType`](/reference/telegram/types/results/button-type/)
- Related constructors: [`buttonTypeDefault`](/reference/telegram/types/base/button-type-default/), [`buttonTypeRequestGeoLocation`](/reference/telegram/types/base/button-type-request-geo-location/), [`buttonTypeRequestPhone`](/reference/telegram/types/base/button-type-request-phone/), [`buttonTypeRequestPoll`](/reference/telegram/types/base/button-type-request-poll/), [`buttonTypeSimpleWebView`](/reference/telegram/types/base/button-type-simple-web-view/), [`inputButtonTypeRequestPeer`](/reference/telegram/types/base/input-button-type-request-peer/)
- Accepted by: [`keyboardButton`](/reference/telegram/types/base/keyboard-button/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
