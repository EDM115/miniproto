---
title: "help.appUpdate"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.appUpdate"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
schema_source: "tdlib"
constructor_id: "0xccbbce30"
---

# `help.appUpdate`

No description provided by the pinned schema.

## Signature

```tl
help.appUpdate#ccbbce30 flags:# can_not_skip:flags.0?true id:int version:string text:string entities:Vector<MessageEntity> document:flags.1?Document url:flags.2?string sticker:flags.3?Document = help.AppUpdate;
```

## Result type

`help.AppUpdate`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| can_not_skip | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| id | int | — | — | No description provided by the pinned schema. |
| version | string | — | — | No description provided by the pinned schema. |
| text | string | — | — | No description provided by the pinned schema. |
| entities | Vector<MessageEntity> | — | — | No description provided by the pinned schema. |
| document | flags.1?Document | flags.1 | — | No description provided by the pinned schema. |
| url | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| sticker | flags.3?Document | flags.3 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| can_not_skip | 0 | Controlled by `flags`; present when this bit is set. |
| document | 1 | Controlled by `flags`; present when this bit is set. |
| url | 2 | Controlled by `flags`; present when this bit is set. |
| sticker | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import HelpAppUpdate
```

Public access: `miniproto.raw.types.HelpAppUpdate`.

## Safe usage shape

```python
from miniproto.raw.types import HelpAppUpdate

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = HelpAppUpdate
```

## Result family

[`help.AppUpdate`](/reference/telegram/types/results/help-app-update/)

## Relationships

- Result family: [`help.AppUpdate`](/reference/telegram/types/results/help-app-update/)
- Related constructors: [`help.noAppUpdate`](/reference/telegram/types/help/no-app-update/)
- Returned by: [`help.getAppUpdate`](/reference/telegram/functions/help/get-app-update/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
