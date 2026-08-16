---
title: "passkey"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "passkey"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x98613ebf"
---

# `passkey`

No description provided by the pinned schema.

## Signature

```tl
passkey#98613ebf flags:# id:string name:string date:int software_emoji_id:flags.0?long last_usage_date:flags.1?int = Passkey;
```

## Result type

`Passkey`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| id | string | — | — | No description provided by the pinned schema. |
| name | string | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| software_emoji_id | flags.0?long | flags.0 | — | No description provided by the pinned schema. |
| last_usage_date | flags.1?int | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| software_emoji_id | 0 | Controlled by `flags`; present when this bit is set. |
| last_usage_date | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import Passkey
```

Public access: `miniproto.raw.types.Passkey`.

## Safe usage shape

```python
from miniproto.raw.types import Passkey

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = Passkey
```

## Result family

[`Passkey`](/reference/telegram/types/results/passkey/)

## Relationships

- Result family: [`Passkey`](/reference/telegram/types/results/passkey/)
- Accepted by: [`account.passkeys`](/reference/telegram/types/account/passkeys/)
- Returned by: [`account.registerPasskey`](/reference/telegram/functions/account/register-passkey/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
