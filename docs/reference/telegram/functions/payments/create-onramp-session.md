---
title: "payments.createOnrampSession"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "payments.createOnrampSession"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0xa2197cf6"
---

# `payments.createOnrampSession`

No description provided by the pinned schema.

## Signature

```tl
payments.createOnrampSession#a2197cf6 flags:# provider:string crypto_currency:string address:string payment_method:flags.0?string base_currency:flags.1?string base_amount:flags.2?string memo:flags.3?string theme:flags.4?string success_return_url:flags.5?string fail_return_url:flags.6?string crypto_amount:flags.7?string = OnrampSession;
```

## Result type

`OnrampSession`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| provider | string | — | — | No description provided by the pinned schema. |
| crypto_currency | string | — | — | No description provided by the pinned schema. |
| address | string | — | — | No description provided by the pinned schema. |
| payment_method | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| base_currency | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| base_amount | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| memo | flags.3?string | flags.3 | — | No description provided by the pinned schema. |
| theme | flags.4?string | flags.4 | — | No description provided by the pinned schema. |
| success_return_url | flags.5?string | flags.5 | — | No description provided by the pinned schema. |
| fail_return_url | flags.6?string | flags.6 | — | No description provided by the pinned schema. |
| crypto_amount | flags.7?string | flags.7 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| payment_method | 0 | Controlled by `flags`; present when this bit is set. |
| base_currency | 1 | Controlled by `flags`; present when this bit is set. |
| base_amount | 2 | Controlled by `flags`; present when this bit is set. |
| memo | 3 | Controlled by `flags`; present when this bit is set. |
| theme | 4 | Controlled by `flags`; present when this bit is set. |
| success_return_url | 5 | Controlled by `flags`; present when this bit is set. |
| fail_return_url | 6 | Controlled by `flags`; present when this bit is set. |
| crypto_amount | 7 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import PaymentsCreateOnrampSession
```

Public access: `miniproto.raw.functions.PaymentsCreateOnrampSession`.

## Class reference

```python
from miniproto.raw.functions import PaymentsCreateOnrampSession

# Refer to the raw request class without constructing it or calling Telegram
request_type = PaymentsCreateOnrampSession
```

## Result family

[`OnrampSession`](/reference/telegram/types/results/onramp-session/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`OnrampSession`](/reference/telegram/types/results/onramp-session/)
Known selected constructors: [`onrampSession`](/reference/telegram/types/base/onramp-session/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
