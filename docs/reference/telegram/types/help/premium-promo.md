---
title: "help.premiumPromo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.premiumPromo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
layer: 228
schema_source: "tdlib"
constructor_id: "0x5334759c"
---

# `help.premiumPromo`

No description provided by the pinned schema.

## Signature

```tl
help.premiumPromo#5334759c status_text:string status_entities:Vector<MessageEntity> video_sections:Vector<string> videos:Vector<Document> period_options:Vector<PremiumSubscriptionOption> users:Vector<User> = help.PremiumPromo;
```

## Result type

`help.PremiumPromo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| status_text | string | — | — | No description provided by the pinned schema. |
| status_entities | Vector<MessageEntity> | — | — | No description provided by the pinned schema. |
| video_sections | Vector<string> | — | — | No description provided by the pinned schema. |
| videos | Vector<Document> | — | — | No description provided by the pinned schema. |
| period_options | Vector<PremiumSubscriptionOption> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import HelpPremiumPromo
```

Public access: `miniproto.raw.types.HelpPremiumPromo`.

## Safe usage shape

```python
from miniproto.raw.types import HelpPremiumPromo

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = HelpPremiumPromo
```

## Result family

[`help.PremiumPromo`](/reference/telegram/types/results/help-premium-promo/)

## Relationships

- Result family: [`help.PremiumPromo`](/reference/telegram/types/results/help-premium-promo/)
- Returned by: [`help.getPremiumPromo`](/reference/telegram/functions/help/get-premium-promo/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
