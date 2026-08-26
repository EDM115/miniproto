---
title: "help.appConfig"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.appConfig"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
schema_source: "tdlib"
constructor_id: "0xdd18782e"
---

# `help.appConfig`

No description provided by the pinned schema.

## Signature

```tl
help.appConfig#dd18782e hash:int config:JSONValue = help.AppConfig;
```

## Result type

`help.AppConfig`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | int | — | — | No description provided by the pinned schema. |
| config | JSONValue | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import HelpAppConfig
```

Public access: `miniproto.raw.types.HelpAppConfig`.

## Safe usage shape

```python
from miniproto.raw.types import HelpAppConfig

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = HelpAppConfig
```

## Result family

[`help.AppConfig`](/reference/telegram/types/results/help-app-config/)

## Relationships

- Result family: [`help.AppConfig`](/reference/telegram/types/results/help-app-config/)
- Related constructors: [`help.appConfigNotModified`](/reference/telegram/types/help/app-config-not-modified/)
- Returned by: [`help.getAppConfig`](/reference/telegram/functions/help/get-app-config/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
