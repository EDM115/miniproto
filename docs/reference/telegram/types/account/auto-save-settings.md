---
title: "account.autoSaveSettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.autoSaveSettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0x4c3e069d"
---

# `account.autoSaveSettings`

No description provided by the pinned schema.

## Signature

```tl
account.autoSaveSettings#4c3e069d users_settings:AutoSaveSettings chats_settings:AutoSaveSettings broadcasts_settings:AutoSaveSettings exceptions:Vector<AutoSaveException> chats:Vector<Chat> users:Vector<User> = account.AutoSaveSettings;
```

## Result type

`account.AutoSaveSettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| users_settings | AutoSaveSettings | — | — | No description provided by the pinned schema. |
| chats_settings | AutoSaveSettings | — | — | No description provided by the pinned schema. |
| broadcasts_settings | AutoSaveSettings | — | — | No description provided by the pinned schema. |
| exceptions | Vector<AutoSaveException> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AccountAutoSaveSettings
```

Public access: `miniproto.raw.types.AccountAutoSaveSettings`.

## Safe usage shape

```python
from miniproto.raw.types import AccountAutoSaveSettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountAutoSaveSettings
```

## Result family

[`account.AutoSaveSettings`](/reference/telegram/types/results/account-auto-save-settings/)

## Relationships

- Result family: [`account.AutoSaveSettings`](/reference/telegram/types/results/account-auto-save-settings/)
- Returned by: [`account.getAutoSaveSettings`](/reference/telegram/functions/account/get-auto-save-settings/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
