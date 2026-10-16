---
title: "inputWallPaperSlug"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputWallPaperSlug"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x72091c80"
---

# `inputWallPaperSlug`

No description provided by the pinned schema.

## Signature

```tl
inputWallPaperSlug#72091c80 slug:string = InputWallPaper;
```

## Result type

`InputWallPaper`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| slug | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputWallPaperSlug
```

Public access: `miniproto.raw.types.InputWallPaperSlug`.

## Class reference

```python
from miniproto.raw.types import InputWallPaperSlug

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = InputWallPaperSlug
```

## Result family

[`InputWallPaper`](/reference/telegram/types/results/input-wall-paper/)

## Relationships

- Result family: [`InputWallPaper`](/reference/telegram/types/results/input-wall-paper/)
- Related constructors: [`inputWallPaper`](/reference/telegram/types/base/input-wall-paper/), [`inputWallPaperNoFile`](/reference/telegram/types/base/input-wall-paper-no-file/)
- Accepted by: [`account.getMultiWallPapers`](/reference/telegram/functions/account/get-multi-wall-papers/), [`account.getWallPaper`](/reference/telegram/functions/account/get-wall-paper/), [`account.installWallPaper`](/reference/telegram/functions/account/install-wall-paper/), [`account.saveWallPaper`](/reference/telegram/functions/account/save-wall-paper/), [`messages.setChatWallPaper`](/reference/telegram/functions/messages/set-chat-wall-paper/), [`inputThemeSettings`](/reference/telegram/types/base/input-theme-settings/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
