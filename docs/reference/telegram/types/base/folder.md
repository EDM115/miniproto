---
title: "folder"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "folder"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xff544e65"
---

# `folder`

No description provided by the pinned schema.

## Signature

```tl
folder#ff544e65 flags:# autofill_new_broadcasts:flags.0?true autofill_public_groups:flags.1?true autofill_new_correspondents:flags.2?true id:int title:string photo:flags.3?ChatPhoto = Folder;
```

## Result type

`Folder`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| autofill_new_broadcasts | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| autofill_public_groups | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| autofill_new_correspondents | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| id | int | — | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| photo | flags.3?ChatPhoto | flags.3 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| autofill_new_broadcasts | 0 | Controlled by `flags`; present when this bit is set. |
| autofill_public_groups | 1 | Controlled by `flags`; present when this bit is set. |
| autofill_new_correspondents | 2 | Controlled by `flags`; present when this bit is set. |
| photo | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import Folder
```

Public access: `miniproto.raw.types.Folder`.

## Safe usage shape

```python
from miniproto.raw.types import Folder

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = Folder
```

## Result family

[`Folder`](/reference/telegram/types/results/folder/)

## Relationships

- Result family: [`Folder`](/reference/telegram/types/results/folder/)
- Accepted by: [`dialogFolder`](/reference/telegram/types/base/dialog-folder/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
