---
title: "secureValue"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "secureValue"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x187fa0ca"
---

# `secureValue`

No description provided by the pinned schema.

## Signature

```tl
secureValue#187fa0ca flags:# type:SecureValueType data:flags.0?SecureData front_side:flags.1?SecureFile reverse_side:flags.2?SecureFile selfie:flags.3?SecureFile translation:flags.6?Vector<SecureFile> files:flags.4?Vector<SecureFile> plain_data:flags.5?SecurePlainData hash:bytes = SecureValue;
```

## Result type

`SecureValue`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| type | SecureValueType | — | — | No description provided by the pinned schema. |
| data | flags.0?SecureData | flags.0 | — | No description provided by the pinned schema. |
| front_side | flags.1?SecureFile | flags.1 | — | No description provided by the pinned schema. |
| reverse_side | flags.2?SecureFile | flags.2 | — | No description provided by the pinned schema. |
| selfie | flags.3?SecureFile | flags.3 | — | No description provided by the pinned schema. |
| translation | flags.6?Vector<SecureFile> | flags.6 | — | No description provided by the pinned schema. |
| files | flags.4?Vector<SecureFile> | flags.4 | — | No description provided by the pinned schema. |
| plain_data | flags.5?SecurePlainData | flags.5 | — | No description provided by the pinned schema. |
| hash | bytes | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| data | 0 | Controlled by `flags`; present when this bit is set. |
| front_side | 1 | Controlled by `flags`; present when this bit is set. |
| reverse_side | 2 | Controlled by `flags`; present when this bit is set. |
| selfie | 3 | Controlled by `flags`; present when this bit is set. |
| translation | 6 | Controlled by `flags`; present when this bit is set. |
| files | 4 | Controlled by `flags`; present when this bit is set. |
| plain_data | 5 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import SecureValue
```

Public access: `miniproto.raw.types.SecureValue`.

## Safe usage shape

```python
from miniproto.raw.types import SecureValue

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = SecureValue
```

## Result family

[`SecureValue`](/reference/telegram/types/results/secure-value/)

## Relationships

- Result family: [`SecureValue`](/reference/telegram/types/results/secure-value/)
- Accepted by: [`account.authorizationForm`](/reference/telegram/types/account/authorization-form/), [`messageActionSecureValuesSentMe`](/reference/telegram/types/base/message-action-secure-values-sent-me/)
- Returned by: [`account.getAllSecureValues`](/reference/telegram/functions/account/get-all-secure-values/), [`account.getSecureValue`](/reference/telegram/functions/account/get-secure-value/), [`account.saveSecureValue`](/reference/telegram/functions/account/save-secure-value/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
