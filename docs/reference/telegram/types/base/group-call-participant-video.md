---
title: "groupCallParticipantVideo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "groupCallParticipantVideo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x67753ac8"
---

# `groupCallParticipantVideo`

No description provided by the pinned schema.

## Signature

```tl
groupCallParticipantVideo#67753ac8 flags:# paused:flags.0?true endpoint:string source_groups:Vector<GroupCallParticipantVideoSourceGroup> audio_source:flags.1?int = GroupCallParticipantVideo;
```

## Result type

`GroupCallParticipantVideo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| paused | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| endpoint | string | — | — | No description provided by the pinned schema. |
| source_groups | Vector<GroupCallParticipantVideoSourceGroup> | — | — | No description provided by the pinned schema. |
| audio_source | flags.1?int | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| paused | 0 | Controlled by `flags`; present when this bit is set. |
| audio_source | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import GroupCallParticipantVideo
```

Public access: `miniproto.raw.types.GroupCallParticipantVideo`.

## Safe usage shape

```python
from miniproto.raw.types import GroupCallParticipantVideo

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = GroupCallParticipantVideo
```

## Result family

[`GroupCallParticipantVideo`](/reference/telegram/types/results/group-call-participant-video/)

## Relationships

- Result family: [`GroupCallParticipantVideo`](/reference/telegram/types/results/group-call-participant-video/)
- Accepted by: [`groupCallParticipant`](/reference/telegram/types/base/group-call-participant/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
