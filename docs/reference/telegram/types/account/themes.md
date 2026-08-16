---
title: "account.themes"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.themes"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0x9a3d8c6d"
---

# `account.themes`

No description provided by the pinned schema.

## Signature

```tl
account.themes#9a3d8c6d hash:long themes:Vector<Theme> = account.Themes;
```

## Result type

`account.Themes`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | long | — | — | No description provided by the pinned schema. |
| themes | Vector<Theme> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AccountThemes
```

Public access: `miniproto.raw.types.AccountThemes`.

## Safe usage shape

```python
from miniproto.raw.types import AccountThemes

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountThemes
```

## Result family

[`account.Themes`](/reference/telegram/types/results/account-themes/)

## Relationships

- Result family: [`account.Themes`](/reference/telegram/types/results/account-themes/)
- Related constructors: [`account.themesNotModified`](/reference/telegram/types/account/themes-not-modified/)
- Returned by: [`account.getChatThemes`](/reference/telegram/functions/account/get-chat-themes/), [`account.getThemes`](/reference/telegram/functions/account/get-themes/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
