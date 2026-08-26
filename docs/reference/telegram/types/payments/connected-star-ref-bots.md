---
title: "payments.connectedStarRefBots"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "payments.connectedStarRefBots"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
constructor_id: "0x98d5ea1d"
---

# `payments.connectedStarRefBots`

No description provided by the pinned schema.

## Signature

```tl
payments.connectedStarRefBots#98d5ea1d count:int connected_bots:Vector<ConnectedBotStarRef> users:Vector<User> = payments.ConnectedStarRefBots;
```

## Result type

`payments.ConnectedStarRefBots`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| count | int | — | — | No description provided by the pinned schema. |
| connected_bots | Vector<ConnectedBotStarRef> | — | — | No description provided by the pinned schema. |
| users | Vector<User> | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import PaymentsConnectedStarRefBots
```

Public access: `miniproto.raw.types.PaymentsConnectedStarRefBots`.

## Safe usage shape

```python
from miniproto.raw.types import PaymentsConnectedStarRefBots

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = PaymentsConnectedStarRefBots
```

## Result family

[`payments.ConnectedStarRefBots`](/reference/telegram/types/results/payments-connected-star-ref-bots/)

## Relationships

- Result family: [`payments.ConnectedStarRefBots`](/reference/telegram/types/results/payments-connected-star-ref-bots/)
- Returned by: [`payments.connectStarRefBot`](/reference/telegram/functions/payments/connect-star-ref-bot/), [`payments.editConnectedStarRefBot`](/reference/telegram/functions/payments/edit-connected-star-ref-bot/), [`payments.getConnectedStarRefBot`](/reference/telegram/functions/payments/get-connected-star-ref-bot/), [`payments.getConnectedStarRefBots`](/reference/telegram/functions/payments/get-connected-star-ref-bots/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
