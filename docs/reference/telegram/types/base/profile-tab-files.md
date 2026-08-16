---
title: "profileTabFiles"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "profileTabFiles"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xab339c00"
---

# `profileTabFiles`

No description provided by the pinned schema.

## Signature

```tl
profileTabFiles#ab339c00 = ProfileTab;
```

## Result type

`ProfileTab`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import ProfileTabFiles
```

Public access: `miniproto.raw.types.ProfileTabFiles`.

## Safe usage shape

```python
from miniproto.raw.types import ProfileTabFiles

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ProfileTabFiles
```

## Result family

[`ProfileTab`](/reference/telegram/types/results/profile-tab/)

## Relationships

- Result family: [`ProfileTab`](/reference/telegram/types/results/profile-tab/)
- Related constructors: [`profileTabGifs`](/reference/telegram/types/base/profile-tab-gifs/), [`profileTabGifts`](/reference/telegram/types/base/profile-tab-gifts/), [`profileTabLinks`](/reference/telegram/types/base/profile-tab-links/), [`profileTabMedia`](/reference/telegram/types/base/profile-tab-media/), [`profileTabMusic`](/reference/telegram/types/base/profile-tab-music/), [`profileTabPosts`](/reference/telegram/types/base/profile-tab-posts/), [`profileTabVoice`](/reference/telegram/types/base/profile-tab-voice/)
- Accepted by: [`account.setMainProfileTab`](/reference/telegram/functions/account/set-main-profile-tab/), [`channels.setMainProfileTab`](/reference/telegram/functions/channels/set-main-profile-tab/), [`channelFull`](/reference/telegram/types/base/channel-full/), [`userFull`](/reference/telegram/types/base/user-full/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
