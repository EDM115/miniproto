---
title: "reactionsNotifySettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "reactionsNotifySettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x71e4ea58"
---

# `reactionsNotifySettings`

No description provided by the pinned schema.

## Signature

```tl
reactionsNotifySettings#71e4ea58 flags:# messages_notify_from:flags.0?ReactionNotificationsFrom stories_notify_from:flags.1?ReactionNotificationsFrom poll_votes_notify_from:flags.2?ReactionNotificationsFrom sound:NotificationSound show_previews:Bool = ReactionsNotifySettings;
```

## Result type

`ReactionsNotifySettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| messages_notify_from | flags.0?ReactionNotificationsFrom | flags.0 | — | No description provided by the pinned schema. |
| stories_notify_from | flags.1?ReactionNotificationsFrom | flags.1 | — | No description provided by the pinned schema. |
| poll_votes_notify_from | flags.2?ReactionNotificationsFrom | flags.2 | — | No description provided by the pinned schema. |
| sound | NotificationSound | — | — | No description provided by the pinned schema. |
| show_previews | Bool | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| messages_notify_from | 0 | Controlled by `flags`; present when this bit is set. |
| stories_notify_from | 1 | Controlled by `flags`; present when this bit is set. |
| poll_votes_notify_from | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ReactionsNotifySettings
```

Public access: `miniproto.raw.types.ReactionsNotifySettings`.

## Safe usage shape

```python
from miniproto.raw.types import ReactionsNotifySettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ReactionsNotifySettings
```

## Result family

[`ReactionsNotifySettings`](/reference/telegram/types/results/reactions-notify-settings/)

## Relationships

- Result family: [`ReactionsNotifySettings`](/reference/telegram/types/results/reactions-notify-settings/)
- Accepted by: [`account.setReactionsNotifySettings`](/reference/telegram/functions/account/set-reactions-notify-settings/)
- Returned by: [`account.getReactionsNotifySettings`](/reference/telegram/functions/account/get-reactions-notify-settings/), [`account.setReactionsNotifySettings`](/reference/telegram/functions/account/set-reactions-notify-settings/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
