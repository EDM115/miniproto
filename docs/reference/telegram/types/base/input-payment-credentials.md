---
title: "inputPaymentCredentials"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputPaymentCredentials"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x3417d728"
---

# `inputPaymentCredentials`

No description provided by the pinned schema.

## Signature

```tl
inputPaymentCredentials#3417d728 flags:# save:flags.0?true data:DataJSON = InputPaymentCredentials;
```

## Result type

`InputPaymentCredentials`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| save | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| data | DataJSON | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| save | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputPaymentCredentials
```

Public access: `miniproto.raw.types.InputPaymentCredentials`.

## Safe usage shape

```python
from miniproto.raw.types import InputPaymentCredentials

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputPaymentCredentials
```

## Result family

[`InputPaymentCredentials`](/reference/telegram/types/results/input-payment-credentials/)

## Relationships

- Result family: [`InputPaymentCredentials`](/reference/telegram/types/results/input-payment-credentials/)
- Related constructors: [`inputPaymentCredentialsApplePay`](/reference/telegram/types/base/input-payment-credentials-apple-pay/), [`inputPaymentCredentialsGooglePay`](/reference/telegram/types/base/input-payment-credentials-google-pay/), [`inputPaymentCredentialsSaved`](/reference/telegram/types/base/input-payment-credentials-saved/)
- Accepted by: [`payments.sendPaymentForm`](/reference/telegram/functions/payments/send-payment-form/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
