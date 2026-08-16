---
title: "auth.sentCodeTypeFragmentSms"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "auth.sentCodeTypeFragmentSms"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
layer: 228
schema_source: "tdlib"
constructor_id: "0xd9565c39"
---

# `auth.sentCodeTypeFragmentSms`

No description provided by the pinned schema.

## Signature

```tl
auth.sentCodeTypeFragmentSms#d9565c39 url:string length:int = auth.SentCodeType;
```

## Result type

`auth.SentCodeType`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| url | string | — | — | No description provided by the pinned schema. |
| length | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AuthSentCodeTypeFragmentSms
```

Public access: `miniproto.raw.types.AuthSentCodeTypeFragmentSms`.

## Safe usage shape

```python
from miniproto.raw.types import AuthSentCodeTypeFragmentSms

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AuthSentCodeTypeFragmentSms
```

## Result family

[`auth.SentCodeType`](/reference/telegram/types/results/auth-sent-code-type/)

## Relationships

- Result family: [`auth.SentCodeType`](/reference/telegram/types/results/auth-sent-code-type/)
- Related constructors: [`auth.sentCodeTypeApp`](/reference/telegram/types/auth/sent-code-type-app/), [`auth.sentCodeTypeCall`](/reference/telegram/types/auth/sent-code-type-call/), [`auth.sentCodeTypeEmailCode`](/reference/telegram/types/auth/sent-code-type-email-code/), [`auth.sentCodeTypeFirebaseSms`](/reference/telegram/types/auth/sent-code-type-firebase-sms/), [`auth.sentCodeTypeFlashCall`](/reference/telegram/types/auth/sent-code-type-flash-call/), [`auth.sentCodeTypeMissedCall`](/reference/telegram/types/auth/sent-code-type-missed-call/), [`auth.sentCodeTypeSetUpEmailRequired`](/reference/telegram/types/auth/sent-code-type-set-up-email-required/), [`auth.sentCodeTypeSms`](/reference/telegram/types/auth/sent-code-type-sms/), [`auth.sentCodeTypeSmsPhrase`](/reference/telegram/types/auth/sent-code-type-sms-phrase/), [`auth.sentCodeTypeSmsWord`](/reference/telegram/types/auth/sent-code-type-sms-word/)
- Accepted by: [`auth.sentCode`](/reference/telegram/types/auth/sent-code/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
