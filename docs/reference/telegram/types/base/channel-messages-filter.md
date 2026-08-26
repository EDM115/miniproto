---
title: "channelMessagesFilter"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "channelMessagesFilter"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xcd77d957"
---

# `channelMessagesFilter`

No description provided by the pinned schema.

## Signature

```tl
channelMessagesFilter#cd77d957 flags:# exclude_new_messages:flags.1?true ranges:Vector<MessageRange> = ChannelMessagesFilter;
```

## Result type

`ChannelMessagesFilter`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| exclude_new_messages | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| ranges | Vector<MessageRange> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| exclude_new_messages | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import ChannelMessagesFilter
```

Public access: `miniproto.raw.types.ChannelMessagesFilter`.

## Safe usage shape

```python
from miniproto.raw.types import ChannelMessagesFilter

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChannelMessagesFilter
```

## Result family

[`ChannelMessagesFilter`](/reference/telegram/types/results/channel-messages-filter/)

## Relationships

- Result family: [`ChannelMessagesFilter`](/reference/telegram/types/results/channel-messages-filter/)
- Related constructors: [`channelMessagesFilterEmpty`](/reference/telegram/types/base/channel-messages-filter-empty/)
- Accepted by: [`updates.getChannelDifference`](/reference/telegram/functions/updates/get-channel-difference/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
