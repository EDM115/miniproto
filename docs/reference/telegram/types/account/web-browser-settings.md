---
title: "account.webBrowserSettings"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "account.webBrowserSettings"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "account"
layer: 228
schema_source: "tdlib"
constructor_id: "0x79eb8cb3"
---

# `account.webBrowserSettings`

No description provided by the pinned schema.

## Signature

```tl
account.webBrowserSettings#79eb8cb3 flags:# open_external_browser:flags.0?true display_close_button:flags.1?true external_exceptions:Vector<WebDomainException> inapp_exceptions:Vector<WebDomainException> hash:long = account.WebBrowserSettings;
```

## Result type

`account.WebBrowserSettings`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| open_external_browser | flags.0?true | flags.0 | — | No description provided by the pinned schema. |
| display_close_button | flags.1?true | flags.1 | — | No description provided by the pinned schema. |
| external_exceptions | Vector<WebDomainException> | — | — | No description provided by the pinned schema. |
| inapp_exceptions | Vector<WebDomainException> | — | — | No description provided by the pinned schema. |
| hash | long | — | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| open_external_browser | 0 | Controlled by `flags`; present when this bit is set. |
| display_close_button | 1 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.types import AccountWebBrowserSettings
```

Public access: `miniproto.raw.types.AccountWebBrowserSettings`.

## Safe usage shape

```python
from miniproto.raw.types import AccountWebBrowserSettings

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = AccountWebBrowserSettings
```

## Result family

[`account.WebBrowserSettings`](/reference/telegram/types/results/account-web-browser-settings/)

## Relationships

- Result family: [`account.WebBrowserSettings`](/reference/telegram/types/results/account-web-browser-settings/)
- Related constructors: [`account.webBrowserSettingsNotModified`](/reference/telegram/types/account/web-browser-settings-not-modified/)
- Returned by: [`account.deleteWebBrowserSettingsExceptions`](/reference/telegram/functions/account/delete-web-browser-settings-exceptions/), [`account.getWebBrowserSettings`](/reference/telegram/functions/account/get-web-browser-settings/), [`account.updateWebBrowserSettings`](/reference/telegram/functions/account/update-web-browser-settings/)

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
