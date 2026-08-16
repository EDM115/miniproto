---
title: "userStatusLastWeek"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "userStatusLastWeek"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x541a1d1a"
---

# `userStatusLastWeek`

No description provided by the pinned schema.

## Signature

```tl
userStatusLastWeek#541a1d1a flags:# by_me:flags.0?true = UserStatus;
```

## Result type

`UserStatus`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| by_me | flags.0?true | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| by_me | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import UserStatusLastWeek
```

Public access: `miniproto.raw.types.UserStatusLastWeek`.

## Safe usage shape

```python
from miniproto.raw.types import UserStatusLastWeek

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UserStatusLastWeek
```

## Result family

[`UserStatus`](/reference/telegram/types/results/user-status/)

## Relationships

- Result family: [`UserStatus`](/reference/telegram/types/results/user-status/)
- Related constructors: [`userStatusEmpty`](/reference/telegram/types/base/user-status-empty/), [`userStatusLastMonth`](/reference/telegram/types/base/user-status-last-month/), [`userStatusOffline`](/reference/telegram/types/base/user-status-offline/), [`userStatusOnline`](/reference/telegram/types/base/user-status-online/), [`userStatusRecently`](/reference/telegram/types/base/user-status-recently/)
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
