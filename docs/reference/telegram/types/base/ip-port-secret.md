---
title: "ipPortSecret"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "ipPortSecret"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x37982646"
---

# `ipPortSecret`

No description provided by the pinned schema.

## Signature

```tl
ipPortSecret#37982646 ipv4:int port:int secret:bytes = IpPort;
```

## Result type

`IpPort`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| ipv4 | int | — | — | No description provided by the pinned schema. |
| port | int | — | — | No description provided by the pinned schema. |
| secret | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import IpPortSecret
```

Public access: `miniproto.raw.types.IpPortSecret`.

## Safe usage shape

```python
from miniproto.raw.types import IpPortSecret

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = IpPortSecret
```

## Result family

[`IpPort`](/reference/telegram/types/results/ip-port/)

## Relationships

- Result family: [`IpPort`](/reference/telegram/types/results/ip-port/)
- Related constructors: [`ipPort`](/reference/telegram/types/base/ip-port/)
- Accepted by: [`accessPointRule`](/reference/telegram/types/base/access-point-rule/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
