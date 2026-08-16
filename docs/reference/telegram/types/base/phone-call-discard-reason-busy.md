---
title: "phoneCallDiscardReasonBusy"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "phoneCallDiscardReasonBusy"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xfaf7e8c9"
---

# `phoneCallDiscardReasonBusy`

No description provided by the pinned schema.

## Signature

```tl
phoneCallDiscardReasonBusy#faf7e8c9 = PhoneCallDiscardReason;
```

## Result type

`PhoneCallDiscardReason`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import PhoneCallDiscardReasonBusy
```

Public access: `miniproto.raw.types.PhoneCallDiscardReasonBusy`.

## Safe usage shape

```python
from miniproto.raw.types import PhoneCallDiscardReasonBusy

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PhoneCallDiscardReasonBusy
```

## Result family

[`PhoneCallDiscardReason`](/reference/telegram/types/results/phone-call-discard-reason/)

## Relationships

- Result family: [`PhoneCallDiscardReason`](/reference/telegram/types/results/phone-call-discard-reason/)
- Related constructors: [`phoneCallDiscardReasonDisconnect`](/reference/telegram/types/base/phone-call-discard-reason-disconnect/), [`phoneCallDiscardReasonHangup`](/reference/telegram/types/base/phone-call-discard-reason-hangup/), [`phoneCallDiscardReasonMigrateConferenceCall`](/reference/telegram/types/base/phone-call-discard-reason-migrate-conference-call/), [`phoneCallDiscardReasonMissed`](/reference/telegram/types/base/phone-call-discard-reason-missed/)
- Accepted by: [`phone.discardCall`](/reference/telegram/functions/phone/discard-call/), [`messageActionPhoneCall`](/reference/telegram/types/base/message-action-phone-call/), [`phoneCallDiscarded`](/reference/telegram/types/base/phone-call-discarded/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
