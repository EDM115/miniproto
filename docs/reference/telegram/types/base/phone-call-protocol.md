---
title: "phoneCallProtocol"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "phoneCallProtocol"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xfc878fc8"
---

# `phoneCallProtocol`

No description provided by the pinned schema.

## Signature

```tl
phoneCallProtocol#fc878fc8 flags:# udp_p2p:flags.0?true udp_reflector:flags.1?true min_layer:int max_layer:int library_versions:Vector<string> = PhoneCallProtocol;
```

## Result type

`PhoneCallProtocol`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| udp_p2p | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| udp_reflector | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| min_layer | int | — | — | No description provided by the pinned schema. |
| max_layer | int | — | — | No description provided by the pinned schema. |
| library_versions | Vector<string> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| udp_p2p | 0 | Controlled by `flags`; present when this bit is set. |
| udp_reflector | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PhoneCallProtocol
```

Public access: `miniproto.raw.types.PhoneCallProtocol`.

## Safe usage shape

```python
from miniproto.raw.types import PhoneCallProtocol

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PhoneCallProtocol
```

## Result family

[`PhoneCallProtocol`](/reference/telegram/types/results/phone-call-protocol/)

## Relationships

- Result family: [`PhoneCallProtocol`](/reference/telegram/types/results/phone-call-protocol/)
- Accepted by: [`phone.acceptCall`](/reference/telegram/functions/phone/accept-call/), [`phone.confirmCall`](/reference/telegram/functions/phone/confirm-call/), [`phone.requestCall`](/reference/telegram/functions/phone/request-call/), [`phoneCall`](/reference/telegram/types/base/phone-call/), [`phoneCallAccepted`](/reference/telegram/types/base/phone-call-accepted/), [`phoneCallRequested`](/reference/telegram/types/base/phone-call-requested/), [`phoneCallWaiting`](/reference/telegram/types/base/phone-call-waiting/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
