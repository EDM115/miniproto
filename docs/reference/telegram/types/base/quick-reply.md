---
title: "quickReply"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "quickReply"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x0697102b"
---

# `quickReply`

No description provided by the pinned schema.

## Signature

```tl
quickReply#0697102b shortcut_id:int shortcut:string top_message:int count:int = QuickReply;
```

## Result type

`QuickReply`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| shortcut_id | int | — | — | No description provided by the pinned schema. |
| shortcut | string | — | — | No description provided by the pinned schema. |
| top_message | int | — | — | No description provided by the pinned schema. |
| count | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import QuickReply
```

Public access: `miniproto.raw.types.QuickReply`.

## Safe usage shape

```python
from miniproto.raw.types import QuickReply

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = QuickReply
```

## Result family

[`QuickReply`](/reference/telegram/types/results/quick-reply/)

## Relationships

- Result family: [`QuickReply`](/reference/telegram/types/results/quick-reply/)
- Accepted by: [`messages.quickReplies`](/reference/telegram/types/messages/quick-replies/), [`updateNewQuickReply`](/reference/telegram/types/base/update-new-quick-reply/), [`updateQuickReplies`](/reference/telegram/types/base/update-quick-replies/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
