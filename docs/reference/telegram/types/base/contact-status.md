---
title: "contactStatus"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "contactStatus"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x16d9703b"
---

# `contactStatus`

No description provided by the pinned schema.

## Signature

```tl
contactStatus#16d9703b user_id:long status:UserStatus = ContactStatus;
```

## Result type

`ContactStatus`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| user_id | long | — | — | No description provided by the pinned schema. |
| status | UserStatus | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import ContactStatus
```

Public access: `miniproto.raw.types.ContactStatus`.

## Class reference

```python
from miniproto.raw.types import ContactStatus

# Refer to the raw constructor class without constructing it or calling Telegram
constructor_type = ContactStatus
```

## Result family

[`ContactStatus`](/reference/telegram/types/results/contact-status/)

## Relationships

- Result family: [`ContactStatus`](/reference/telegram/types/results/contact-status/)
- Returned by: [`contacts.getStatuses`](/reference/telegram/functions/contacts/get-statuses/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
