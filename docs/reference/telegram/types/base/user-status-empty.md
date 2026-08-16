---
title: "userStatusEmpty"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "userStatusEmpty"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x09d05049"
---

# `userStatusEmpty`

No description provided by the pinned schema.

## Signature

```tl
userStatusEmpty#09d05049 = UserStatus;
```

## Result type

`UserStatus`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import UserStatusEmpty
```

Public access: `miniproto.raw.types.UserStatusEmpty`.

## Safe usage shape

```python
from miniproto.raw.types import UserStatusEmpty

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UserStatusEmpty
```

## Result family

[`UserStatus`](/reference/telegram/types/results/user-status/)

## Relationships

- Result family: [`UserStatus`](/reference/telegram/types/results/user-status/)
- Related constructors: [`userStatusLastMonth`](/reference/telegram/types/base/user-status-last-month/), [`userStatusLastWeek`](/reference/telegram/types/base/user-status-last-week/), [`userStatusOffline`](/reference/telegram/types/base/user-status-offline/), [`userStatusOnline`](/reference/telegram/types/base/user-status-online/), [`userStatusRecently`](/reference/telegram/types/base/user-status-recently/)
- Accepted by: [`contactStatus`](/reference/telegram/types/base/contact-status/), [`updateUserStatus`](/reference/telegram/types/base/update-user-status/), [`user`](/reference/telegram/types/base/user/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
