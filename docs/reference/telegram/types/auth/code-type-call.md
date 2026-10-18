---
title: "auth.codeTypeCall"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "auth.codeTypeCall"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
schema_source: "tdlib"
constructor_id: "0x741cd3e3"
---

# `auth.codeTypeCall`

No description provided by the pinned schema.

## Signature

```tl
auth.codeTypeCall#741cd3e3 = auth.CodeType;
```

## Result type

`auth.CodeType`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import AuthCodeTypeCall
```

Public access: `miniproto.raw.types.AuthCodeTypeCall`.

## Class reference

```python
from miniproto.raw.types import AuthCodeTypeCall

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = AuthCodeTypeCall
```

## Result family

[`auth.CodeType`](/reference/telegram/types/results/auth-code-type/)

## Relationships

- Result family: [`auth.CodeType`](/reference/telegram/types/results/auth-code-type/)
- Related constructors: [`auth.codeTypeFlashCall`](/reference/telegram/types/auth/code-type-flash-call/), [`auth.codeTypeFragmentSms`](/reference/telegram/types/auth/code-type-fragment-sms/), [`auth.codeTypeMissedCall`](/reference/telegram/types/auth/code-type-missed-call/), [`auth.codeTypeSms`](/reference/telegram/types/auth/code-type-sms/)
- Accepted by: [`auth.sentCode`](/reference/telegram/types/auth/sent-code/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
