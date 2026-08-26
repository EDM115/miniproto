---
title: "phoneCallDiscardReasonMissed"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "phoneCallDiscardReasonMissed"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x85e42301"
---

# `phoneCallDiscardReasonMissed`

No description provided by the pinned schema.

## Signature

```tl
phoneCallDiscardReasonMissed#85e42301 = PhoneCallDiscardReason;
```

## Result type

`PhoneCallDiscardReason`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import PhoneCallDiscardReasonMissed
```

Public access: `miniproto.raw.types.PhoneCallDiscardReasonMissed`.

## Safe usage shape

```python
from miniproto.raw.types import PhoneCallDiscardReasonMissed

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PhoneCallDiscardReasonMissed
```

## Result family

[`PhoneCallDiscardReason`](/reference/telegram/types/results/phone-call-discard-reason/)

## Relationships

- Result family: [`PhoneCallDiscardReason`](/reference/telegram/types/results/phone-call-discard-reason/)
- Related constructors: [`phoneCallDiscardReasonBusy`](/reference/telegram/types/base/phone-call-discard-reason-busy/), [`phoneCallDiscardReasonDisconnect`](/reference/telegram/types/base/phone-call-discard-reason-disconnect/), [`phoneCallDiscardReasonHangup`](/reference/telegram/types/base/phone-call-discard-reason-hangup/), [`phoneCallDiscardReasonMigrateConferenceCall`](/reference/telegram/types/base/phone-call-discard-reason-migrate-conference-call/)
- Accepted by: [`phone.discardCall`](/reference/telegram/functions/phone/discard-call/), [`messageActionPhoneCall`](/reference/telegram/types/base/message-action-phone-call/), [`phoneCallDiscarded`](/reference/telegram/types/base/phone-call-discarded/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
