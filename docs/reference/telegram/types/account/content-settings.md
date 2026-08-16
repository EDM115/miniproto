---
title: "account.contentSettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.contentSettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0x57e28221"
---

# `account.contentSettings`

No description provided by the pinned schema.

## Signature

```tl
account.contentSettings#57e28221 flags:# sensitive_enabled:flags.0?true sensitive_can_change:flags.1?true = account.ContentSettings;
```

## Result type

`account.ContentSettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| sensitive_enabled | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| sensitive_can_change | flags.1?true | flags.1 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| sensitive_enabled | 0 | Controlled by `flags`; present when this bit is set. |
| sensitive_can_change | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import AccountContentSettings
```

Public access: `miniproto.raw.types.AccountContentSettings`.

## Safe usage shape

```python
from miniproto.raw.types import AccountContentSettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountContentSettings
```

## Result family

[`account.ContentSettings`](/reference/telegram/types/results/account-content-settings/)

## Relationships

- Result family: [`account.ContentSettings`](/reference/telegram/types/results/account-content-settings/)
- Returned by: [`account.getContentSettings`](/reference/telegram/functions/account/get-content-settings/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
