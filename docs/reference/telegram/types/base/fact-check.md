---
title: "factCheck"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "factCheck"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xb89bfccf"
---

# `factCheck`

No description provided by the pinned schema.

## Signature

```tl
factCheck#b89bfccf flags:# need_check:flags.0?true country:flags.1?string text:flags.1?TextWithEntities hash:long = FactCheck;
```

## Result type

`FactCheck`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| need_check | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| country | flags.1?string | flags.1 | — | No description provided by the pinned schema. |
| text | flags.1?TextWithEntities | flags.1 | — | No description provided by the pinned schema. |
| hash | long | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| need_check | 0 | Controlled by `flags`; present when this bit is set. |
| country | 1 | Controlled by `flags`; present when this bit is set. |
| text | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import FactCheck
```

Public access: `miniproto.raw.types.FactCheck`.

## Safe usage shape

```python
from miniproto.raw.types import FactCheck

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = FactCheck
```

## Result family

[`FactCheck`](/reference/telegram/types/results/fact-check/)

## Relationships

- Result family: [`FactCheck`](/reference/telegram/types/results/fact-check/)
- Accepted by: [`message`](/reference/telegram/types/base/message/)
- Returned by: [`messages.getFactCheck`](/reference/telegram/functions/messages/get-fact-check/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
