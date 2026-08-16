---
title: "help.peerColors"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "help.peerColors"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "help"
layer: 228
schema_source: "tdlib"
constructor_id: "0x00f8ed08"
---

# `help.peerColors`

No description provided by the pinned schema.

## Signature

```tl
help.peerColors#00f8ed08 hash:int colors:Vector<help.PeerColorOption> = help.PeerColors;
```

## Result type

`help.PeerColors`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| hash | int | — | — | No description provided by the pinned schema. |
| colors | Vector<help.PeerColorOption> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import HelpPeerColors
```

Public access: `miniproto.raw.types.HelpPeerColors`.

## Safe usage shape

```python
from miniproto.raw.types import HelpPeerColors

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = HelpPeerColors
```

## Result family

[`help.PeerColors`](/reference/telegram/types/results/help-peer-colors/)

## Relationships

- Result family: [`help.PeerColors`](/reference/telegram/types/results/help-peer-colors/)
- Related constructors: [`help.peerColorsNotModified`](/reference/telegram/types/help/peer-colors-not-modified/)
- Returned by: [`help.getPeerColors`](/reference/telegram/functions/help/get-peer-colors/), [`help.getPeerProfileColors`](/reference/telegram/functions/help/get-peer-profile-colors/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
