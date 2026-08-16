---
title: "channelMessagesFilterEmpty"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "channelMessagesFilterEmpty"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x94d42ee7"
---

# `channelMessagesFilterEmpty`

No description provided by the pinned schema.

## Signature

```tl
channelMessagesFilterEmpty#94d42ee7 = ChannelMessagesFilter;
```

## Result type

`ChannelMessagesFilter`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import ChannelMessagesFilterEmpty
```

Public access: `miniproto.raw.types.ChannelMessagesFilterEmpty`.

## Safe usage shape

```python
from miniproto.raw.types import ChannelMessagesFilterEmpty

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChannelMessagesFilterEmpty
```

## Result family

[`ChannelMessagesFilter`](/reference/telegram/types/results/channel-messages-filter/)

## Relationships

- Result family: [`ChannelMessagesFilter`](/reference/telegram/types/results/channel-messages-filter/)
- Related constructors: [`channelMessagesFilter`](/reference/telegram/types/base/channel-messages-filter/)
- Accepted by: [`updates.getChannelDifference`](/reference/telegram/functions/updates/get-channel-difference/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
