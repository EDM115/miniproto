---
title: "onrampProviderInfo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "onrampProviderInfo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x0dc27582"
---

# `onrampProviderInfo`

No description provided by the pinned schema.

## Signature

```tl
onrampProviderInfo#0dc27582 flags:# supports_base_currencies:flags.0?true supports_limits:flags.1?true supports_quote:flags.2?true id:string name:string crypto_currencies:Vector<string> = OnrampProviderInfo;
```

## Result type

`OnrampProviderInfo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| supports_base_currencies | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| supports_limits | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| supports_quote | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| id | string | — | — | No description provided by the pinned schema. |
| name | string | — | — | No description provided by the pinned schema. |
| crypto_currencies | Vector<string> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| supports_base_currencies | 0 | Controlled by `flags`; present when this bit is set. |
| supports_limits | 1 | Controlled by `flags`; present when this bit is set. |
| supports_quote | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import OnrampProviderInfo
```

Public access: `miniproto.raw.types.OnrampProviderInfo`.

## Class reference

```python
from miniproto.raw.types import OnrampProviderInfo

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = OnrampProviderInfo
```

## Result family

[`OnrampProviderInfo`](/reference/telegram/types/results/onramp-provider-info/)

## Relationships

- Result family: [`OnrampProviderInfo`](/reference/telegram/types/results/onramp-provider-info/)
- Returned by: [`payments.getOnrampProviders`](/reference/telegram/functions/payments/get-onramp-providers/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
