---
title: "payments.bankCardData"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.bankCardData"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0x3e24e573"
---

# `payments.bankCardData`

No description provided by the pinned schema.

## Signature

```tl
payments.bankCardData#3e24e573 title:string open_urls:Vector<BankCardOpenUrl> = payments.BankCardData;
```

## Result type

`payments.BankCardData`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| title | string | — | — | No description provided by the pinned schema. |
| open_urls | Vector<BankCardOpenUrl> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PaymentsBankCardData
```

Public access: `miniproto.raw.types.PaymentsBankCardData`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsBankCardData

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsBankCardData
```

## Result family

[`payments.BankCardData`](/reference/telegram/types/results/payments-bank-card-data/)

## Relationships

- Result family: [`payments.BankCardData`](/reference/telegram/types/results/payments-bank-card-data/)
- Returned by: [`payments.getBankCardData`](/reference/telegram/functions/payments/get-bank-card-data/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
