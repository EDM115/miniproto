---
title: "inputBusinessRecipients"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputBusinessRecipients"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0x6f8b32aa"
---

# `inputBusinessRecipients`

No description provided by the pinned schema.

## Signature

```tl
inputBusinessRecipients#6f8b32aa flags:# existing_chats:flags.0?true new_chats:flags.1?true contacts:flags.2?true non_contacts:flags.3?true exclude_selected:flags.5?true users:flags.4?Vector<InputUser> = InputBusinessRecipients;
```

## Result type

`InputBusinessRecipients`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| existing_chats | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| new_chats | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| contacts | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| non_contacts | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| exclude_selected | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| users | flags.4?Vector<InputUser> | flags.4 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| existing_chats | 0 | Controlled by `flags`; present when this bit is set. |
| new_chats | 1 | Controlled by `flags`; present when this bit is set. |
| contacts | 2 | Controlled by `flags`; present when this bit is set. |
| non_contacts | 3 | Controlled by `flags`; present when this bit is set. |
| exclude_selected | 5 | Controlled by `flags`; present when this bit is set. |
| users | 4 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import InputBusinessRecipients
```

Public access: `miniproto.raw.types.InputBusinessRecipients`.

## Safe usage shape

```python
from miniproto.raw.types import InputBusinessRecipients

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputBusinessRecipients
```

## Result family

[`InputBusinessRecipients`](/reference/telegram/types/results/input-business-recipients/)

## Relationships

- Result family: [`InputBusinessRecipients`](/reference/telegram/types/results/input-business-recipients/)
- Accepted by: [`inputBusinessAwayMessage`](/reference/telegram/types/base/input-business-away-message/), [`inputBusinessGreetingMessage`](/reference/telegram/types/base/input-business-greeting-message/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
