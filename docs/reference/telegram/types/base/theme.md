---
title: "theme"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "theme"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xa00e67d6"
---

# `theme`

No description provided by the pinned schema.

## Signature

```tl
theme#a00e67d6 flags:# creator:flags.0?true default:flags.1?true for_chat:flags.5?true id:long access_hash:long slug:string title:string document:flags.2?Document settings:flags.3?Vector<ThemeSettings> emoticon:flags.6?string installs_count:flags.4?int = Theme;
```

## Result type

`Theme`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| creator | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| default | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| for_chat | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |
| slug | string | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| document | flags.2?Document | flags.2 | — | No description provided by the pinned schema. |
| settings | flags.3?Vector<ThemeSettings> | flags.3 | — | No description provided by the pinned schema. |
| emoticon | flags.6?string | flags.6 | — | No description provided by the pinned schema. |
| installs_count | flags.4?int | flags.4 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| creator | 0 | Controlled by `flags`; present when this bit is set. |
| default | 1 | Controlled by `flags`; present when this bit is set. |
| for_chat | 5 | Controlled by `flags`; present when this bit is set. |
| document | 2 | Controlled by `flags`; present when this bit is set. |
| settings | 3 | Controlled by `flags`; present when this bit is set. |
| emoticon | 6 | Controlled by `flags`; present when this bit is set. |
| installs_count | 4 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import Theme
```

Public access: `miniproto.raw.types.Theme`.

## Safe usage shape

```python
from miniproto.raw.types import Theme

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = Theme
```

## Result family

[`Theme`](/reference/telegram/types/results/theme/)

## Relationships

- Result family: [`Theme`](/reference/telegram/types/results/theme/)
- Accepted by: [`account.themes`](/reference/telegram/types/account/themes/), [`updateTheme`](/reference/telegram/types/base/update-theme/)
- Returned by: [`account.createTheme`](/reference/telegram/functions/account/create-theme/), [`account.getTheme`](/reference/telegram/functions/account/get-theme/), [`account.updateTheme`](/reference/telegram/functions/account/update-theme/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
