---
title: "suggestedPost"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "suggestedPost"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x0e8e37e5"
---

# `suggestedPost`

No description provided by the pinned schema.

## Signature

```tl
suggestedPost#0e8e37e5 flags:# accepted:flags.1?true rejected:flags.2?true price:flags.3?StarsAmount schedule_date:flags.0?int = SuggestedPost;
```

## Result type

`SuggestedPost`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| accepted | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| rejected | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| price | flags.3?StarsAmount | flags.3 | — | No description provided by the pinned schema. |
| schedule_date | flags.0?int | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| accepted | 1 | Controlled by `flags`; present when this bit is set. |
| rejected | 2 | Controlled by `flags`; present when this bit is set. |
| price | 3 | Controlled by `flags`; present when this bit is set. |
| schedule_date | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import SuggestedPost
```

Public access: `miniproto.raw.types.SuggestedPost`.

## Safe usage shape

```python
from miniproto.raw.types import SuggestedPost

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = SuggestedPost
```

## Result family

[`SuggestedPost`](/reference/telegram/types/results/suggested-post/)

## Relationships

- Result family: [`SuggestedPost`](/reference/telegram/types/results/suggested-post/)
- Accepted by: [`messages.forwardMessages`](/reference/telegram/functions/messages/forward-messages/), [`messages.saveDraft`](/reference/telegram/functions/messages/save-draft/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`draftMessage`](/reference/telegram/types/base/draft-message/), [`message`](/reference/telegram/types/base/message/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
