---
title: "channelAdminLogEvent"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "channelAdminLogEvent"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x1fad68cd"
---

# `channelAdminLogEvent`

No description provided by the pinned schema.

## Signature

```tl
channelAdminLogEvent#1fad68cd id:long date:int user_id:long action:ChannelAdminLogEventAction = ChannelAdminLogEvent;
```

## Result type

`ChannelAdminLogEvent`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | long | — | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| user_id | long | — | — | No description provided by the pinned schema. |
| action | ChannelAdminLogEventAction | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ChannelAdminLogEvent
```

Public access: `miniproto.raw.types.ChannelAdminLogEvent`.

## Class reference

```python
from miniproto.raw.types import ChannelAdminLogEvent

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = ChannelAdminLogEvent
```

## Result family

[`ChannelAdminLogEvent`](/reference/telegram/types/results/channel-admin-log-event/)

## Relationships

- Result family: [`ChannelAdminLogEvent`](/reference/telegram/types/results/channel-admin-log-event/)
- Accepted by: [`channels.adminLogResults`](/reference/telegram/types/channels/admin-log-results/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
