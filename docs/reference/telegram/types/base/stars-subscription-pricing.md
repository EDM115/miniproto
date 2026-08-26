---
title: "starsSubscriptionPricing"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starsSubscriptionPricing"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x05416d58"
---

# `starsSubscriptionPricing`

No description provided by the pinned schema.

## Signature

```tl
starsSubscriptionPricing#05416d58 period:int amount:long = StarsSubscriptionPricing;
```

## Result type

`StarsSubscriptionPricing`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| period | int | — | — | No description provided by the pinned schema. |
| amount | long | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import StarsSubscriptionPricing
```

Public access: `miniproto.raw.types.StarsSubscriptionPricing`.

## Safe usage shape

```python
from miniproto.raw.types import StarsSubscriptionPricing

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarsSubscriptionPricing
```

## Result family

[`StarsSubscriptionPricing`](/reference/telegram/types/results/stars-subscription-pricing/)

## Relationships

- Result family: [`StarsSubscriptionPricing`](/reference/telegram/types/results/stars-subscription-pricing/)
- Accepted by: [`messages.exportChatInvite`](/reference/telegram/functions/messages/export-chat-invite/), [`chatInvite`](/reference/telegram/types/base/chat-invite/), [`chatInviteExported`](/reference/telegram/types/base/chat-invite-exported/), [`starsSubscription`](/reference/telegram/types/base/stars-subscription/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
