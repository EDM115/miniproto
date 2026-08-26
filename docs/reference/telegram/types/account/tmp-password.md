---
title: "account.tmpPassword"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.tmpPassword"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0xdb64fd34"
---

# `account.tmpPassword`

No description provided by the pinned schema.

## Signature

```tl
account.tmpPassword#db64fd34 tmp_password:bytes valid_until:int = account.TmpPassword;
```

## Result type

`account.TmpPassword`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| tmp_password | bytes | — | — | No description provided by the pinned schema. |
| valid_until | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AccountTmpPassword
```

Public access: `miniproto.raw.types.AccountTmpPassword`.

## Safe usage shape

```python
from miniproto.raw.types import AccountTmpPassword

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountTmpPassword
```

## Result family

[`account.TmpPassword`](/reference/telegram/types/results/account-tmp-password/)

## Relationships

- Result family: [`account.TmpPassword`](/reference/telegram/types/results/account-tmp-password/)
- Returned by: [`account.getTmpPassword`](/reference/telegram/functions/account/get-tmp-password/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
