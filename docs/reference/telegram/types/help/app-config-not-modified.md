---
title: "help.appConfigNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.appConfigNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
schema_source: "tdlib"
constructor_id: "0x7cde641d"
---

# `help.appConfigNotModified`

No description provided by the pinned schema.

## Signature

```tl
help.appConfigNotModified#7cde641d = help.AppConfig;
```

## Result type

`help.AppConfig`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import HelpAppConfigNotModified
```

Public access: `miniproto.raw.types.HelpAppConfigNotModified`.

## Class reference

```python
from miniproto.raw.types import HelpAppConfigNotModified

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = HelpAppConfigNotModified
```

## Result family

[`help.AppConfig`](/reference/telegram/types/results/help-app-config/)

## Relationships

- Result family: [`help.AppConfig`](/reference/telegram/types/results/help-app-config/)
- Related constructors: [`help.appConfig`](/reference/telegram/types/help/app-config/)
- Returned by: [`help.getAppConfig`](/reference/telegram/functions/help/get-app-config/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
