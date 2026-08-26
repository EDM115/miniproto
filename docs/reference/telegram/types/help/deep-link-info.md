---
title: "help.deepLinkInfo"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.deepLinkInfo"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
schema_source: "tdlib"
constructor_id: "0x6a4ee832"
---

# `help.deepLinkInfo`

No description provided by the pinned schema.

## Signature

```tl
help.deepLinkInfo#6a4ee832 flags:# update_app:flags.0?true message:string entities:flags.1?Vector<MessageEntity> = help.DeepLinkInfo;
```

## Result type

`help.DeepLinkInfo`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| update_app | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| message | string | — | — | No description provided by the pinned schema. |
| entities | flags.1?Vector<MessageEntity> | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| update_app | 0 | Controlled by `flags`; present when this bit is set. |
| entities | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import HelpDeepLinkInfo
```

Public access: `miniproto.raw.types.HelpDeepLinkInfo`.

## Safe usage shape

```python
from miniproto.raw.types import HelpDeepLinkInfo

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = HelpDeepLinkInfo
```

## Result family

[`help.DeepLinkInfo`](/reference/telegram/types/results/help-deep-link-info/)

## Relationships

- Result family: [`help.DeepLinkInfo`](/reference/telegram/types/results/help-deep-link-info/)
- Related constructors: [`help.deepLinkInfoEmpty`](/reference/telegram/types/help/deep-link-info-empty/)
- Returned by: [`help.getDeepLinkInfo`](/reference/telegram/functions/help/get-deep-link-info/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
