---
title: "inputPaymentCredentialsSaved"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputPaymentCredentialsSaved"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xc10eb2cf"
---

# `inputPaymentCredentialsSaved`

No description provided by the pinned schema.

## Signature

```tl
inputPaymentCredentialsSaved#c10eb2cf id:string tmp_password:bytes = InputPaymentCredentials;
```

## Result type

`InputPaymentCredentials`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | string | — | — | No description provided by the pinned schema. |
| tmp_password | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputPaymentCredentialsSaved
```

Public access: `miniproto.raw.types.InputPaymentCredentialsSaved`.

## Class reference

```python
from miniproto.raw.types import InputPaymentCredentialsSaved

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = InputPaymentCredentialsSaved
```

## Result family

[`InputPaymentCredentials`](/reference/telegram/types/results/input-payment-credentials/)

## Relationships

- Result family: [`InputPaymentCredentials`](/reference/telegram/types/results/input-payment-credentials/)
- Related constructors: [`inputPaymentCredentials`](/reference/telegram/types/base/input-payment-credentials/), [`inputPaymentCredentialsApplePay`](/reference/telegram/types/base/input-payment-credentials-apple-pay/), [`inputPaymentCredentialsGooglePay`](/reference/telegram/types/base/input-payment-credentials-google-pay/)
- Accepted by: [`payments.sendPaymentForm`](/reference/telegram/functions/payments/send-payment-form/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
