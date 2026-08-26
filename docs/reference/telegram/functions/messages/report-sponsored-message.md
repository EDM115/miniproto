---
title: "messages.reportSponsoredMessage"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "messages.reportSponsoredMessage"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "messages"
schema_source: "tdlib"
constructor_id: "0x12cbf0c4"
---

# `messages.reportSponsoredMessage`

No description provided by the pinned schema.

## Signature

```tl
messages.reportSponsoredMessage#12cbf0c4 random_id:bytes option:bytes = channels.SponsoredMessageReportResult;
```

## Result type

`channels.SponsoredMessageReportResult`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| random_id | bytes | — | — | No description provided by the pinned schema. |
| option | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import MessagesReportSponsoredMessage
```

Public access: `miniproto.raw.functions.MessagesReportSponsoredMessage`.

## Safe usage shape

```python
from miniproto.raw.functions import MessagesReportSponsoredMessage

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = MessagesReportSponsoredMessage
```

## Result family

[`channels.SponsoredMessageReportResult`](/reference/telegram/types/results/channels-sponsored-message-report-result/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

No non-primitive type relationships were found.


## Returned types

[`channels.SponsoredMessageReportResult`](/reference/telegram/types/results/channels-sponsored-message-report-result/)
Known selected constructors: [`channels.sponsoredMessageReportResultAdsHidden`](/reference/telegram/types/channels/sponsored-message-report-result-ads-hidden/), [`channels.sponsoredMessageReportResultChooseOption`](/reference/telegram/types/channels/sponsored-message-report-result-choose-option/), [`channels.sponsoredMessageReportResultReported`](/reference/telegram/types/channels/sponsored-message-report-result-reported/)

## Availability evidence

- user only

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
