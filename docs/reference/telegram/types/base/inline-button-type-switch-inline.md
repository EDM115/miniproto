---
title: "inlineButtonTypeSwitchInline"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inlineButtonTypeSwitchInline"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x93773ff5"
---

# `inlineButtonTypeSwitchInline`

No description provided by the pinned schema.

## Signature

```tl
inlineButtonTypeSwitchInline#93773ff5 flags:# same_peer:flags.0?true query:string peer_types:flags.1?Vector<InlineQueryPeerType> = InlineButtonType;
```

## Result type

`InlineButtonType`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| same_peer | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| query | string | — | — | No description provided by the pinned schema. |
| peer_types | flags.1?Vector<InlineQueryPeerType> | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| same_peer | 0 | Controlled by `flags`; present when this bit is set. |
| peer_types | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InlineButtonTypeSwitchInline
```

Public access: `miniproto.raw.types.InlineButtonTypeSwitchInline`.

## Safe usage shape

```python
from miniproto.raw.types import InlineButtonTypeSwitchInline

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InlineButtonTypeSwitchInline
```

## Result family

[`InlineButtonType`](/reference/telegram/types/results/inline-button-type/)

## Relationships

- Result family: [`InlineButtonType`](/reference/telegram/types/results/inline-button-type/)
- Related constructors: [`inlineButtonTypeBuy`](/reference/telegram/types/base/inline-button-type-buy/), [`inlineButtonTypeCallback`](/reference/telegram/types/base/inline-button-type-callback/), [`inlineButtonTypeCopy`](/reference/telegram/types/base/inline-button-type-copy/), [`inlineButtonTypeDisabled`](/reference/telegram/types/base/inline-button-type-disabled/), [`inlineButtonTypeGame`](/reference/telegram/types/base/inline-button-type-game/), [`inlineButtonTypeUrl`](/reference/telegram/types/base/inline-button-type-url/), [`inlineButtonTypeUrlAuth`](/reference/telegram/types/base/inline-button-type-url-auth/), [`inlineButtonTypeUserProfile`](/reference/telegram/types/base/inline-button-type-user-profile/), [`inlineButtonTypeWebView`](/reference/telegram/types/base/inline-button-type-web-view/), [`inputInlineButtonTypeUrlAuth`](/reference/telegram/types/base/input-inline-button-type-url-auth/), [`inputInlineButtonTypeUserProfile`](/reference/telegram/types/base/input-inline-button-type-user-profile/)
- Accepted by: [`keyboardInlineButton`](/reference/telegram/types/base/keyboard-inline-button/), [`pageButton`](/reference/telegram/types/base/page-button/), [`textButton`](/reference/telegram/types/base/text-button/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
