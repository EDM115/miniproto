---
title: "account.password"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.password"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0x957b50fb"
---

# `account.password`

No description provided by the pinned schema.

## Signature

```tl
account.password#957b50fb flags:# has_recovery:flags.0?true has_secure_values:flags.1?true has_password:flags.2?true current_algo:flags.2?PasswordKdfAlgo srp_B:flags.2?bytes srp_id:flags.2?long hint:flags.3?string email_unconfirmed_pattern:flags.4?string new_algo:PasswordKdfAlgo new_secure_algo:SecurePasswordKdfAlgo secure_random:bytes pending_reset_date:flags.5?int login_email_pattern:flags.6?string = account.Password;
```

## Result type

`account.Password`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| has_recovery | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| has_secure_values | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| has_password | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| current_algo | flags.2?PasswordKdfAlgo | flags.2 | — | No description provided by the pinned schema. |
| srp_B | flags.2?bytes | flags.2 | — | No description provided by the pinned schema. |
| srp_id | flags.2?long | flags.2 | — | No description provided by the pinned schema. |
| hint | flags.3?string | flags.3 | — | No description provided by the pinned schema. |
| email_unconfirmed_pattern | flags.4?string | flags.4 | — | No description provided by the pinned schema. |
| new_algo | PasswordKdfAlgo | — | — | No description provided by the pinned schema. |
| new_secure_algo | SecurePasswordKdfAlgo | — | — | No description provided by the pinned schema. |
| secure_random | bytes | — | — | No description provided by the pinned schema. |
| pending_reset_date | flags.5?int | flags.5 | — | No description provided by the pinned schema. |
| login_email_pattern | flags.6?string | flags.6 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| has_recovery | 0 | Controlled by `flags`; present when this bit is set. |
| has_secure_values | 1 | Controlled by `flags`; present when this bit is set. |
| has_password | 2 | Controlled by `flags`; present when this bit is set. |
| current_algo | 2 | Controlled by `flags`; present when this bit is set. |
| srp_B | 2 | Controlled by `flags`; present when this bit is set. |
| srp_id | 2 | Controlled by `flags`; present when this bit is set. |
| hint | 3 | Controlled by `flags`; present when this bit is set. |
| email_unconfirmed_pattern | 4 | Controlled by `flags`; present when this bit is set. |
| pending_reset_date | 5 | Controlled by `flags`; present when this bit is set. |
| login_email_pattern | 6 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import AccountPassword
```

Public access: `miniproto.raw.types.AccountPassword`.

## Safe usage shape

```python
from miniproto.raw.types import AccountPassword

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountPassword
```

## Result family

[`account.Password`](/reference/telegram/types/results/account-password/)

## Relationships

- Result family: [`account.Password`](/reference/telegram/types/results/account-password/)
- Returned by: [`account.getPassword`](/reference/telegram/functions/account/get-password/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
