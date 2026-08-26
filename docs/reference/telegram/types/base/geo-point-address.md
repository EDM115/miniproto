---
title: "geoPointAddress"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "geoPointAddress"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xde4c5d93"
---

# `geoPointAddress`

No description provided by the pinned schema.

## Signature

```tl
geoPointAddress#de4c5d93 flags:# country_iso2:string state:flags.0?string city:flags.1?string street:flags.2?string = GeoPointAddress;
```

## Result type

`GeoPointAddress`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| country_iso2 | string | — | — | No description provided by the pinned schema. |
| state | flags.0?string | flags.0 | — | No description provided by the pinned schema. |
| city | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| street | flags.2?string | flags.2 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| state | 0 | Controlled by `flags`; present when this bit is set. |
| city | 1 | Controlled by `flags`; present when this bit is set. |
| street | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import GeoPointAddress
```

Public access: `miniproto.raw.types.GeoPointAddress`.

## Safe usage shape

```python
from miniproto.raw.types import GeoPointAddress

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = GeoPointAddress
```

## Result family

[`GeoPointAddress`](/reference/telegram/types/results/geo-point-address/)

## Relationships

- Result family: [`GeoPointAddress`](/reference/telegram/types/results/geo-point-address/)
- Accepted by: [`mediaAreaGeoPoint`](/reference/telegram/types/base/media-area-geo-point/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
