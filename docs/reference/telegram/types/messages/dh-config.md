---
title: "messages.dhConfig"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "messages.dhConfig"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
layer: 228
schema_source: "tdlib"
constructor_id: "0x2c221edd"
---

# `messages.dhConfig`

No description provided by the pinned schema.

## Signature

```tl
messages.dhConfig#2c221edd g:int p:bytes version:int random:bytes = messages.DhConfig;
```

## Result type

`messages.DhConfig`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| g | int | — | — | No description provided by the pinned schema. |
| p | bytes | — | — | No description provided by the pinned schema. |
| version | int | — | — | No description provided by the pinned schema. |
| random | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import MessagesDhConfig
```

Public access: `miniproto.raw.types.MessagesDhConfig`.

## Safe usage shape

```python
from miniproto.raw.types import MessagesDhConfig

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MessagesDhConfig
```

## Result family

[`messages.DhConfig`](/reference/telegram/types/results/messages-dh-config/)

## Relationships

- Result family: [`messages.DhConfig`](/reference/telegram/types/results/messages-dh-config/)
- Related constructors: [`messages.dhConfigNotModified`](/reference/telegram/types/messages/dh-config-not-modified/)
- Returned by: [`messages.getDhConfig`](/reference/telegram/functions/messages/get-dh-config/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
