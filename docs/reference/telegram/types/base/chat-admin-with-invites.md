---
title: "chatAdminWithInvites"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "chatAdminWithInvites"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xf2ecef23"
---

# `chatAdminWithInvites`

No description provided by the pinned schema.

## Signature

```tl
chatAdminWithInvites#f2ecef23 admin_id:long invites_count:int revoked_invites_count:int = ChatAdminWithInvites;
```

## Result type

`ChatAdminWithInvites`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| admin_id | long | — | — | No description provided by the pinned schema. |
| invites_count | int | — | — | No description provided by the pinned schema. |
| revoked_invites_count | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ChatAdminWithInvites
```

Public access: `miniproto.raw.types.ChatAdminWithInvites`.

## Safe usage shape

```python
from miniproto.raw.types import ChatAdminWithInvites

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChatAdminWithInvites
```

## Result family

[`ChatAdminWithInvites`](/reference/telegram/types/results/chat-admin-with-invites/)

## Relationships

- Result family: [`ChatAdminWithInvites`](/reference/telegram/types/results/chat-admin-with-invites/)
- Accepted by: [`messages.chatAdminsWithInvites`](/reference/telegram/types/messages/chat-admins-with-invites/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
