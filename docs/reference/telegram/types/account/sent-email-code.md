---
title: "account.sentEmailCode"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.sentEmailCode"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0x811f854f"
---

# `account.sentEmailCode`

No description provided by the pinned schema.

## Signature

```tl
account.sentEmailCode#811f854f email_pattern:string length:int = account.SentEmailCode;
```

## Result type

`account.SentEmailCode`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| email_pattern | string | — | — | No description provided by the pinned schema. |
| length | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AccountSentEmailCode
```

Public access: `miniproto.raw.types.AccountSentEmailCode`.

## Safe usage shape

```python
from miniproto.raw.types import AccountSentEmailCode

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountSentEmailCode
```

## Result family

[`account.SentEmailCode`](/reference/telegram/types/results/account-sent-email-code/)

## Relationships

- Result family: [`account.SentEmailCode`](/reference/telegram/types/results/account-sent-email-code/)
- Returned by: [`account.sendVerifyEmailCode`](/reference/telegram/functions/account/send-verify-email-code/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
