---
title: "account.connectedBots"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.connectedBots"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0x17d7f87b"
---

# `account.connectedBots`

No description provided by the pinned schema.

## Signature

```tl
account.connectedBots#17d7f87b connected_bots:Vector<ConnectedBot> users:Vector<User> = account.ConnectedBots;
```

## Result type

`account.ConnectedBots`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| connected_bots | Vector<ConnectedBot> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AccountConnectedBots
```

Public access: `miniproto.raw.types.AccountConnectedBots`.

## Safe usage shape

```python
from miniproto.raw.types import AccountConnectedBots

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountConnectedBots
```

## Result family

[`account.ConnectedBots`](/reference/telegram/types/results/account-connected-bots/)

## Relationships

- Result family: [`account.ConnectedBots`](/reference/telegram/types/results/account-connected-bots/)
- Returned by: [`account.getConnectedBots`](/reference/telegram/functions/account/get-connected-bots/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
