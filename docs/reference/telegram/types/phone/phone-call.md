---
title: "phone.phoneCall"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "phone.phoneCall"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "phone"
schema_source: "tdlib"
constructor_id: "0xec82e140"
---

# `phone.phoneCall`

No description provided by the pinned schema.

## Signature

```tl
phone.phoneCall#ec82e140 phone_call:PhoneCall users:Vector<User> = phone.PhoneCall;
```

## Result type

`phone.PhoneCall`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| phone_call | PhoneCall | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PhonePhoneCall
```

Public access: `miniproto.raw.types.PhonePhoneCall`.

## Safe usage shape

```python
from miniproto.raw.types import PhonePhoneCall

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PhonePhoneCall
```

## Result family

[`phone.PhoneCall`](/reference/telegram/types/results/phone-phone-call/)

## Relationships

- Result family: [`phone.PhoneCall`](/reference/telegram/types/results/phone-phone-call/)
- Returned by: [`phone.acceptCall`](/reference/telegram/functions/phone/accept-call/), [`phone.confirmCall`](/reference/telegram/functions/phone/confirm-call/), [`phone.requestCall`](/reference/telegram/functions/phone/request-call/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
