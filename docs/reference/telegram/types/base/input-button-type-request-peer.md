---
title: "inputButtonTypeRequestPeer"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputButtonTypeRequestPeer"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x3fe268fe"
---

# `inputButtonTypeRequestPeer`

No description provided by the pinned schema.

## Signature

```tl
inputButtonTypeRequestPeer#3fe268fe flags:# name_requested:flags.0?true username_requested:flags.1?true photo_requested:flags.2?true button_id:int peer_type:RequestPeerType max_quantity:int = ButtonType;
```

## Result type

`ButtonType`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| name_requested | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| username_requested | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| photo_requested | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| button_id | int | — | — | No description provided by the pinned schema. |
| peer_type | RequestPeerType | — | — | No description provided by the pinned schema. |
| max_quantity | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| name_requested | 0 | Controlled by `flags`; present when this bit is set. |
| username_requested | 1 | Controlled by `flags`; present when this bit is set. |
| photo_requested | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputButtonTypeRequestPeer
```

Public access: `miniproto.raw.types.InputButtonTypeRequestPeer`.

## Safe usage shape

```python
from miniproto.raw.types import InputButtonTypeRequestPeer

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputButtonTypeRequestPeer
```

## Result family

[`ButtonType`](/reference/telegram/types/results/button-type/)

## Relationships

- Result family: [`ButtonType`](/reference/telegram/types/results/button-type/)
- Related constructors: [`buttonTypeDefault`](/reference/telegram/types/base/button-type-default/), [`buttonTypeRequestGeoLocation`](/reference/telegram/types/base/button-type-request-geo-location/), [`buttonTypeRequestPeer`](/reference/telegram/types/base/button-type-request-peer/), [`buttonTypeRequestPhone`](/reference/telegram/types/base/button-type-request-phone/), [`buttonTypeRequestPoll`](/reference/telegram/types/base/button-type-request-poll/), [`buttonTypeSimpleWebView`](/reference/telegram/types/base/button-type-simple-web-view/)
- Accepted by: [`keyboardButton`](/reference/telegram/types/base/keyboard-button/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
