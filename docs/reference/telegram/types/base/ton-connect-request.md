---
title: "tonConnectRequest"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "tonConnectRequest"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xa15f8513"
---

# `tonConnectRequest`

No description provided by the pinned schema.

## Signature

```tl
tonConnectRequest#a15f8513 flags:# session_id:long msg_id:int body:bytes expires:int topic:flags.0?string trace_id:flags.1?string = TonConnectRequest;
```

## Result type

`TonConnectRequest`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| session_id | long | — | — | No description provided by the pinned schema. |
| msg_id | int | — | — | No description provided by the pinned schema. |
| body | bytes | — | — | No description provided by the pinned schema. |
| expires | int | — | — | No description provided by the pinned schema. |
| topic | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| trace_id | flags.1?string | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| topic | 0 | Controlled by `flags`; present when this bit is set. |
| trace_id | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import TonConnectRequest
```

Public access: `miniproto.raw.types.TonConnectRequest`.

## Class reference

```python
from miniproto.raw.types import TonConnectRequest

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = TonConnectRequest
```

## Result family

[`TonConnectRequest`](/reference/telegram/types/results/ton-connect-request/)

## Relationships

- Result family: [`TonConnectRequest`](/reference/telegram/types/results/ton-connect-request/)
- Accepted by: [`wallet.tonConnectPending`](/reference/telegram/types/wallet/ton-connect-pending/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
