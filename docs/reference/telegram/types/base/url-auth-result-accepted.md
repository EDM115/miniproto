---
title: "urlAuthResultAccepted"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "urlAuthResultAccepted"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x623a8fa0"
---

# `urlAuthResultAccepted`

No description provided by the pinned schema.

## Signature

```tl
urlAuthResultAccepted#623a8fa0 flags:# url:flags.0?string = UrlAuthResult;
```

## Result type

`UrlAuthResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| url | flags.0?string | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| url | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import UrlAuthResultAccepted
```

Public access: `miniproto.raw.types.UrlAuthResultAccepted`.

## Safe usage shape

```python
from miniproto.raw.types import UrlAuthResultAccepted

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UrlAuthResultAccepted
```

## Result family

[`UrlAuthResult`](/reference/telegram/types/results/url-auth-result/)

## Relationships

- Result family: [`UrlAuthResult`](/reference/telegram/types/results/url-auth-result/)
- Related constructors: [`urlAuthResultDefault`](/reference/telegram/types/base/url-auth-result-default/), [`urlAuthResultRequest`](/reference/telegram/types/base/url-auth-result-request/)
- Returned by: [`messages.acceptUrlAuth`](/reference/telegram/functions/messages/accept-url-auth/), [`messages.requestUrlAuth`](/reference/telegram/functions/messages/request-url-auth/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
