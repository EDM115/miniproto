---
title: "auth.sentCodeTypeFlashCall"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "auth.sentCodeTypeFlashCall"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
schema_source: "tdlib"
constructor_id: "0xab03c6d9"
---

# `auth.sentCodeTypeFlashCall`

No description provided by the pinned schema.

## Signature

```tl
auth.sentCodeTypeFlashCall#ab03c6d9 pattern:string = auth.SentCodeType;
```

## Result type

`auth.SentCodeType`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| pattern | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AuthSentCodeTypeFlashCall
```

Public access: `miniproto.raw.types.AuthSentCodeTypeFlashCall`.

## Safe usage shape

```python
from miniproto.raw.types import AuthSentCodeTypeFlashCall

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AuthSentCodeTypeFlashCall
```

## Result family

[`auth.SentCodeType`](/reference/telegram/types/results/auth-sent-code-type/)

## Relationships

- Result family: [`auth.SentCodeType`](/reference/telegram/types/results/auth-sent-code-type/)
- Related constructors: [`auth.sentCodeTypeApp`](/reference/telegram/types/auth/sent-code-type-app/), [`auth.sentCodeTypeCall`](/reference/telegram/types/auth/sent-code-type-call/), [`auth.sentCodeTypeEmailCode`](/reference/telegram/types/auth/sent-code-type-email-code/), [`auth.sentCodeTypeFirebaseSms`](/reference/telegram/types/auth/sent-code-type-firebase-sms/), [`auth.sentCodeTypeFragmentSms`](/reference/telegram/types/auth/sent-code-type-fragment-sms/), [`auth.sentCodeTypeMissedCall`](/reference/telegram/types/auth/sent-code-type-missed-call/), [`auth.sentCodeTypeSetUpEmailRequired`](/reference/telegram/types/auth/sent-code-type-set-up-email-required/), [`auth.sentCodeTypeSms`](/reference/telegram/types/auth/sent-code-type-sms/), [`auth.sentCodeTypeSmsPhrase`](/reference/telegram/types/auth/sent-code-type-sms-phrase/), [`auth.sentCodeTypeSmsWord`](/reference/telegram/types/auth/sent-code-type-sms-word/)
- Accepted by: [`auth.sentCode`](/reference/telegram/types/auth/sent-code/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
