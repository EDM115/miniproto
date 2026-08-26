---
title: "phone.confirmCall"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "phone.confirmCall"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "phone"
schema_source: "tdlib"
constructor_id: "0x2efe1722"
---

# `phone.confirmCall`

No description provided by the pinned schema.

## Signature

```tl
phone.confirmCall#2efe1722 peer:InputPhoneCall g_a:bytes key_fingerprint:long protocol:PhoneCallProtocol = phone.PhoneCall;
```

## Result type

`phone.PhoneCall`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| peer | InputPhoneCall | — | — | No description provided by the pinned schema. |
| g_a | bytes | — | — | No description provided by the pinned schema. |
| key_fingerprint | long | — | — | No description provided by the pinned schema. |
| protocol | PhoneCallProtocol | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import PhoneConfirmCall
```

Public access: `miniproto.raw.functions.PhoneConfirmCall`.

## Safe usage shape

```python
from miniproto.raw.functions import PhoneConfirmCall

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = PhoneConfirmCall
```

## Result family

[`phone.PhoneCall`](/reference/telegram/types/results/phone-phone-call/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CALL_ALREADY_DECLINED`](/reference/telegram/errors/call-already-declined/) | The call was already declined. |
| 400 | [`CALL_PEER_INVALID`](/reference/telegram/errors/call-peer-invalid/) | The provided call peer object is invalid. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputPhoneCall`](/reference/telegram/types/results/input-phone-call/), [`PhoneCallProtocol`](/reference/telegram/types/results/phone-call-protocol/)
Known selected constructors: [`inputPhoneCall`](/reference/telegram/types/base/input-phone-call/), [`phoneCallProtocol`](/reference/telegram/types/base/phone-call-protocol/)

## Returned types

[`phone.PhoneCall`](/reference/telegram/types/results/phone-phone-call/)
Known selected constructors: [`phone.phoneCall`](/reference/telegram/types/phone/phone-call/)

## Related methods

[`phone.acceptCall`](/reference/telegram/functions/phone/accept-call/), [`phone.discardCall`](/reference/telegram/functions/phone/discard-call/), [`phone.receivedCall`](/reference/telegram/functions/phone/received-call/), [`phone.requestCall`](/reference/telegram/functions/phone/request-call/), [`phone.saveCallDebug`](/reference/telegram/functions/phone/save-call-debug/), [`phone.saveCallLog`](/reference/telegram/functions/phone/save-call-log/), [`phone.sendSignalingData`](/reference/telegram/functions/phone/send-signaling-data/), [`phone.setCallRating`](/reference/telegram/functions/phone/set-call-rating/)

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
