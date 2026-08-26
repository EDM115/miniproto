---
title: "phone.groupCallStreamChannels"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "phone.groupCallStreamChannels"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "phone"
schema_source: "tdlib"
constructor_id: "0xd0e482b2"
---

# `phone.groupCallStreamChannels`

No description provided by the pinned schema.

## Signature

```tl
phone.groupCallStreamChannels#d0e482b2 channels:Vector<GroupCallStreamChannel> = phone.GroupCallStreamChannels;
```

## Result type

`phone.GroupCallStreamChannels`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| channels | Vector<GroupCallStreamChannel> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PhoneGroupCallStreamChannels
```

Public access: `miniproto.raw.types.PhoneGroupCallStreamChannels`.

## Safe usage shape

```python
from miniproto.raw.types import PhoneGroupCallStreamChannels

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PhoneGroupCallStreamChannels
```

## Result family

[`phone.GroupCallStreamChannels`](/reference/telegram/types/results/phone-group-call-stream-channels/)

## Relationships

- Result family: [`phone.GroupCallStreamChannels`](/reference/telegram/types/results/phone-group-call-stream-channels/)
- Returned by: [`phone.getGroupCallStreamChannels`](/reference/telegram/functions/phone/get-group-call-stream-channels/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
