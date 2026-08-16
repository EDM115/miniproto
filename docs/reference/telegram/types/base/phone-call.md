---
title: "phoneCall"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "phoneCall"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x30535af5"
---

# `phoneCall`

No description provided by the pinned schema.

## Signature

```tl
phoneCall#30535af5 flags:# p2p_allowed:flags.5?true video:flags.6?true conference_supported:flags.8?true id:long access_hash:long date:int admin_id:long participant_id:long g_a_or_b:bytes key_fingerprint:long protocol:PhoneCallProtocol connections:Vector<PhoneConnection> start_date:int custom_parameters:flags.7?DataJSON = PhoneCall;
```

## Result type

`PhoneCall`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| p2p_allowed | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| video | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| conference_supported | flags.8?true | flags.8 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| admin_id | long | — | — | No description provided by the pinned schema. |
| participant_id | long | — | — | No description provided by the pinned schema. |
| g_a_or_b | bytes | — | — | No description provided by the pinned schema. |
| key_fingerprint | long | — | — | No description provided by the pinned schema. |
| protocol | PhoneCallProtocol | — | — | No description provided by the pinned schema. |
| connections | Vector<PhoneConnection> | — | — | No description provided by the pinned schema. |
| start_date | int | — | — | No description provided by the pinned schema. |
| custom_parameters | flags.7?DataJSON | flags.7 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| p2p_allowed | 5 | Controlled by `flags`; present when this bit is set. |
| video | 6 | Controlled by `flags`; present when this bit is set. |
| conference_supported | 8 | Controlled by `flags`; present when this bit is set. |
| custom_parameters | 7 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PhoneCall
```

Public access: `miniproto.raw.types.PhoneCall`.

## Safe usage shape

```python
from miniproto.raw.types import PhoneCall

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PhoneCall
```

## Result family

[`PhoneCall`](/reference/telegram/types/results/phone-call/)

## Relationships

- Result family: [`PhoneCall`](/reference/telegram/types/results/phone-call/)
- Related constructors: [`phoneCallAccepted`](/reference/telegram/types/base/phone-call-accepted/), [`phoneCallDiscarded`](/reference/telegram/types/base/phone-call-discarded/), [`phoneCallEmpty`](/reference/telegram/types/base/phone-call-empty/), [`phoneCallRequested`](/reference/telegram/types/base/phone-call-requested/), [`phoneCallWaiting`](/reference/telegram/types/base/phone-call-waiting/)
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
