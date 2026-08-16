---
title: "chatInvite"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "chatInvite"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x5c9d3702"
---

# `chatInvite`

No description provided by the pinned schema.

## Signature

```tl
chatInvite#5c9d3702 flags:# channel:flags.0?true broadcast:flags.1?true public:flags.2?true megagroup:flags.3?true request_needed:flags.6?true verified:flags.7?true scam:flags.8?true fake:flags.9?true can_refulfill_subscription:flags.11?true title:string about:flags.5?string photo:Photo participants_count:int participants:flags.4?Vector<User> color:int subscription_pricing:flags.10?StarsSubscriptionPricing subscription_form_id:flags.12?long bot_verification:flags.13?BotVerification = ChatInvite;
```

## Result type

`ChatInvite`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| channel | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| broadcast | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| public | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| megagroup | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| request_needed | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| verified | flags.7?true | flags.7 | — | No description provided by the pinned schema. |
| scam | flags.8?true | flags.8 | — | No description provided by the pinned schema. |
| fake | flags.9?true | flags.9 | — | No description provided by the pinned schema. |
| can_refulfill_subscription | flags.11?true | flags.11 | — | No description provided by the pinned schema. |
| title | string | — | — | No description provided by the pinned schema. |
| about | flags.5?string | flags.5 | — | No description provided by the pinned schema. |
| photo | Photo | — | — | No description provided by the pinned schema. |
| participants_count | int | — | — | No description provided by the pinned schema. |
| participants | flags.4?Vector<User> | flags.4 | — | No description provided by the pinned schema. |
| color | int | — | — | No description provided by the pinned schema. |
| subscription_pricing | flags.10?StarsSubscriptionPricing | flags.10 | — | No description provided by the pinned schema. |
| subscription_form_id | flags.12?long | flags.12 | — | No description provided by the pinned schema. |
| bot_verification | flags.13?BotVerification | flags.13 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| channel | 0 | Controlled by `flags`; present when this bit is set. |
| broadcast | 1 | Controlled by `flags`; present when this bit is set. |
| public | 2 | Controlled by `flags`; present when this bit is set. |
| megagroup | 3 | Controlled by `flags`; present when this bit is set. |
| request_needed | 6 | Controlled by `flags`; present when this bit is set. |
| verified | 7 | Controlled by `flags`; present when this bit is set. |
| scam | 8 | Controlled by `flags`; present when this bit is set. |
| fake | 9 | Controlled by `flags`; present when this bit is set. |
| can_refulfill_subscription | 11 | Controlled by `flags`; present when this bit is set. |
| about | 5 | Controlled by `flags`; present when this bit is set. |
| participants | 4 | Controlled by `flags`; present when this bit is set. |
| subscription_pricing | 10 | Controlled by `flags`; present when this bit is set. |
| subscription_form_id | 12 | Controlled by `flags`; present when this bit is set. |
| bot_verification | 13 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ChatInvite
```

Public access: `miniproto.raw.types.ChatInvite`.

## Safe usage shape

```python
from miniproto.raw.types import ChatInvite

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChatInvite
```

## Result family

[`ChatInvite`](/reference/telegram/types/results/chat-invite/)

## Relationships

- Result family: [`ChatInvite`](/reference/telegram/types/results/chat-invite/)
- Related constructors: [`chatInviteAlready`](/reference/telegram/types/base/chat-invite-already/), [`chatInvitePeek`](/reference/telegram/types/base/chat-invite-peek/)
- Accepted by: [`recentMeUrlChatInvite`](/reference/telegram/types/base/recent-me-url-chat-invite/)
- Returned by: [`messages.checkChatInvite`](/reference/telegram/functions/messages/check-chat-invite/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
