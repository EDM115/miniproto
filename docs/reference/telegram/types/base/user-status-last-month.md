---
title: "userStatusLastMonth"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "userStatusLastMonth"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x65899777"
---

# `userStatusLastMonth`

No description provided by the pinned schema.

## Signature

```tl
userStatusLastMonth#65899777 flags:# by_me:flags.0?true = UserStatus;
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
from miniproto.raw.types import UserStatusLastMonth
```

Public access: `miniproto.raw.types.UserStatusLastMonth`.

## Safe usage shape

```python
from miniproto.raw.types import UserStatusLastMonth

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UserStatusLastMonth
```

## Result family

[`UserStatus`](/reference/telegram/types/results/user-status/)

## Relationships

- Result family: [`UserStatus`](/reference/telegram/types/results/user-status/)
- Related constructors: [`userStatusEmpty`](/reference/telegram/types/base/user-status-empty/), [`userStatusLastWeek`](/reference/telegram/types/base/user-status-last-week/), [`userStatusOffline`](/reference/telegram/types/base/user-status-offline/), [`userStatusOnline`](/reference/telegram/types/base/user-status-online/), [`userStatusRecently`](/reference/telegram/types/base/user-status-recently/)
- Accepted by: [`contactStatus`](/reference/telegram/types/base/contact-status/), [`updateUserStatus`](/reference/telegram/types/base/update-user-status/), [`user`](/reference/telegram/types/base/user/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
