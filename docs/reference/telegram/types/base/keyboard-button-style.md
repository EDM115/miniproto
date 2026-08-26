---
title: "keyboardButtonStyle"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "keyboardButtonStyle"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x4fdd3430"
---

# `keyboardButtonStyle`

No description provided by the pinned schema.

## Signature

```tl
keyboardButtonStyle#4fdd3430 flags:# bg_primary:flags.0?true bg_danger:flags.1?true bg_success:flags.2?true icon:flags.3?long = KeyboardButtonStyle;
```

## Result type

`KeyboardButtonStyle`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| bg_primary | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| bg_danger | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| bg_success | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| icon | flags.3?long | flags.3 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| bg_primary | 0 | Controlled by `flags`; present when this bit is set. |
| bg_danger | 1 | Controlled by `flags`; present when this bit is set. |
| bg_success | 2 | Controlled by `flags`; present when this bit is set. |
| icon | 3 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import KeyboardButtonStyle
```

Public access: `miniproto.raw.types.KeyboardButtonStyle`.

## Safe usage shape

```python
from miniproto.raw.types import KeyboardButtonStyle

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = KeyboardButtonStyle
```

## Result family

[`KeyboardButtonStyle`](/reference/telegram/types/results/keyboard-button-style/)

## Relationships

- Result family: [`KeyboardButtonStyle`](/reference/telegram/types/results/keyboard-button-style/)
- Accepted by: [`keyboardButton`](/reference/telegram/types/base/keyboard-button/), [`keyboardInlineButton`](/reference/telegram/types/base/keyboard-inline-button/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
