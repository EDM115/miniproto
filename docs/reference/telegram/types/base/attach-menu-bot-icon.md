---
title: "attachMenuBotIcon"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "attachMenuBotIcon"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xb2a7386b"
---

# `attachMenuBotIcon`

No description provided by the pinned schema.

## Signature

```tl
attachMenuBotIcon#b2a7386b flags:# name:string icon:Document colors:flags.0?Vector<AttachMenuBotIconColor> = AttachMenuBotIcon;
```

## Result type

`AttachMenuBotIcon`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| name | string | — | — | No description provided by the pinned schema. |
| icon | Document | — | — | No description provided by the pinned schema. |
| colors | flags.0?Vector<AttachMenuBotIconColor> | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| colors | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import AttachMenuBotIcon
```

Public access: `miniproto.raw.types.AttachMenuBotIcon`.

## Safe usage shape

```python
from miniproto.raw.types import AttachMenuBotIcon

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AttachMenuBotIcon
```

## Result family

[`AttachMenuBotIcon`](/reference/telegram/types/results/attach-menu-bot-icon/)

## Relationships

- Result family: [`AttachMenuBotIcon`](/reference/telegram/types/results/attach-menu-bot-icon/)
- Accepted by: [`attachMenuBot`](/reference/telegram/types/base/attach-menu-bot/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
