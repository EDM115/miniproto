---
title: "missingInvitee"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "missingInvitee"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0x628c9224"
---

# `missingInvitee`

No description provided by the pinned schema.

## Signature

```tl
missingInvitee#628c9224 flags:# premium_would_allow_invite:flags.0?true premium_required_for_pm:flags.1?true user_id:long = MissingInvitee;
```

## Result type

`MissingInvitee`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| premium_would_allow_invite | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| premium_required_for_pm | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| user_id | long | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| premium_would_allow_invite | 0 | Controlled by `flags`; present when this bit is set. |
| premium_required_for_pm | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import MissingInvitee
```

Public access: `miniproto.raw.types.MissingInvitee`.

## Safe usage shape

```python
from miniproto.raw.types import MissingInvitee

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = MissingInvitee
```

## Result family

[`MissingInvitee`](/reference/telegram/types/results/missing-invitee/)

## Relationships

- Result family: [`MissingInvitee`](/reference/telegram/types/results/missing-invitee/)
- Accepted by: [`messages.invitedUsers`](/reference/telegram/types/messages/invited-users/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
