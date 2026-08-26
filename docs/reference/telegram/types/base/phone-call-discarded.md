---
title: "phoneCallDiscarded"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "phoneCallDiscarded"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x50ca4de1"
---

# `phoneCallDiscarded`

No description provided by the pinned schema.

## Signature

```tl
phoneCallDiscarded#50ca4de1 flags:# need_rating:flags.2?true need_debug:flags.3?true video:flags.6?true id:long reason:flags.0?PhoneCallDiscardReason duration:flags.1?int = PhoneCall;
```

## Result type

`PhoneCall`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| need_rating | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| need_debug | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| video | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| reason | flags.0?PhoneCallDiscardReason | flags.0 | — | No description provided by the pinned schema. |
| duration | flags.1?int | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| need_rating | 2 | Controlled by `flags`; present when this bit is set. |
| need_debug | 3 | Controlled by `flags`; present when this bit is set. |
| video | 6 | Controlled by `flags`; present when this bit is set. |
| reason | 0 | Controlled by `flags`; present when this bit is set. |
| duration | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PhoneCallDiscarded
```

Public access: `miniproto.raw.types.PhoneCallDiscarded`.

## Safe usage shape

```python
from miniproto.raw.types import PhoneCallDiscarded

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PhoneCallDiscarded
```

## Result family

[`PhoneCall`](/reference/telegram/types/results/phone-call/)

## Relationships

- Result family: [`PhoneCall`](/reference/telegram/types/results/phone-call/)
- Related constructors: [`phoneCall`](/reference/telegram/types/base/phone-call/), [`phoneCallAccepted`](/reference/telegram/types/base/phone-call-accepted/), [`phoneCallEmpty`](/reference/telegram/types/base/phone-call-empty/), [`phoneCallRequested`](/reference/telegram/types/base/phone-call-requested/), [`phoneCallWaiting`](/reference/telegram/types/base/phone-call-waiting/)
- Accepted by: [`phone.phoneCall`](/reference/telegram/types/phone/phone-call/), [`updatePhoneCall`](/reference/telegram/types/base/update-phone-call/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
