---
title: "webAuthorization"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "webAuthorization"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xa6f8f452"
---

# `webAuthorization`

No description provided by the pinned schema.

## Signature

```tl
webAuthorization#a6f8f452 hash:long bot_id:long domain:string browser:string platform:string date_created:int date_active:int ip:string region:string = WebAuthorization;
```

## Result type

`WebAuthorization`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | long | — | — | No description provided by the pinned schema. |
| bot_id | long | — | — | No description provided by the pinned schema. |
| domain | string | — | — | No description provided by the pinned schema. |
| browser | string | — | — | No description provided by the pinned schema. |
| platform | string | — | — | No description provided by the pinned schema. |
| date_created | int | — | — | No description provided by the pinned schema. |
| date_active | int | — | — | No description provided by the pinned schema. |
| ip | string | — | — | No description provided by the pinned schema. |
| region | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import WebAuthorization
```

Public access: `miniproto.raw.types.WebAuthorization`.

## Safe usage shape

```python
from miniproto.raw.types import WebAuthorization

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = WebAuthorization
```

## Result family

[`WebAuthorization`](/reference/telegram/types/results/web-authorization/)

## Relationships

- Result family: [`WebAuthorization`](/reference/telegram/types/results/web-authorization/)
- Accepted by: [`account.webAuthorizations`](/reference/telegram/types/account/web-authorizations/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
