---
title: "myBoost"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "myBoost"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xc448415c"
---

# `myBoost`

No description provided by the pinned schema.

## Signature

```tl
myBoost#c448415c flags:# slot:int peer:flags.0?Peer date:int expires:int cooldown_until_date:flags.1?int = MyBoost;
```

## Result type

`MyBoost`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| slot | int | — | — | No description provided by the pinned schema. |
| peer | flags.0?Peer | flags.0 | — | No description provided by the pinned schema. |
| date | int | — | — | No description provided by the pinned schema. |
| expires | int | — | — | No description provided by the pinned schema. |
| cooldown_until_date | flags.1?int | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| peer | 0 | Controlled by `flags`; present when this bit is set. |
| cooldown_until_date | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MyBoost
```

Public access: `miniproto.raw.types.MyBoost`.

## Safe usage shape

```python
from miniproto.raw.types import MyBoost

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MyBoost
```

## Result family

[`MyBoost`](/reference/telegram/types/results/my-boost/)

## Relationships

- Result family: [`MyBoost`](/reference/telegram/types/results/my-boost/)
- Accepted by: [`premium.myBoosts`](/reference/telegram/types/premium/my-boosts/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
