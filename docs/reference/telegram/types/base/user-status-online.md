---
title: "userStatusOnline"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "userStatusOnline"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xedb93949"
---

# `userStatusOnline`

No description provided by the pinned schema.

## Signature

```tl
userStatusOnline#edb93949 expires:int = UserStatus;
```

## Result type

`UserStatus`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| expires | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import UserStatusOnline
```

Public access: `miniproto.raw.types.UserStatusOnline`.

## Safe usage shape

```python
from miniproto.raw.types import UserStatusOnline

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UserStatusOnline
```

## Result family

[`UserStatus`](/reference/telegram/types/results/user-status/)

## Relationships

- Result family: [`UserStatus`](/reference/telegram/types/results/user-status/)
- Related constructors: [`userStatusEmpty`](/reference/telegram/types/base/user-status-empty/), [`userStatusLastMonth`](/reference/telegram/types/base/user-status-last-month/), [`userStatusLastWeek`](/reference/telegram/types/base/user-status-last-week/), [`userStatusOffline`](/reference/telegram/types/base/user-status-offline/), [`userStatusRecently`](/reference/telegram/types/base/user-status-recently/)
- Accepted by: [`contactStatus`](/reference/telegram/types/base/contact-status/), [`updateUserStatus`](/reference/telegram/types/base/update-user-status/), [`user`](/reference/telegram/types/base/user/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
