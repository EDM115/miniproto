---
title: "dialogCommunity"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "dialogCommunity"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
layer: 228
schema_source: "tdlib"
constructor_id: "0xf78a0973"
---

# `dialogCommunity`

No description provided by the pinned schema.

## Signature

```tl
dialogCommunity#f78a0973 flags:# pinned:flags.2?true community_id:long notify_settings:PeerNotifySettings = Dialog;
```

## Result type

`Dialog`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| pinned | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| community_id | long | — | — | No description provided by the pinned schema. |
| notify_settings | PeerNotifySettings | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| pinned | 2 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import DialogCommunity
```

Public access: `miniproto.raw.types.DialogCommunity`.

## Safe usage shape

```python
from miniproto.raw.types import DialogCommunity

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = DialogCommunity
```

## Result family

[`Dialog`](/reference/telegram/types/results/dialog/)

## Relationships

- Result family: [`Dialog`](/reference/telegram/types/results/dialog/)
- Related constructors: [`dialog`](/reference/telegram/types/base/dialog/), [`dialogFolder`](/reference/telegram/types/base/dialog-folder/)
- Accepted by: [`messages.dialogs`](/reference/telegram/types/messages/dialogs/), [`messages.dialogsSlice`](/reference/telegram/types/messages/dialogs-slice/), [`messages.peerDialogs`](/reference/telegram/types/messages/peer-dialogs/), [`updates.channelDifferenceTooLong`](/reference/telegram/types/updates/channel-difference-too-long/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
