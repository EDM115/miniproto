---
title: "receivedNotifyMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "receivedNotifyMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xa384b779"
---

# `receivedNotifyMessage`

No description provided by the pinned schema.

## Signature

```tl
receivedNotifyMessage#a384b779 id:int flags:int = ReceivedNotifyMessage;
```

## Result type

`ReceivedNotifyMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| id | int | — | — | No description provided by the pinned schema. |
| flags | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ReceivedNotifyMessage
```

Public access: `miniproto.raw.types.ReceivedNotifyMessage`.

## Safe usage shape

```python
from miniproto.raw.types import ReceivedNotifyMessage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = ReceivedNotifyMessage
```

## Result family

[`ReceivedNotifyMessage`](/reference/telegram/types/results/received-notify-message/)

## Relationships

- Result family: [`ReceivedNotifyMessage`](/reference/telegram/types/results/received-notify-message/)
- Returned by: [`messages.receivedMessages`](/reference/telegram/functions/messages/received-messages/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
