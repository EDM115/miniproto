---
title: "phoneCallWaiting"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "phoneCallWaiting"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xc5226f17"
---

# `phoneCallWaiting`

No description provided by the pinned schema.

## Signature

```tl
phoneCallWaiting#c5226f17 flags:# video:flags.6?true id:long access_hash:long date:int admin_id:long participant_id:long protocol:PhoneCallProtocol receive_date:flags.0?int = PhoneCall;
```

## Result type

`PhoneCall`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| video | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| admin_id | long | — | — | No description provided by the pinned schema. |
| participant_id | long | — | — | No description provided by the pinned schema. |
| protocol | PhoneCallProtocol | — | — | No description provided by the pinned schema. |
| receive_date | flags.0?int | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| video | 6 | Controlled by `flags`; present when this bit is set. |
| receive_date | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PhoneCallWaiting
```

Public access: `miniproto.raw.types.PhoneCallWaiting`.

## Safe usage shape

```python
from miniproto.raw.types import PhoneCallWaiting

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PhoneCallWaiting
```

## Result family

[`PhoneCall`](/reference/telegram/types/results/phone-call/)

## Relationships

- Result family: [`PhoneCall`](/reference/telegram/types/results/phone-call/)
- Related constructors: [`phoneCall`](/reference/telegram/types/base/phone-call/), [`phoneCallAccepted`](/reference/telegram/types/base/phone-call-accepted/), [`phoneCallDiscarded`](/reference/telegram/types/base/phone-call-discarded/), [`phoneCallEmpty`](/reference/telegram/types/base/phone-call-empty/), [`phoneCallRequested`](/reference/telegram/types/base/phone-call-requested/)
- Accepted by: [`phone.phoneCall`](/reference/telegram/types/phone/phone-call/), [`updatePhoneCall`](/reference/telegram/types/base/update-phone-call/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
