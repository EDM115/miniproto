---
title: "wallPaperSettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "wallPaperSettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x372efcd0"
---

# `wallPaperSettings`

No description provided by the pinned schema.

## Signature

```tl
wallPaperSettings#372efcd0 flags:# blur:flags.1?true motion:flags.2?true background_color:flags.0?int second_background_color:flags.4?int third_background_color:flags.5?int fourth_background_color:flags.6?int intensity:flags.3?int rotation:flags.4?int emoticon:flags.7?string = WallPaperSettings;
```

## Result type

`WallPaperSettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| blur | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| motion | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| background_color | flags.0?int | flags.0 | — | No description provided by the pinned schema. |
| second_background_color | flags.4?int | flags.4 | — | No description provided by the pinned schema. |
| third_background_color | flags.5?int | flags.5 | — | No description provided by the pinned schema. |
| fourth_background_color | flags.6?int | flags.6 | — | No description provided by the pinned schema. |
| intensity | flags.3?int | flags.3 | — | No description provided by the pinned schema. |
| rotation | flags.4?int | flags.4 | — | No description provided by the pinned schema. |
| emoticon | flags.7?string | flags.7 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| blur | 1 | Controlled by `flags`; present when this bit is set. |
| motion | 2 | Controlled by `flags`; present when this bit is set. |
| background_color | 0 | Controlled by `flags`; present when this bit is set. |
| second_background_color | 4 | Controlled by `flags`; present when this bit is set. |
| third_background_color | 5 | Controlled by `flags`; present when this bit is set. |
| fourth_background_color | 6 | Controlled by `flags`; present when this bit is set. |
| intensity | 3 | Controlled by `flags`; present when this bit is set. |
| rotation | 4 | Controlled by `flags`; present when this bit is set. |
| emoticon | 7 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import WallPaperSettings
```

Public access: `miniproto.raw.types.WallPaperSettings`.

## Safe usage shape

```python
from miniproto.raw.types import WallPaperSettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = WallPaperSettings
```

## Result family

[`WallPaperSettings`](/reference/telegram/types/results/wall-paper-settings/)

## Relationships

- Result family: [`WallPaperSettings`](/reference/telegram/types/results/wall-paper-settings/)
- Accepted by: [`account.installWallPaper`](/reference/telegram/functions/account/install-wall-paper/), [`account.saveWallPaper`](/reference/telegram/functions/account/save-wall-paper/), [`account.uploadWallPaper`](/reference/telegram/functions/account/upload-wall-paper/), [`messages.setChatWallPaper`](/reference/telegram/functions/messages/set-chat-wall-paper/), [`inputThemeSettings`](/reference/telegram/types/base/input-theme-settings/), [`wallPaper`](/reference/telegram/types/base/wall-paper/), [`wallPaperNoFile`](/reference/telegram/types/base/wall-paper-no-file/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
