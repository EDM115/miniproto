---
title: "users.usersSlice"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "users.usersSlice"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "users"
schema_source: "tdlib"
constructor_id: "0x315a4974"
---

# `users.usersSlice`

No description provided by the pinned schema.

## Signature

```tl
users.usersSlice#315a4974 count:int users:Vector<User> = users.Users;
```

## Result type

`users.Users`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| count | int | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import UsersUsersSlice
```

Public access: `miniproto.raw.types.UsersUsersSlice`.

## Class reference

```python
from miniproto.raw.types import UsersUsersSlice

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = UsersUsersSlice
```

## Result family

[`users.Users`](/reference/telegram/types/results/users-users/)

## Relationships

- Result family: [`users.Users`](/reference/telegram/types/results/users-users/)
- Related constructors: [`users.users`](/reference/telegram/types/users/users/)
- Returned by: [`bots.getBotRecommendations`](/reference/telegram/functions/bots/get-bot-recommendations/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
