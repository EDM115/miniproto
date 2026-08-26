---
title: "inputWallPaper"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputWallPaper"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xe630b979"
---

# `inputWallPaper`

No description provided by the pinned schema.

## Signature

```tl
inputWallPaper#e630b979 id:long access_hash:long = InputWallPaper;
```

## Result type

`InputWallPaper`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputWallPaper
```

Public access: `miniproto.raw.types.InputWallPaper`.

## Safe usage shape

```python
from miniproto.raw.types import InputWallPaper

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputWallPaper
```

## Result family

[`InputWallPaper`](/reference/telegram/types/results/input-wall-paper/)

## Relationships

- Result family: [`InputWallPaper`](/reference/telegram/types/results/input-wall-paper/)
- Related constructors: [`inputWallPaperNoFile`](/reference/telegram/types/base/input-wall-paper-no-file/), [`inputWallPaperSlug`](/reference/telegram/types/base/input-wall-paper-slug/)
- Accepted by: [`account.getMultiWallPapers`](/reference/telegram/functions/account/get-multi-wall-papers/), [`account.getWallPaper`](/reference/telegram/functions/account/get-wall-paper/), [`account.installWallPaper`](/reference/telegram/functions/account/install-wall-paper/), [`account.saveWallPaper`](/reference/telegram/functions/account/save-wall-paper/), [`messages.setChatWallPaper`](/reference/telegram/functions/messages/set-chat-wall-paper/), [`inputThemeSettings`](/reference/telegram/types/base/input-theme-settings/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
