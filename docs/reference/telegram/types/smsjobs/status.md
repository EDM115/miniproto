---
title: "smsjobs.status"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "smsjobs.status"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "smsjobs"
schema_source: "tdlib"
constructor_id: "0x2aee9191"
---

# `smsjobs.status`

No description provided by the pinned schema.

## Signature

```tl
smsjobs.status#2aee9191 flags:# allow_international:flags.0?true recent_sent:int recent_since:int recent_remains:int total_sent:int total_since:int last_gift_slug:flags.1?string terms_url:string = smsjobs.Status;
```

## Result type

`smsjobs.Status`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| allow_international | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| recent_sent | int | — | — | No description provided by the pinned schema. |
| recent_since | int | — | — | No description provided by the pinned schema. |
| recent_remains | int | — | — | No description provided by the pinned schema. |
| total_sent | int | — | — | No description provided by the pinned schema. |
| total_since | int | — | — | No description provided by the pinned schema. |
| last_gift_slug | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| terms_url | string | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| allow_international | 0 | Controlled by `flags`; present when this bit is set. |
| last_gift_slug | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import SmsjobsStatus
```

Public access: `miniproto.raw.types.SmsjobsStatus`.

## Safe usage shape

```python
from miniproto.raw.types import SmsjobsStatus

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = SmsjobsStatus
```

## Result family

[`smsjobs.Status`](/reference/telegram/types/results/smsjobs-status/)

## Relationships

- Result family: [`smsjobs.Status`](/reference/telegram/types/results/smsjobs-status/)
- Returned by: [`smsjobs.getStatus`](/reference/telegram/functions/smsjobs/get-status/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
