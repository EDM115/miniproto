---
title: "inputPhoneCall"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputPhoneCall"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x1e36fded"
---

# `inputPhoneCall`

No description provided by the pinned schema.

## Signature

```tl
inputPhoneCall#1e36fded id:long access_hash:long = InputPhoneCall;
```

## Result type

`InputPhoneCall`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputPhoneCall
```

Public access: `miniproto.raw.types.InputPhoneCall`.

## Safe usage shape

```python
from miniproto.raw.types import InputPhoneCall

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputPhoneCall
```

## Result family

[`InputPhoneCall`](/reference/telegram/types/results/input-phone-call/)

## Relationships

- Result family: [`InputPhoneCall`](/reference/telegram/types/results/input-phone-call/)
- Accepted by: [`phone.acceptCall`](/reference/telegram/functions/phone/accept-call/), [`phone.confirmCall`](/reference/telegram/functions/phone/confirm-call/), [`phone.discardCall`](/reference/telegram/functions/phone/discard-call/), [`phone.receivedCall`](/reference/telegram/functions/phone/received-call/), [`phone.saveCallDebug`](/reference/telegram/functions/phone/save-call-debug/), [`phone.saveCallLog`](/reference/telegram/functions/phone/save-call-log/), [`phone.sendSignalingData`](/reference/telegram/functions/phone/send-signaling-data/), [`phone.setCallRating`](/reference/telegram/functions/phone/set-call-rating/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
