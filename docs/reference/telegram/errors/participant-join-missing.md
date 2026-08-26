---
title: "PARTICIPANT_JOIN_MISSING"
description: "Trying to enable a presentation, when the user hasn't joined the Video Chat with [phone.joinGroupCall](https://core.telegram.org/method/phone.joinGroupCall)."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "400:PARTICIPANT_JOIN_MISSING"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
schema_source: "tdlib"
---

# `PARTICIPANT_JOIN_MISSING`

Trying to enable a presentation, when the user hasn't joined the Video Chat with [phone.joinGroupCall](https://core.telegram.org/method/phone.joinGroupCall).

## Error details

- code: 400
- parameterized: no
- mapped methods: [`phone.editGroupCallParticipant`](/reference/telegram/functions/phone/edit-group-call-participant/), [`phone.joinGroupCallPresentation`](/reference/telegram/functions/phone/join-group-call-presentation/)

## Python error class

```python
from miniproto.errors import ParticipantJoinMissing
```

Public access: `miniproto.errors.ParticipantJoinMissing`.

## Provenance

- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
