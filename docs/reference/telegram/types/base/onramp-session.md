---
title: "onrampSession"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "onrampSession"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xd1e42e24"
---

# `onrampSession`

No description provided by the pinned schema.

## Signature

```tl
onrampSession#d1e42e24 provider:string session_id:string url:string expires_date:int = OnrampSession;
```

## Result type

`OnrampSession`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| provider | string | — | — | No description provided by the pinned schema. |
| session_id | string | — | — | No description provided by the pinned schema. |
| url | string | — | — | No description provided by the pinned schema. |
| expires_date | int | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import OnrampSession
```

Public access: `miniproto.raw.types.OnrampSession`.

## Class reference

```python
from miniproto.raw.types import OnrampSession

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = OnrampSession
```

## Result family

[`OnrampSession`](/reference/telegram/types/results/onramp-session/)

## Relationships

- Result family: [`OnrampSession`](/reference/telegram/types/results/onramp-session/)
- Returned by: [`payments.createOnrampSession`](/reference/telegram/functions/payments/create-onramp-session/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
