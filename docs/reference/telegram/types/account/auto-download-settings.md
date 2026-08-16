---
title: "account.autoDownloadSettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.autoDownloadSettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0x63cacf26"
---

# `account.autoDownloadSettings`

No description provided by the pinned schema.

## Signature

```tl
account.autoDownloadSettings#63cacf26 low:AutoDownloadSettings medium:AutoDownloadSettings high:AutoDownloadSettings = account.AutoDownloadSettings;
```

## Result type

`account.AutoDownloadSettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| low | AutoDownloadSettings | — | — | No description provided by the pinned schema. |
| medium | AutoDownloadSettings | — | — | No description provided by the pinned schema. |
| high | AutoDownloadSettings | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import AccountAutoDownloadSettings
```

Public access: `miniproto.raw.types.AccountAutoDownloadSettings`.

## Safe usage shape

```python
from miniproto.raw.types import AccountAutoDownloadSettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountAutoDownloadSettings
```

## Result family

[`account.AutoDownloadSettings`](/reference/telegram/types/results/account-auto-download-settings/)

## Relationships

- Result family: [`account.AutoDownloadSettings`](/reference/telegram/types/results/account-auto-download-settings/)
- Returned by: [`account.getAutoDownloadSettings`](/reference/telegram/functions/account/get-auto-download-settings/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
