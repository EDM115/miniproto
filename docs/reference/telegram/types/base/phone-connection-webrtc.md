---
title: "phoneConnectionWebrtc"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "phoneConnectionWebrtc"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x635fe375"
---

# `phoneConnectionWebrtc`

No description provided by the pinned schema.

## Signature

```tl
phoneConnectionWebrtc#635fe375 flags:# turn:flags.0?true stun:flags.1?true id:long ip:string ipv6:string port:int username:string password:string = PhoneConnection;
```

## Result type

`PhoneConnection`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| turn | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| stun | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| ip | string | — | — | No description provided by the pinned schema. |
| ipv6 | string | — | — | No description provided by the pinned schema. |
| port | int | — | — | No description provided by the pinned schema. |
| username | string | — | — | No description provided by the pinned schema. |
| password | string | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| turn | 0 | Controlled by `flags`; present when this bit is set. |
| stun | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import PhoneConnectionWebrtc
```

Public access: `miniproto.raw.types.PhoneConnectionWebrtc`.

## Safe usage shape

```python
from miniproto.raw.types import PhoneConnectionWebrtc

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PhoneConnectionWebrtc
```

## Result family

[`PhoneConnection`](/reference/telegram/types/results/phone-connection/)

## Relationships

- Result family: [`PhoneConnection`](/reference/telegram/types/results/phone-connection/)
- Related constructors: [`phoneConnection`](/reference/telegram/types/base/phone-connection/)
- Accepted by: [`phoneCall`](/reference/telegram/types/base/phone-call/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
