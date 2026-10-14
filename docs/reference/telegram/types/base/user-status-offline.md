---
title: "userStatusOffline"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "userStatusOffline"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x008c703f"
---

# `userStatusOffline`

No description provided by the pinned schema.

## Signature

```tl
userStatusOffline#008c703f was_online:int = UserStatus;
```

## Result type

`UserStatus`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| was_online | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import UserStatusOffline
```

Public access: `miniproto.raw.types.UserStatusOffline`.

## Class reference

```python
from miniproto.raw.types import UserStatusOffline

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = UserStatusOffline
```

## Result family

[`UserStatus`](/reference/telegram/types/results/user-status/)

## Relationships

- Result family: [`UserStatus`](/reference/telegram/types/results/user-status/)
- Related constructors: [`userStatusEmpty`](/reference/telegram/types/base/user-status-empty/), [`userStatusLastMonth`](/reference/telegram/types/base/user-status-last-month/), [`userStatusLastWeek`](/reference/telegram/types/base/user-status-last-week/), [`userStatusOnline`](/reference/telegram/types/base/user-status-online/), [`userStatusRecently`](/reference/telegram/types/base/user-status-recently/)
- Accepted by: [`contactStatus`](/reference/telegram/types/base/contact-status/), [`updateUserStatus`](/reference/telegram/types/base/update-user-status/), [`user`](/reference/telegram/types/base/user/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
