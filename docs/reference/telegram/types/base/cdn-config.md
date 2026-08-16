---
title: "cdnConfig"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "cdnConfig"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x5725e40a"
---

# `cdnConfig`

No description provided by the pinned schema.

## Signature

```tl
cdnConfig#5725e40a public_keys:Vector<CdnPublicKey> = CdnConfig;
```

## Result type

`CdnConfig`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| public_keys | Vector<CdnPublicKey> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import CdnConfig
```

Public access: `miniproto.raw.types.CdnConfig`.

## Safe usage shape

```python
from miniproto.raw.types import CdnConfig

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = CdnConfig
```

## Result family

[`CdnConfig`](/reference/telegram/types/results/cdn-config/)

## Relationships

- Result family: [`CdnConfig`](/reference/telegram/types/results/cdn-config/)
- Returned by: [`help.getCdnConfig`](/reference/telegram/functions/help/get-cdn-config/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
