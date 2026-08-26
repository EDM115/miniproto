---
title: "account.chatThemesNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.chatThemesNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0xe011e1c4"
---

# `account.chatThemesNotModified`

No description provided by the pinned schema.

## Signature

```tl
account.chatThemesNotModified#e011e1c4 = account.ChatThemes;
```

## Result type

`account.ChatThemes`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import AccountChatThemesNotModified
```

Public access: `miniproto.raw.types.AccountChatThemesNotModified`.

## Safe usage shape

```python
from miniproto.raw.types import AccountChatThemesNotModified

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountChatThemesNotModified
```

## Result family

[`account.ChatThemes`](/reference/telegram/types/results/account-chat-themes/)

## Relationships

- Result family: [`account.ChatThemes`](/reference/telegram/types/results/account-chat-themes/)
- Related constructors: [`account.chatThemes`](/reference/telegram/types/account/chat-themes/)
- Returned by: [`account.getUniqueGiftChatThemes`](/reference/telegram/functions/account/get-unique-gift-chat-themes/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
