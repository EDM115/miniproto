---
title: "fragment.collectibleInfo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "fragment.collectibleInfo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "fragment"
layer: 228
schema_source: "tdlib"
constructor_id: "0x6ebdff91"
---

# `fragment.collectibleInfo`

No description provided by the pinned schema.

## Signature

```tl
fragment.collectibleInfo#6ebdff91 purchase_date:int currency:string amount:long crypto_currency:string crypto_amount:long url:string = fragment.CollectibleInfo;
```

## Result type

`fragment.CollectibleInfo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| purchase_date | int | — | — | No description provided by the pinned schema. |
| currency | string | — | — | No description provided by the pinned schema. |
| amount | long | — | — | No description provided by the pinned schema. |
| crypto_currency | string | — | — | No description provided by the pinned schema. |
| crypto_amount | long | — | — | No description provided by the pinned schema. |
| url | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import FragmentCollectibleInfo
```

Public access: `miniproto.raw.types.FragmentCollectibleInfo`.

## Safe usage shape

```python
from miniproto.raw.types import FragmentCollectibleInfo

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = FragmentCollectibleInfo
```

## Result family

[`fragment.CollectibleInfo`](/reference/telegram/types/results/fragment-collectible-info/)

## Relationships

- Result family: [`fragment.CollectibleInfo`](/reference/telegram/types/results/fragment-collectible-info/)
- Returned by: [`fragment.getCollectibleInfo`](/reference/telegram/functions/fragment/get-collectible-info/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
