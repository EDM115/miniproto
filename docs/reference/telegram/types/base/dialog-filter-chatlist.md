---
title: "dialogFilterChatlist"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "dialogFilterChatlist"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x96537bd7"
---

# `dialogFilterChatlist`

No description provided by the pinned schema.

## Signature

```tl
dialogFilterChatlist#96537bd7 flags:# has_my_invites:flags.26?true title_noanimate:flags.28?true id:int title:TextWithEntities emoticon:flags.25?string color:flags.27?int pinned_peers:Vector<InputPeer> include_peers:Vector<InputPeer> = DialogFilter;
```

## Result type

`DialogFilter`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| has_my_invites | flags.26?true | flags.26 | — | No description provided by the pinned schema. |
| title_noanimate | flags.28?true | flags.28 | — | No description provided by the pinned schema. |
| id | int | — | — | No description provided by the pinned schema. |
| title | TextWithEntities | — | — | No description provided by the pinned schema. |
| emoticon | flags.25?string | flags.25 | — | No description provided by the pinned schema. |
| color | flags.27?int | flags.27 | — | No description provided by the pinned schema. |
| pinned_peers | Vector<InputPeer> | — | — | No description provided by the pinned schema. |
| include_peers | Vector<InputPeer> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| has_my_invites | 26 | Controlled by `flags`; present when this bit is set. |
| title_noanimate | 28 | Controlled by `flags`; present when this bit is set. |
| emoticon | 25 | Controlled by `flags`; present when this bit is set. |
| color | 27 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import DialogFilterChatlist
```

Public access: `miniproto.raw.types.DialogFilterChatlist`.

## Safe usage shape

```python
from miniproto.raw.types import DialogFilterChatlist

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = DialogFilterChatlist
```

## Result family

[`DialogFilter`](/reference/telegram/types/results/dialog-filter/)

## Relationships

- Result family: [`DialogFilter`](/reference/telegram/types/results/dialog-filter/)
- Related constructors: [`dialogFilter`](/reference/telegram/types/base/dialog-filter/), [`dialogFilterDefault`](/reference/telegram/types/base/dialog-filter-default/)
- Accepted by: [`messages.updateDialogFilter`](/reference/telegram/functions/messages/update-dialog-filter/), [`chatlists.exportedChatlistInvite`](/reference/telegram/types/chatlists/exported-chatlist-invite/), [`dialogFilterSuggested`](/reference/telegram/types/base/dialog-filter-suggested/), [`messages.dialogFilters`](/reference/telegram/types/messages/dialog-filters/), [`updateDialogFilter`](/reference/telegram/types/base/update-dialog-filter/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
