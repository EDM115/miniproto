---
title: "inputTheme"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputTheme"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x3c5693e9"
---

# `inputTheme`

No description provided by the pinned schema.

## Signature

```tl
inputTheme#3c5693e9 id:long access_hash:long = InputTheme;
```

## Result type

`InputTheme`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | long | — | — | No description provided by the pinned schema. |
| access_hash | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputTheme
```

Public access: `miniproto.raw.types.InputTheme`.

## Safe usage shape

```python
from miniproto.raw.types import InputTheme

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputTheme
```

## Result family

[`InputTheme`](/reference/telegram/types/results/input-theme/)

## Relationships

- Result family: [`InputTheme`](/reference/telegram/types/results/input-theme/)
- Related constructors: [`inputThemeSlug`](/reference/telegram/types/base/input-theme-slug/)
- Accepted by: [`account.getTheme`](/reference/telegram/functions/account/get-theme/), [`account.installTheme`](/reference/telegram/functions/account/install-theme/), [`account.saveTheme`](/reference/telegram/functions/account/save-theme/), [`account.updateTheme`](/reference/telegram/functions/account/update-theme/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
