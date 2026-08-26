---
title: "account.webBrowserSettingsNotModified"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.webBrowserSettingsNotModified"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
schema_source: "tdlib"
constructor_id: "0xc31c8f4e"
---

# `account.webBrowserSettingsNotModified`

No description provided by the pinned schema.

## Signature

```tl
account.webBrowserSettingsNotModified#c31c8f4e = account.WebBrowserSettings;
```

## Result type

`account.WebBrowserSettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| — | — | — | — | This declaration has no parameters. |

## Python binding

```python
from miniproto.raw.types import AccountWebBrowserSettingsNotModified
```

Public access: `miniproto.raw.types.AccountWebBrowserSettingsNotModified`.

## Safe usage shape

```python
from miniproto.raw.types import AccountWebBrowserSettingsNotModified

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountWebBrowserSettingsNotModified
```

## Result family

[`account.WebBrowserSettings`](/reference/telegram/types/results/account-web-browser-settings/)

## Relationships

- Result family: [`account.WebBrowserSettings`](/reference/telegram/types/results/account-web-browser-settings/)
- Related constructors: [`account.webBrowserSettings`](/reference/telegram/types/account/web-browser-settings/)
- Returned by: [`account.deleteWebBrowserSettingsExceptions`](/reference/telegram/functions/account/delete-web-browser-settings-exceptions/), [`account.getWebBrowserSettings`](/reference/telegram/functions/account/get-web-browser-settings/), [`account.updateWebBrowserSettings`](/reference/telegram/functions/account/update-web-browser-settings/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
