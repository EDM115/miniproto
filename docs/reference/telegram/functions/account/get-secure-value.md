---
title: "account.getSecureValue"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "account.getSecureValue"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0x73665bc2"
---

# `account.getSecureValue`

No description provided by the pinned schema.

## Signature

```tl
account.getSecureValue#73665bc2 types:Vector<SecureValueType> = Vector<SecureValue>;
```

## Result type

`Vector<SecureValue>`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| types | Vector<SecureValueType> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import AccountGetSecureValue
```

Public access: `miniproto.raw.functions.AccountGetSecureValue`.

## Safe usage shape

```python
from miniproto.raw.functions import AccountGetSecureValue

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = AccountGetSecureValue
```

## Result family

[`SecureValue`](/reference/telegram/types/results/secure-value/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`SecureValueType`](/reference/telegram/types/results/secure-value-type/)
Known selected constructors: [`secureValueTypeAddress`](/reference/telegram/types/base/secure-value-type-address/), [`secureValueTypeBankStatement`](/reference/telegram/types/base/secure-value-type-bank-statement/), [`secureValueTypeDriverLicense`](/reference/telegram/types/base/secure-value-type-driver-license/), [`secureValueTypeEmail`](/reference/telegram/types/base/secure-value-type-email/), [`secureValueTypeIdentityCard`](/reference/telegram/types/base/secure-value-type-identity-card/), [`secureValueTypeInternalPassport`](/reference/telegram/types/base/secure-value-type-internal-passport/), [`secureValueTypePassport`](/reference/telegram/types/base/secure-value-type-passport/), [`secureValueTypePassportRegistration`](/reference/telegram/types/base/secure-value-type-passport-registration/), [`secureValueTypePersonalDetails`](/reference/telegram/types/base/secure-value-type-personal-details/), [`secureValueTypePhone`](/reference/telegram/types/base/secure-value-type-phone/), [`secureValueTypeRentalAgreement`](/reference/telegram/types/base/secure-value-type-rental-agreement/), [`secureValueTypeTemporaryRegistration`](/reference/telegram/types/base/secure-value-type-temporary-registration/), [`secureValueTypeUtilityBill`](/reference/telegram/types/base/secure-value-type-utility-bill/)

## Returned types

[`SecureValue`](/reference/telegram/types/results/secure-value/)
Known selected constructors: [`secureValue`](/reference/telegram/types/base/secure-value/)

## Related methods

[`account.deleteSecureValue`](/reference/telegram/functions/account/delete-secure-value/), [`account.getAllSecureValues`](/reference/telegram/functions/account/get-all-secure-values/), [`account.saveSecureValue`](/reference/telegram/functions/account/save-secure-value/)

## Availability evidence

- user only

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
