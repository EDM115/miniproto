---
title: "help.passportConfigNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.passportConfigNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
schema_source: "tdlib"
constructor_id: "0xbfb9f457"
---

# `help.passportConfigNotModified`

No description provided by the pinned schema.

## Signature

```tl
help.passportConfigNotModified#bfb9f457 = help.PassportConfig;
```

## Result type

`help.PassportConfig`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import HelpPassportConfigNotModified
```

Public access: `miniproto.raw.types.HelpPassportConfigNotModified`.

## Safe usage shape

```python
from miniproto.raw.types import HelpPassportConfigNotModified

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = HelpPassportConfigNotModified
```

## Result family

[`help.PassportConfig`](/reference/telegram/types/results/help-passport-config/)

## Relationships

- Result family: [`help.PassportConfig`](/reference/telegram/types/results/help-passport-config/)
- Related constructors: [`help.passportConfig`](/reference/telegram/types/help/passport-config/)
- Returned by: [`help.getPassportConfig`](/reference/telegram/functions/help/get-passport-config/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
