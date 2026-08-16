---
title: "requestPeerTypeBroadcast"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "requestPeerTypeBroadcast"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x339bef6c"
---

# `requestPeerTypeBroadcast`

No description provided by the pinned schema.

## Signature

```tl
requestPeerTypeBroadcast#339bef6c flags:# creator:flags.0?true has_username:flags.3?Bool user_admin_rights:flags.1?ChatAdminRights bot_admin_rights:flags.2?ChatAdminRights = RequestPeerType;
```

## Result type

`RequestPeerType`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| creator | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| has_username | flags.3?Bool | flags.3 | — | No description provided by the pinned schema. |
| user_admin_rights | flags.1?ChatAdminRights | flags.1 | — | No description provided by the pinned schema. |
| bot_admin_rights | flags.2?ChatAdminRights | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| creator | 0 | Controlled by `flags`; present when this bit is set. |
| has_username | 3 | Controlled by `flags`; present when this bit is set. |
| user_admin_rights | 1 | Controlled by `flags`; present when this bit is set. |
| bot_admin_rights | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import RequestPeerTypeBroadcast
```

Public access: `miniproto.raw.types.RequestPeerTypeBroadcast`.

## Safe usage shape

```python
from miniproto.raw.types import RequestPeerTypeBroadcast

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = RequestPeerTypeBroadcast
```

## Result family

[`RequestPeerType`](/reference/telegram/types/results/request-peer-type/)

## Relationships

- Result family: [`RequestPeerType`](/reference/telegram/types/results/request-peer-type/)
- Related constructors: [`requestPeerTypeChat`](/reference/telegram/types/base/request-peer-type-chat/), [`requestPeerTypeCreateBot`](/reference/telegram/types/base/request-peer-type-create-bot/), [`requestPeerTypeUser`](/reference/telegram/types/base/request-peer-type-user/)
- Accepted by: [`inputKeyboardButtonRequestPeer`](/reference/telegram/types/base/input-keyboard-button-request-peer/), [`keyboardButtonRequestPeer`](/reference/telegram/types/base/keyboard-button-request-peer/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
