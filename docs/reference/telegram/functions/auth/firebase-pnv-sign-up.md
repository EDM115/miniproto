---
title: "auth.firebasePnvSignUp"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "auth.firebasePnvSignUp"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "auth"
schema_source: "tdlib"
constructor_id: "0x783f6b56"
---

# `auth.firebasePnvSignUp`

No description provided by the pinned schema.

## Signature

```tl
auth.firebasePnvSignUp#783f6b56 flags:# no_joined_notifications:flags.0?true first_name:string last_name:string = auth.Authorization;
```

## Result type

`auth.Authorization`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| no_joined_notifications | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| first_name | string | — | — | No description provided by the pinned schema. |
| last_name | string | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| no_joined_notifications | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import AuthFirebasePnvSignUp
```

Public access: `miniproto.raw.functions.AuthFirebasePnvSignUp`.

## Safe usage shape

```python
from miniproto.raw.functions import AuthFirebasePnvSignUp

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AuthFirebasePnvSignUp
```

## Result family

[`auth.Authorization`](/reference/telegram/types/results/auth-authorization/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`auth.Authorization`](/reference/telegram/types/results/auth-authorization/)
Known selected constructors: [`auth.authorization`](/reference/telegram/types/auth/authorization/), [`auth.authorizationSignUpRequired`](/reference/telegram/types/auth/authorization-sign-up-required/)

## Related methods

[`auth.checkPassword`](/reference/telegram/functions/auth/check-password/), [`auth.finishFirebasePnvLogin`](/reference/telegram/functions/auth/finish-firebase-pnv-login/), [`auth.finishPasskeyLogin`](/reference/telegram/functions/auth/finish-passkey-login/), [`auth.importAuthorization`](/reference/telegram/functions/auth/import-authorization/), [`auth.importBotAuthorization`](/reference/telegram/functions/auth/import-bot-authorization/), [`auth.importWebTokenAuthorization`](/reference/telegram/functions/auth/import-web-token-authorization/), [`auth.recoverPassword`](/reference/telegram/functions/auth/recover-password/), [`auth.signIn`](/reference/telegram/functions/auth/sign-in/), [`auth.signUp`](/reference/telegram/functions/auth/sign-up/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
