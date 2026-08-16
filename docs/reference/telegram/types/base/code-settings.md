---
title: "codeSettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "codeSettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xad253d78"
---

# `codeSettings`

No description provided by the pinned schema.

## Signature

```tl
codeSettings#ad253d78 flags:# allow_flashcall:flags.0?true current_number:flags.1?true allow_app_hash:flags.4?true allow_missed_call:flags.5?true allow_firebase:flags.7?true unknown_number:flags.9?true logout_tokens:flags.6?Vector<bytes> token:flags.8?string app_sandbox:flags.8?Bool = CodeSettings;
```

## Result type

`CodeSettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| allow_flashcall | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| current_number | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| allow_app_hash | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| allow_missed_call | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| allow_firebase | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| unknown_number | flags.9?true | flags.9 | — | No description provided by the pinned schema. |
| logout_tokens | flags.6?Vector<bytes> | flags.6 | — | No description provided by the pinned schema. |
| token | flags.8?string | flags.8 | — | No description provided by the pinned schema. |
| app_sandbox | flags.8?Bool | flags.8 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| allow_flashcall | 0 | Controlled by `flags`; present when this bit is set. |
| current_number | 1 | Controlled by `flags`; present when this bit is set. |
| allow_app_hash | 4 | Controlled by `flags`; present when this bit is set. |
| allow_missed_call | 5 | Controlled by `flags`; present when this bit is set. |
| allow_firebase | 7 | Controlled by `flags`; present when this bit is set. |
| unknown_number | 9 | Controlled by `flags`; present when this bit is set. |
| logout_tokens | 6 | Controlled by `flags`; present when this bit is set. |
| token | 8 | Controlled by `flags`; present when this bit is set. |
| app_sandbox | 8 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import CodeSettings
```

Public access: `miniproto.raw.types.CodeSettings`.

## Safe usage shape

```python
from miniproto.raw.types import CodeSettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = CodeSettings
```

## Result family

[`CodeSettings`](/reference/telegram/types/results/code-settings/)

## Relationships

- Result family: [`CodeSettings`](/reference/telegram/types/results/code-settings/)
- Accepted by: [`account.sendChangePhoneCode`](/reference/telegram/functions/account/send-change-phone-code/), [`account.sendConfirmPhoneCode`](/reference/telegram/functions/account/send-confirm-phone-code/), [`account.sendVerifyPhoneCode`](/reference/telegram/functions/account/send-verify-phone-code/), [`auth.sendCode`](/reference/telegram/functions/auth/send-code/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
