---
title: "phone.acceptCall"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "phone.acceptCall"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "phone"
layer: 228
schema_source: "tdlib"
constructor_id: "0x3bd2b4a0"
---

# `phone.acceptCall`

No description provided by the pinned schema.

## Signature

```tl
phone.acceptCall#3bd2b4a0 peer:InputPhoneCall g_b:bytes protocol:PhoneCallProtocol = phone.PhoneCall;
```

## Result type

`phone.PhoneCall`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| peer | InputPhoneCall | — | — | No description provided by the pinned schema. |
| g_b | bytes | — | — | No description provided by the pinned schema. |
| protocol | PhoneCallProtocol | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import PhoneAcceptCall
```

Public access: `miniproto.raw.functions.PhoneAcceptCall`.

## Safe usage shape

```python
from miniproto.raw.functions import PhoneAcceptCall

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = PhoneAcceptCall
```

## Result family

[`phone.PhoneCall`](/reference/telegram/types/results/phone-phone-call/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CALL_ALREADY_ACCEPTED`](/reference/telegram/errors/call-already-accepted/) | The call was already accepted. |
| 400 | [`CALL_ALREADY_DECLINED`](/reference/telegram/errors/call-already-declined/) | The call was already declined. |
| 400 | [`CALL_PEER_INVALID`](/reference/telegram/errors/call-peer-invalid/) | The provided call peer object is invalid. |
| 400 | [`CALL_PROTOCOL_FLAGS_INVALID`](/reference/telegram/errors/call-protocol-flags-invalid/) | Call protocol flags invalid. |
| 400 | [`CALL_PROTOCOL_LAYER_INVALID`](/reference/telegram/errors/call-protocol-layer-invalid/) | The specified protocol layer version range is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |
| 406 | [`CALL_PROTOCOL_COMPAT_LAYER_INVALID`](/reference/telegram/errors/call-protocol-compat-layer-invalid/) | The other side of the call does not support any of the VoIP protocols supported by the local client, as specified by the `protocol.layer` and `protocol.library_versions` fields. |
| 500 | [`CALL_OCCUPY_FAILED`](/reference/telegram/errors/call-occupy-failed-500/) | The call failed because the user is already making another call. |

## Accepted types

[`InputPhoneCall`](/reference/telegram/types/results/input-phone-call/), [`PhoneCallProtocol`](/reference/telegram/types/results/phone-call-protocol/)
Known selected constructors: [`inputPhoneCall`](/reference/telegram/types/base/input-phone-call/), [`phoneCallProtocol`](/reference/telegram/types/base/phone-call-protocol/)

## Returned types

[`phone.PhoneCall`](/reference/telegram/types/results/phone-phone-call/)
Known selected constructors: [`phone.phoneCall`](/reference/telegram/types/phone/phone-call/)

## Related methods

[`phone.confirmCall`](/reference/telegram/functions/phone/confirm-call/), [`phone.discardCall`](/reference/telegram/functions/phone/discard-call/), [`phone.receivedCall`](/reference/telegram/functions/phone/received-call/), [`phone.requestCall`](/reference/telegram/functions/phone/request-call/), [`phone.saveCallDebug`](/reference/telegram/functions/phone/save-call-debug/), [`phone.saveCallLog`](/reference/telegram/functions/phone/save-call-log/), [`phone.sendSignalingData`](/reference/telegram/functions/phone/send-signaling-data/), [`phone.setCallRating`](/reference/telegram/functions/phone/set-call-rating/)

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
