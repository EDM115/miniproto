---
title: "urlAuthResultRequest"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "urlAuthResultRequest"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x3cd623ec"
---

# `urlAuthResultRequest`

No description provided by the pinned schema.

## Signature

```tl
urlAuthResultRequest#3cd623ec flags:# request_write_access:flags.0?true request_phone_number:flags.1?true match_codes_first:flags.5?true is_app:flags.6?true bot:User domain:string browser:flags.2?string platform:flags.2?string ip:flags.2?string region:flags.2?string match_codes:flags.3?Vector<string> user_id_hint:flags.4?long verified_app_name:flags.7?string = UrlAuthResult;
```

## Result type

`UrlAuthResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| request_write_access | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| request_phone_number | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| match_codes_first | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| is_app | flags.6?true | flags.6 | — | No description provided by the pinned schema. |
| bot | User | — | — | No description provided by the pinned schema. |
| domain | string | — | — | No description provided by the pinned schema. |
| browser | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| platform | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| ip | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| region | flags.2?string | flags.2 | — | No description provided by the pinned schema. |
| match_codes | flags.3?Vector<string> | flags.3 | — | No description provided by the pinned schema. |
| user_id_hint | flags.4?long | flags.4 | — | No description provided by the pinned schema. |
| verified_app_name | flags.7?string | flags.7 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| request_write_access | 0 | Controlled by `flags`; present when this bit is set. |
| request_phone_number | 1 | Controlled by `flags`; present when this bit is set. |
| match_codes_first | 5 | Controlled by `flags`; present when this bit is set. |
| is_app | 6 | Controlled by `flags`; present when this bit is set. |
| browser | 2 | Controlled by `flags`; present when this bit is set. |
| platform | 2 | Controlled by `flags`; present when this bit is set. |
| ip | 2 | Controlled by `flags`; present when this bit is set. |
| region | 2 | Controlled by `flags`; present when this bit is set. |
| match_codes | 3 | Controlled by `flags`; present when this bit is set. |
| user_id_hint | 4 | Controlled by `flags`; present when this bit is set. |
| verified_app_name | 7 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import UrlAuthResultRequest
```

Public access: `miniproto.raw.types.UrlAuthResultRequest`.

## Safe usage shape

```python
from miniproto.raw.types import UrlAuthResultRequest

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = UrlAuthResultRequest
```

## Result family

[`UrlAuthResult`](/reference/telegram/types/results/url-auth-result/)

## Relationships

- Result family: [`UrlAuthResult`](/reference/telegram/types/results/url-auth-result/)
- Related constructors: [`urlAuthResultAccepted`](/reference/telegram/types/base/url-auth-result-accepted/), [`urlAuthResultDefault`](/reference/telegram/types/base/url-auth-result-default/)
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
