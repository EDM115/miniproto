---
title: "account.passkeys"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.passkeys"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0xf8e0aa1c"
---

# `account.passkeys`

No description provided by the pinned schema.

## Signature

```tl
account.passkeys#f8e0aa1c passkeys:Vector<Passkey> = account.Passkeys;
```

## Result type

`account.Passkeys`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| passkeys | Vector<Passkey> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AccountPasskeys
```

Public access: `miniproto.raw.types.AccountPasskeys`.

## Class reference

```python
from miniproto.raw.types import AccountPasskeys

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = AccountPasskeys
```

## Result family

[`account.Passkeys`](/reference/telegram/types/results/account-passkeys/)

## Relationships

- Result family: [`account.Passkeys`](/reference/telegram/types/results/account-passkeys/)
- Returned by: [`account.getPasskeys`](/reference/telegram/functions/account/get-passkeys/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
