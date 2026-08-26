---
title: "secureValueTypeUtilityBill"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "secureValueTypeUtilityBill"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xfc36954e"
---

# `secureValueTypeUtilityBill`

No description provided by the pinned schema.

## Signature

```tl
secureValueTypeUtilityBill#fc36954e = SecureValueType;
```

## Result type

`SecureValueType`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import SecureValueTypeUtilityBill
```

Public access: `miniproto.raw.types.SecureValueTypeUtilityBill`.

## Safe usage shape

```python
from miniproto.raw.types import SecureValueTypeUtilityBill

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = SecureValueTypeUtilityBill
```

## Result family

[`SecureValueType`](/reference/telegram/types/results/secure-value-type/)

## Relationships

- Result family: [`SecureValueType`](/reference/telegram/types/results/secure-value-type/)
- Related constructors: [`secureValueTypeAddress`](/reference/telegram/types/base/secure-value-type-address/), [`secureValueTypeBankStatement`](/reference/telegram/types/base/secure-value-type-bank-statement/), [`secureValueTypeDriverLicense`](/reference/telegram/types/base/secure-value-type-driver-license/), [`secureValueTypeEmail`](/reference/telegram/types/base/secure-value-type-email/), [`secureValueTypeIdentityCard`](/reference/telegram/types/base/secure-value-type-identity-card/), [`secureValueTypeInternalPassport`](/reference/telegram/types/base/secure-value-type-internal-passport/), [`secureValueTypePassport`](/reference/telegram/types/base/secure-value-type-passport/), [`secureValueTypePassportRegistration`](/reference/telegram/types/base/secure-value-type-passport-registration/), [`secureValueTypePersonalDetails`](/reference/telegram/types/base/secure-value-type-personal-details/), [`secureValueTypePhone`](/reference/telegram/types/base/secure-value-type-phone/), [`secureValueTypeRentalAgreement`](/reference/telegram/types/base/secure-value-type-rental-agreement/), [`secureValueTypeTemporaryRegistration`](/reference/telegram/types/base/secure-value-type-temporary-registration/)
- Accepted by: [`account.deleteSecureValue`](/reference/telegram/functions/account/delete-secure-value/), [`account.getSecureValue`](/reference/telegram/functions/account/get-secure-value/), [`inputSecureValue`](/reference/telegram/types/base/input-secure-value/), [`messageActionSecureValuesSent`](/reference/telegram/types/base/message-action-secure-values-sent/), [`secureRequiredType`](/reference/telegram/types/base/secure-required-type/), [`secureValue`](/reference/telegram/types/base/secure-value/), [`secureValueError`](/reference/telegram/types/base/secure-value-error/), [`secureValueErrorData`](/reference/telegram/types/base/secure-value-error-data/), [`secureValueErrorFile`](/reference/telegram/types/base/secure-value-error-file/), [`secureValueErrorFiles`](/reference/telegram/types/base/secure-value-error-files/), [`secureValueErrorFrontSide`](/reference/telegram/types/base/secure-value-error-front-side/), [`secureValueErrorReverseSide`](/reference/telegram/types/base/secure-value-error-reverse-side/), [`secureValueErrorSelfie`](/reference/telegram/types/base/secure-value-error-selfie/), [`secureValueErrorTranslationFile`](/reference/telegram/types/base/secure-value-error-translation-file/), [`secureValueErrorTranslationFiles`](/reference/telegram/types/base/secure-value-error-translation-files/), [`secureValueHash`](/reference/telegram/types/base/secure-value-hash/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
