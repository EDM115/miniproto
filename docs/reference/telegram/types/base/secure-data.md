---
title: "secureData"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "secureData"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x8aeabec3"
---

# `secureData`

No description provided by the pinned schema.

## Signature

```tl
secureData#8aeabec3 data:bytes data_hash:bytes secret:bytes = SecureData;
```

## Result type

`SecureData`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| data | bytes | — | — | No description provided by the pinned schema. |
| data_hash | bytes | — | — | No description provided by the pinned schema. |
| secret | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import SecureData
```

Public access: `miniproto.raw.types.SecureData`.

## Class reference

```python
from miniproto.raw.types import SecureData

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = SecureData
```

## Result family

[`SecureData`](/reference/telegram/types/results/secure-data/)

## Relationships

- Result family: [`SecureData`](/reference/telegram/types/results/secure-data/)
- Accepted by: [`inputSecureValue`](/reference/telegram/types/base/input-secure-value/), [`secureValue`](/reference/telegram/types/base/secure-value/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
