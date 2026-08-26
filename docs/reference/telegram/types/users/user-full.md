---
title: "users.userFull"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "users.userFull"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "users"
schema_source: "tdlib"
constructor_id: "0x3b6d152e"
---

# `users.userFull`

No description provided by the pinned schema.

## Signature

```tl
users.userFull#3b6d152e full_user:UserFull chats:Vector<Chat> users:Vector<User> = users.UserFull;
```

## Result type

`users.UserFull`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| full_user | UserFull | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import UsersUserFull
```

Public access: `miniproto.raw.types.UsersUserFull`.

## Safe usage shape

```python
from miniproto.raw.types import UsersUserFull

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UsersUserFull
```

## Result family

[`users.UserFull`](/reference/telegram/types/results/users-user-full/)

## Relationships

- Result family: [`users.UserFull`](/reference/telegram/types/results/users-user-full/)
- Returned by: [`users.getFullUser`](/reference/telegram/functions/users/get-full-user/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
