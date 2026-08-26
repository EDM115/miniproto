---
title: "inputBusinessAwayMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputBusinessAwayMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x832175e0"
---

# `inputBusinessAwayMessage`

No description provided by the pinned schema.

## Signature

```tl
inputBusinessAwayMessage#832175e0 flags:# offline_only:flags.0?true shortcut_id:int schedule:BusinessAwayMessageSchedule recipients:InputBusinessRecipients = InputBusinessAwayMessage;
```

## Result type

`InputBusinessAwayMessage`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| offline_only | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| shortcut_id | int | — | — | No description provided by the pinned schema. |
| schedule | BusinessAwayMessageSchedule | — | — | No description provided by the pinned schema. |
| recipients | InputBusinessRecipients | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| offline_only | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputBusinessAwayMessage
```

Public access: `miniproto.raw.types.InputBusinessAwayMessage`.

## Safe usage shape

```python
from miniproto.raw.types import InputBusinessAwayMessage

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputBusinessAwayMessage
```

## Result family

[`InputBusinessAwayMessage`](/reference/telegram/types/results/input-business-away-message/)

## Relationships

- Result family: [`InputBusinessAwayMessage`](/reference/telegram/types/results/input-business-away-message/)
- Accepted by: [`account.updateBusinessAwayMessage`](/reference/telegram/functions/account/update-business-away-message/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
