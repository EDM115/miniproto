---
title: "onrampAvailability"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "onrampAvailability"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xf9c84973"
---

# `onrampAvailability`

No description provided by the pinned schema.

## Signature

```tl
onrampAvailability#f9c84973 flags:# allowed:flags.0?true buy_allowed:flags.1?true country_code:string state:flags.2?string methods:Vector<OnrampMethodAvailability> = OnrampAvailability;
```

## Result type

`OnrampAvailability`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| allowed | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| buy_allowed | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| country_code | string | — | — | No description provided by the pinned schema. |
| state | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| methods | Vector<OnrampMethodAvailability> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| allowed | 0 | Controlled by `flags`; present when this bit is set. |
| buy_allowed | 1 | Controlled by `flags`; present when this bit is set. |
| state | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import OnrampAvailability
```

Public access: `miniproto.raw.types.OnrampAvailability`.

## Safe usage shape

```python
from miniproto.raw.types import OnrampAvailability

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = OnrampAvailability
```

## Result family

[`OnrampAvailability`](/reference/telegram/types/results/onramp-availability/)

## Relationships

- Result family: [`OnrampAvailability`](/reference/telegram/types/results/onramp-availability/)
- Returned by: [`payments.getOnrampAvailability`](/reference/telegram/functions/payments/get-onramp-availability/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
