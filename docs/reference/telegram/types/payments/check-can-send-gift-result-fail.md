---
title: "payments.checkCanSendGiftResultFail"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.checkCanSendGiftResultFail"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0xd5e58274"
---

# `payments.checkCanSendGiftResultFail`

No description provided by the pinned schema.

## Signature

```tl
payments.checkCanSendGiftResultFail#d5e58274 reason:TextWithEntities = payments.CheckCanSendGiftResult;
```

## Result type

`payments.CheckCanSendGiftResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| reason | TextWithEntities | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PaymentsCheckCanSendGiftResultFail
```

Public access: `miniproto.raw.types.PaymentsCheckCanSendGiftResultFail`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsCheckCanSendGiftResultFail

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsCheckCanSendGiftResultFail
```

## Result family

[`payments.CheckCanSendGiftResult`](/reference/telegram/types/results/payments-check-can-send-gift-result/)

## Relationships

- Result family: [`payments.CheckCanSendGiftResult`](/reference/telegram/types/results/payments-check-can-send-gift-result/)
- Related constructors: [`payments.checkCanSendGiftResultOk`](/reference/telegram/types/payments/check-can-send-gift-result-ok/)
- Returned by: [`payments.checkCanSendGift`](/reference/telegram/functions/payments/check-can-send-gift/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
