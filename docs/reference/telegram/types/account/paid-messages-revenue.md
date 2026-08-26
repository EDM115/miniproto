---
title: "account.paidMessagesRevenue"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.paidMessagesRevenue"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0x1e109708"
---

# `account.paidMessagesRevenue`

No description provided by the pinned schema.

## Signature

```tl
account.paidMessagesRevenue#1e109708 stars_amount:long = account.PaidMessagesRevenue;
```

## Result type

`account.PaidMessagesRevenue`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| stars_amount | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AccountPaidMessagesRevenue
```

Public access: `miniproto.raw.types.AccountPaidMessagesRevenue`.

## Safe usage shape

```python
from miniproto.raw.types import AccountPaidMessagesRevenue

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountPaidMessagesRevenue
```

## Result family

[`account.PaidMessagesRevenue`](/reference/telegram/types/results/account-paid-messages-revenue/)

## Relationships

- Result family: [`account.PaidMessagesRevenue`](/reference/telegram/types/results/account-paid-messages-revenue/)
- Returned by: [`account.getPaidMessagesRevenue`](/reference/telegram/functions/account/get-paid-messages-revenue/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
