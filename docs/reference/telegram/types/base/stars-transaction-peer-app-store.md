---
title: "starsTransactionPeerAppStore"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "starsTransactionPeerAppStore"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xb457b375"
---

# `starsTransactionPeerAppStore`

No description provided by the pinned schema.

## Signature

```tl
starsTransactionPeerAppStore#b457b375 = StarsTransactionPeer;
```

## Result type

`StarsTransactionPeer`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import StarsTransactionPeerAppStore
```

Public access: `miniproto.raw.types.StarsTransactionPeerAppStore`.

## Safe usage shape

```python
from miniproto.raw.types import StarsTransactionPeerAppStore

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = StarsTransactionPeerAppStore
```

## Result family

[`StarsTransactionPeer`](/reference/telegram/types/results/stars-transaction-peer/)

## Relationships

- Result family: [`StarsTransactionPeer`](/reference/telegram/types/results/stars-transaction-peer/)
- Related constructors: [`starsTransactionPeer`](/reference/telegram/types/base/stars-transaction-peer/), [`starsTransactionPeerAPI`](/reference/telegram/types/base/stars-transaction-peer-api/), [`starsTransactionPeerAds`](/reference/telegram/types/base/stars-transaction-peer-ads/), [`starsTransactionPeerFragment`](/reference/telegram/types/base/stars-transaction-peer-fragment/), [`starsTransactionPeerPlayMarket`](/reference/telegram/types/base/stars-transaction-peer-play-market/), [`starsTransactionPeerPremiumBot`](/reference/telegram/types/base/stars-transaction-peer-premium-bot/), [`starsTransactionPeerUnsupported`](/reference/telegram/types/base/stars-transaction-peer-unsupported/)
- Accepted by: [`starsTransaction`](/reference/telegram/types/base/stars-transaction/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
