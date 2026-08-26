---
title: "dialogFilter"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "dialogFilter"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xaa472651"
---

# `dialogFilter`

No description provided by the pinned schema.

## Signature

```tl
dialogFilter#aa472651 flags:# contacts:flags.0?true non_contacts:flags.1?true groups:flags.2?true broadcasts:flags.3?true bots:flags.4?true exclude_muted:flags.11?true exclude_read:flags.12?true exclude_archived:flags.13?true title_noanimate:flags.28?true id:int title:TextWithEntities emoticon:flags.25?string color:flags.27?int pinned_peers:Vector<InputPeer> include_peers:Vector<InputPeer> exclude_peers:Vector<InputPeer> = DialogFilter;
```

## Result type

`DialogFilter`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| contacts | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| non_contacts | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| groups | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| broadcasts | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| bots | flags.4?true | flags.4 | — | No description provided by the pinned schema. |
| exclude_muted | flags.11?true | flags.11 | — | No description provided by the pinned schema. |
| exclude_read | flags.12?true | flags.12 | — | No description provided by the pinned schema. |
| exclude_archived | flags.13?true | flags.13 | — | No description provided by the pinned schema. |
| title_noanimate | flags.28?true | flags.28 | — | No description provided by the pinned schema. |
| id | int | — | — | No description provided by the pinned schema. |
| title | TextWithEntities | — | — | No description provided by the pinned schema. |
| emoticon | flags.25?string | flags.25 | — | No description provided by the pinned schema. |
| color | flags.27?int | flags.27 | — | No description provided by the pinned schema. |
| pinned_peers | Vector<InputPeer> | — | — | No description provided by the pinned schema. |
| include_peers | Vector<InputPeer> | — | — | No description provided by the pinned schema. |
| exclude_peers | Vector<InputPeer> | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| contacts | 0 | Controlled by `flags`; present when this bit is set. |
| non_contacts | 1 | Controlled by `flags`; present when this bit is set. |
| groups | 2 | Controlled by `flags`; present when this bit is set. |
| broadcasts | 3 | Controlled by `flags`; present when this bit is set. |
| bots | 4 | Controlled by `flags`; present when this bit is set. |
| exclude_muted | 11 | Controlled by `flags`; present when this bit is set. |
| exclude_read | 12 | Controlled by `flags`; present when this bit is set. |
| exclude_archived | 13 | Controlled by `flags`; present when this bit is set. |
| title_noanimate | 28 | Controlled by `flags`; present when this bit is set. |
| emoticon | 25 | Controlled by `flags`; present when this bit is set. |
| color | 27 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import DialogFilter
```

Public access: `miniproto.raw.types.DialogFilter`.

## Safe usage shape

```python
from miniproto.raw.types import DialogFilter

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = DialogFilter
```

## Result family

[`DialogFilter`](/reference/telegram/types/results/dialog-filter/)

## Relationships

- Result family: [`DialogFilter`](/reference/telegram/types/results/dialog-filter/)
- Related constructors: [`dialogFilterChatlist`](/reference/telegram/types/base/dialog-filter-chatlist/), [`dialogFilterDefault`](/reference/telegram/types/base/dialog-filter-default/)
- Accepted by: [`messages.updateDialogFilter`](/reference/telegram/functions/messages/update-dialog-filter/), [`chatlists.exportedChatlistInvite`](/reference/telegram/types/chatlists/exported-chatlist-invite/), [`dialogFilterSuggested`](/reference/telegram/types/base/dialog-filter-suggested/), [`messages.dialogFilters`](/reference/telegram/types/messages/dialog-filters/), [`updateDialogFilter`](/reference/telegram/types/base/update-dialog-filter/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
