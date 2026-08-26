---
title: "businessBotRecipients"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "businessBotRecipients"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xb88cf373"
---

# `businessBotRecipients`

No description provided by the pinned schema.

## Signature

```tl
businessBotRecipients#b88cf373 flags:# existing_chats:flags.0?true new_chats:flags.1?true contacts:flags.2?true non_contacts:flags.3?true exclude_selected:flags.5?true users:flags.4?Vector<long> exclude_users:flags.6?Vector<long> = BusinessBotRecipients;
```

## Result type

`BusinessBotRecipients`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| existing_chats | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| new_chats | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| contacts | flags.2?true | flags.2 | — | No description provided by the pinned schema. |
| non_contacts | flags.3?true | flags.3 | — | No description provided by the pinned schema. |
| exclude_selected | flags.5?true | flags.5 | — | No description provided by the pinned schema. |
| users | flags.4?Vector<long> | flags.4 | — | No description provided by the pinned schema. |
| exclude_users | flags.6?Vector<long> | flags.6 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| existing_chats | 0 | Controlled by `flags`; present when this bit is set. |
| new_chats | 1 | Controlled by `flags`; present when this bit is set. |
| contacts | 2 | Controlled by `flags`; present when this bit is set. |
| non_contacts | 3 | Controlled by `flags`; present when this bit is set. |
| exclude_selected | 5 | Controlled by `flags`; present when this bit is set. |
| users | 4 | Controlled by `flags`; present when this bit is set. |
| exclude_users | 6 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import BusinessBotRecipients
```

Public access: `miniproto.raw.types.BusinessBotRecipients`.

## Safe usage shape

```python
from miniproto.raw.types import BusinessBotRecipients

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = BusinessBotRecipients
```

## Result family

[`BusinessBotRecipients`](/reference/telegram/types/results/business-bot-recipients/)

## Relationships

- Result family: [`BusinessBotRecipients`](/reference/telegram/types/results/business-bot-recipients/)
- Accepted by: [`connectedBot`](/reference/telegram/types/base/connected-bot/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
