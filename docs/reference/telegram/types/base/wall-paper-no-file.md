---
title: "wallPaperNoFile"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "wallPaperNoFile"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xe0804116"
---

# `wallPaperNoFile`

No description provided by the pinned schema.

## Signature

```tl
wallPaperNoFile#e0804116 id:long flags:# default:flags.1?true dark:flags.4?true settings:flags.2?WallPaperSettings = WallPaper;
```

## Result type

`WallPaper`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | long | — | — | No description provided by the pinned schema. |
| flags | # | flag word | — | No description provided by the pinned schema. |
| default | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| dark | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| settings | flags.2?WallPaperSettings | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| default | 1 | Controlled by `flags`; present when this bit is set. |
| dark | 4 | Controlled by `flags`; present when this bit is set. |
| settings | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import WallPaperNoFile
```

Public access: `miniproto.raw.types.WallPaperNoFile`.

## Safe usage shape

```python
from miniproto.raw.types import WallPaperNoFile

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = WallPaperNoFile
```

## Result family

[`WallPaper`](/reference/telegram/types/results/wall-paper/)

## Relationships

- Result family: [`WallPaper`](/reference/telegram/types/results/wall-paper/)
- Related constructors: [`wallPaper`](/reference/telegram/types/base/wall-paper/)
- Accepted by: [`account.wallPapers`](/reference/telegram/types/account/wall-papers/), [`channelAdminLogEventActionChangeWallpaper`](/reference/telegram/types/base/channel-admin-log-event-action-change-wallpaper/), [`channelFull`](/reference/telegram/types/base/channel-full/), [`messageActionSetChatWallPaper`](/reference/telegram/types/base/message-action-set-chat-wall-paper/), [`themeSettings`](/reference/telegram/types/base/theme-settings/), [`updatePeerWallpaper`](/reference/telegram/types/base/update-peer-wallpaper/), [`userFull`](/reference/telegram/types/base/user-full/)
- Returned by: [`account.getMultiWallPapers`](/reference/telegram/functions/account/get-multi-wall-papers/), [`account.getWallPaper`](/reference/telegram/functions/account/get-wall-paper/), [`account.uploadWallPaper`](/reference/telegram/functions/account/upload-wall-paper/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
