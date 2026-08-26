---
title: "messages.dhConfigNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.dhConfigNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0xc0e24635"
---

# `messages.dhConfigNotModified`

No description provided by the pinned schema.

## Signature

```tl
messages.dhConfigNotModified#c0e24635 random:bytes = messages.DhConfig;
```

## Result type

`messages.DhConfig`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| random | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesDhConfigNotModified
```

Public access: `miniproto.raw.types.MessagesDhConfigNotModified`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesDhConfigNotModified

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesDhConfigNotModified
```

## Result family

[`messages.DhConfig`](/reference/telegram/types/results/messages-dh-config/)

## Relationships

- Result family: [`messages.DhConfig`](/reference/telegram/types/results/messages-dh-config/)
- Related constructors: [`messages.dhConfig`](/reference/telegram/types/messages/dh-config/)
- Returned by: [`messages.getDhConfig`](/reference/telegram/functions/messages/get-dh-config/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
