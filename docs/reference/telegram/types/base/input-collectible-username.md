---
title: "inputCollectibleUsername"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputCollectibleUsername"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xe39460a9"
---

# `inputCollectibleUsername`

No description provided by the pinned schema.

## Signature

```tl
inputCollectibleUsername#e39460a9 username:string = InputCollectible;
```

## Result type

`InputCollectible`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| username | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputCollectibleUsername
```

Public access: `miniproto.raw.types.InputCollectibleUsername`.

## Safe usage shape

```python
from miniproto.raw.types import InputCollectibleUsername

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputCollectibleUsername
```

## Result family

[`InputCollectible`](/reference/telegram/types/results/input-collectible/)

## Relationships

- Result family: [`InputCollectible`](/reference/telegram/types/results/input-collectible/)
- Related constructors: [`inputCollectiblePhone`](/reference/telegram/types/base/input-collectible-phone/)
- Accepted by: [`fragment.getCollectibleInfo`](/reference/telegram/functions/fragment/get-collectible-info/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
