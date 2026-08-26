---
title: "accessPointRule"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "accessPointRule"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x4679b65f"
---

# `accessPointRule`

No description provided by the pinned schema.

## Signature

```tl
accessPointRule#4679b65f phone_prefix_rules:string dc_id:int ips:vector<IpPort> = AccessPointRule;
```

## Result type

`AccessPointRule`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| phone_prefix_rules | string | — | — | No description provided by the pinned schema. |
| dc_id | int | — | — | No description provided by the pinned schema. |
| ips | vector<IpPort> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AccessPointRule
```

Public access: `miniproto.raw.types.AccessPointRule`.

## Safe usage shape

```python
from miniproto.raw.types import AccessPointRule

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccessPointRule
```

## Result family

[`AccessPointRule`](/reference/telegram/types/results/access-point-rule/)

## Relationships

- Result family: [`AccessPointRule`](/reference/telegram/types/results/access-point-rule/)
- Accepted by: [`help.configSimple`](/reference/telegram/types/help/config-simple/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
