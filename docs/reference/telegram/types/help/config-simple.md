---
title: "help.configSimple"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.configSimple"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
layer: 228
schema_source: "tdlib"
constructor_id: "0x5a592a6c"
---

# `help.configSimple`

No description provided by the pinned schema.

## Signature

```tl
help.configSimple#5a592a6c date:int expires:int rules:vector<AccessPointRule> = help.ConfigSimple;
```

## Result type

`help.ConfigSimple`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| date | int | — | — | No description provided by the pinned schema. |
| expires | int | — | — | No description provided by the pinned schema. |
| rules | vector<AccessPointRule> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import HelpConfigSimple
```

Public access: `miniproto.raw.types.HelpConfigSimple`.

## Safe usage shape

```python
from miniproto.raw.types import HelpConfigSimple

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = HelpConfigSimple
```

## Result family

[`help.ConfigSimple`](/reference/telegram/types/results/help-config-simple/)

## Relationships

- Result family: [`help.ConfigSimple`](/reference/telegram/types/results/help-config-simple/)
- No additional canonical relationships were found.

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
