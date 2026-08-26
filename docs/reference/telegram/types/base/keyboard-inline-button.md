---
title: "keyboardInlineButton"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "keyboardInlineButton"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x11c1a322"
---

# `keyboardInlineButton`

No description provided by the pinned schema.

## Signature

```tl
keyboardInlineButton#11c1a322 flags:# style:flags.10?KeyboardButtonStyle text:string type:InlineButtonType = KeyboardInlineButton;
```

## Result type

`KeyboardInlineButton`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| style | flags.10?KeyboardButtonStyle | flags.10 | — | No description provided by the pinned schema. |
| text | string | — | — | No description provided by the pinned schema. |
| type | InlineButtonType | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| style | 10 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import KeyboardInlineButton
```

Public access: `miniproto.raw.types.KeyboardInlineButton`.

## Safe usage shape

```python
from miniproto.raw.types import KeyboardInlineButton

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = KeyboardInlineButton
```

## Result family

[`KeyboardInlineButton`](/reference/telegram/types/results/keyboard-inline-button/)

## Relationships

- Result family: [`KeyboardInlineButton`](/reference/telegram/types/results/keyboard-inline-button/)
- Accepted by: [`keyboardInlineButtonRow`](/reference/telegram/types/base/keyboard-inline-button-row/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
