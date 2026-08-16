---
title: "account.resolvedBusinessChatLinks"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.resolvedBusinessChatLinks"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0x9a23af21"
---

# `account.resolvedBusinessChatLinks`

No description provided by the pinned schema.

## Signature

```tl
account.resolvedBusinessChatLinks#9a23af21 flags:# peer:Peer message:string entities:flags.0?Vector<MessageEntity> chats:Vector<Chat> users:Vector<User> = account.ResolvedBusinessChatLinks;
```

## Result type

`account.ResolvedBusinessChatLinks`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| peer | Peer | — | — | No description provided by the pinned schema. |
| message | string | — | — | No description provided by the pinned schema. |
| entities | flags.0?Vector<MessageEntity> | flags.0 | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| entities | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import AccountResolvedBusinessChatLinks
```

Public access: `miniproto.raw.types.AccountResolvedBusinessChatLinks`.

## Safe usage shape

```python
from miniproto.raw.types import AccountResolvedBusinessChatLinks

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountResolvedBusinessChatLinks
```

## Result family

[`account.ResolvedBusinessChatLinks`](/reference/telegram/types/results/account-resolved-business-chat-links/)

## Relationships

- Result family: [`account.ResolvedBusinessChatLinks`](/reference/telegram/types/results/account-resolved-business-chat-links/)
- Returned by: [`account.resolveBusinessChatLink`](/reference/telegram/functions/account/resolve-business-chat-link/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
