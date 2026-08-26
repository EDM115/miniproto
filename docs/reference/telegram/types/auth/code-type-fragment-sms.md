---
title: "auth.codeTypeFragmentSms"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "auth.codeTypeFragmentSms"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
schema_source: "tdlib"
constructor_id: "0x06ed998c"
---

# `auth.codeTypeFragmentSms`

No description provided by the pinned schema.

## Signature

```tl
auth.codeTypeFragmentSms#06ed998c = auth.CodeType;
```

## Result type

`auth.CodeType`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import AuthCodeTypeFragmentSms
```

Public access: `miniproto.raw.types.AuthCodeTypeFragmentSms`.

## Safe usage shape

```python
from miniproto.raw.types import AuthCodeTypeFragmentSms

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AuthCodeTypeFragmentSms
```

## Result family

[`auth.CodeType`](/reference/telegram/types/results/auth-code-type/)

## Relationships

- Result family: [`auth.CodeType`](/reference/telegram/types/results/auth-code-type/)
- Related constructors: [`auth.codeTypeCall`](/reference/telegram/types/auth/code-type-call/), [`auth.codeTypeFlashCall`](/reference/telegram/types/auth/code-type-flash-call/), [`auth.codeTypeMissedCall`](/reference/telegram/types/auth/code-type-missed-call/), [`auth.codeTypeSms`](/reference/telegram/types/auth/code-type-sms/)
- Accepted by: [`auth.sentCode`](/reference/telegram/types/auth/sent-code/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
