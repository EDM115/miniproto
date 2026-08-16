---
title: "auth.sentCodeTypeFirebaseSms"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "auth.sentCodeTypeFirebaseSms"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
layer: 228
schema_source: "tdlib"
constructor_id: "0x009fd736"
---

# `auth.sentCodeTypeFirebaseSms`

No description provided by the pinned schema.

## Signature

```tl
auth.sentCodeTypeFirebaseSms#009fd736 flags:# nonce:flags.0?bytes play_integrity_project_id:flags.2?long play_integrity_nonce:flags.2?bytes receipt:flags.1?string push_timeout:flags.1?int length:int = auth.SentCodeType;
```

## Result type

`auth.SentCodeType`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| nonce | flags.0?bytes | flags.0 | — | No description provided by the pinned schema. |
| play_integrity_project_id | flags.2?long | flags.2 | — | No description provided by the pinned schema. |
| play_integrity_nonce | flags.2?bytes | flags.2 | — | No description provided by the pinned schema. |
| receipt | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| push_timeout | flags.1?int | flags.1 | — | No description provided by the pinned schema. |
| length | int | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| nonce | 0 | Controlled by `flags`; present when this bit is set. |
| play_integrity_project_id | 2 | Controlled by `flags`; present when this bit is set. |
| play_integrity_nonce | 2 | Controlled by `flags`; present when this bit is set. |
| receipt | 1 | Controlled by `flags`; present when this bit is set. |
| push_timeout | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import AuthSentCodeTypeFirebaseSms
```

Public access: `miniproto.raw.types.AuthSentCodeTypeFirebaseSms`.

## Safe usage shape

```python
from miniproto.raw.types import AuthSentCodeTypeFirebaseSms

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AuthSentCodeTypeFirebaseSms
```

## Result family

[`auth.SentCodeType`](/reference/telegram/types/results/auth-sent-code-type/)

## Relationships

- Result family: [`auth.SentCodeType`](/reference/telegram/types/results/auth-sent-code-type/)
- Related constructors: [`auth.sentCodeTypeApp`](/reference/telegram/types/auth/sent-code-type-app/), [`auth.sentCodeTypeCall`](/reference/telegram/types/auth/sent-code-type-call/), [`auth.sentCodeTypeEmailCode`](/reference/telegram/types/auth/sent-code-type-email-code/), [`auth.sentCodeTypeFlashCall`](/reference/telegram/types/auth/sent-code-type-flash-call/), [`auth.sentCodeTypeFragmentSms`](/reference/telegram/types/auth/sent-code-type-fragment-sms/), [`auth.sentCodeTypeMissedCall`](/reference/telegram/types/auth/sent-code-type-missed-call/), [`auth.sentCodeTypeSetUpEmailRequired`](/reference/telegram/types/auth/sent-code-type-set-up-email-required/), [`auth.sentCodeTypeSms`](/reference/telegram/types/auth/sent-code-type-sms/), [`auth.sentCodeTypeSmsPhrase`](/reference/telegram/types/auth/sent-code-type-sms-phrase/), [`auth.sentCodeTypeSmsWord`](/reference/telegram/types/auth/sent-code-type-sms-word/)
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
