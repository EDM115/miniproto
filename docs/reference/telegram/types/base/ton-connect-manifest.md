---
title: "tonConnectManifest"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "tonConnectManifest"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x12229264"
---

# `tonConnectManifest`

No description provided by the pinned schema.

## Signature

```tl
tonConnectManifest#12229264 flags:# url:string name:string icon:flags.0?WebDocument = TonConnectManifest;
```

## Result type

`TonConnectManifest`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| url | string | — | — | No description provided by the pinned schema. |
| name | string | — | — | No description provided by the pinned schema. |
| icon | flags.0?WebDocument | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| icon | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import TonConnectManifest
```

Public access: `miniproto.raw.types.TonConnectManifest`.

## Safe usage shape

```python
from miniproto.raw.types import TonConnectManifest

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = TonConnectManifest
```

## Result family

[`TonConnectManifest`](/reference/telegram/types/results/ton-connect-manifest/)

## Relationships

- Result family: [`TonConnectManifest`](/reference/telegram/types/results/ton-connect-manifest/)
- Accepted by: [`tonConnectSession`](/reference/telegram/types/base/ton-connect-session/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
