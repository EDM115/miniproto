---
title: "channels.adminLogResults"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "channels.adminLogResults"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "channels"
schema_source: "tdlib"
constructor_id: "0xed8af74d"
---

# `channels.adminLogResults`

No description provided by the pinned schema.

## Signature

```tl
channels.adminLogResults#ed8af74d events:Vector<ChannelAdminLogEvent> chats:Vector<Chat> users:Vector<User> = channels.AdminLogResults;
```

## Result type

`channels.AdminLogResults`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| events | Vector<ChannelAdminLogEvent> | — | — | No description provided by the pinned schema. |
| chats | Vector<Chat> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ChannelsAdminLogResults
```

Public access: `miniproto.raw.types.ChannelsAdminLogResults`.

## Safe usage shape

```python
from miniproto.raw.types import ChannelsAdminLogResults

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ChannelsAdminLogResults
```

## Result family

[`channels.AdminLogResults`](/reference/telegram/types/results/channels-admin-log-results/)

## Relationships

- Result family: [`channels.AdminLogResults`](/reference/telegram/types/results/channels-admin-log-results/)
- Returned by: [`channels.getAdminLog`](/reference/telegram/functions/channels/get-admin-log/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
