---
title: "bots.requestedButton"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "bots.requestedButton"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "bots"
schema_source: "tdlib"
constructor_id: "0xf13bbcd7"
---

# `bots.requestedButton`

No description provided by the pinned schema.

## Signature

```tl
bots.requestedButton#f13bbcd7 webapp_req_id:string = bots.RequestedButton;
```

## Result type

`bots.RequestedButton`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| webapp_req_id | string | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import BotsRequestedButton
```

Public access: `miniproto.raw.types.BotsRequestedButton`.

## Class reference

```python
from miniproto.raw.types import BotsRequestedButton

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = BotsRequestedButton
```

## Result family

[`bots.RequestedButton`](/reference/telegram/types/results/bots-requested-button/)

## Relationships

- Result family: [`bots.RequestedButton`](/reference/telegram/types/results/bots-requested-button/)
- Returned by: [`bots.requestWebViewButton`](/reference/telegram/functions/bots/request-web-view-button/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
