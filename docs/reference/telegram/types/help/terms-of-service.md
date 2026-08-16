---
title: "help.termsOfService"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.termsOfService"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
layer: 228
schema_source: "tdlib"
constructor_id: "0x780a0310"
---

# `help.termsOfService`

No description provided by the pinned schema.

## Signature

```tl
help.termsOfService#780a0310 flags:# popup:flags.0?true id:DataJSON text:string entities:Vector<MessageEntity> min_age_confirm:flags.1?int = help.TermsOfService;
```

## Result type

`help.TermsOfService`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| popup | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| id | DataJSON | — | — | No description provided by the pinned schema. |
| text | string | — | — | No description provided by the pinned schema. |
| entities | Vector<MessageEntity> | — | — | No description provided by the pinned schema. |
| min_age_confirm | flags.1?int | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| popup | 0 | Controlled by `flags`; present when this bit is set. |
| min_age_confirm | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import HelpTermsOfService
```

Public access: `miniproto.raw.types.HelpTermsOfService`.

## Safe usage shape

```python
from miniproto.raw.types import HelpTermsOfService

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = HelpTermsOfService
```

## Result family

[`help.TermsOfService`](/reference/telegram/types/results/help-terms-of-service/)

## Relationships

- Result family: [`help.TermsOfService`](/reference/telegram/types/results/help-terms-of-service/)
- Accepted by: [`auth.authorizationSignUpRequired`](/reference/telegram/types/auth/authorization-sign-up-required/), [`help.termsOfServiceUpdate`](/reference/telegram/types/help/terms-of-service-update/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
