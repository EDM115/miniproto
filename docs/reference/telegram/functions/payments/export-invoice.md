---
title: "payments.exportInvoice"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "payments.exportInvoice"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
layer: 228
schema_source: "tdlib"
constructor_id: "0x0f91b065"
---

# `payments.exportInvoice`

No description provided by the pinned schema.

## Signature

```tl
payments.exportInvoice#0f91b065 invoice_media:InputMedia = payments.ExportedInvoice;
```

## Result type

`payments.ExportedInvoice`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| invoice_media | InputMedia | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.functions import PaymentsExportInvoice
```

Public access: `miniproto.raw.functions.PaymentsExportInvoice`.

## Safe usage shape

```python
from miniproto.raw.functions import PaymentsExportInvoice

# Naming the raw request class is local only; it performs no I/O or network request.
request_type = PaymentsExportInvoice
```

## Result family

[`payments.ExportedInvoice`](/reference/telegram/types/results/payments-exported-invoice/)

## RPC errors

| Code | Error | Description |
| ---: | --- | --- |
| 400 | [`BUSINESS_CONNECTION_INVALID`](/reference/telegram/errors/business-connection-invalid/) | The `connection_id` passed to the wrapping [invokeWithBusinessConnection](https://core.telegram.org/api/business) call is invalid. |
| 400 | [`BUSINESS_CONNECTION_NOT_ALLOWED`](/reference/telegram/errors/business-connection-not-allowed/) | This method was invoked over a business connection using [invokeWithBusinessConnection](https://core.telegram.org/api/business#connected-bots), but either (1) we're a user, and users cannot invoke methods over a business connection; (2) we're a bot, but business mode was disabled in @botfather or (3); we're a bot, but this method cannot be invoked over a business connection. |
| 400 | [`CURRENCY_TOTAL_AMOUNT_INVALID`](/reference/telegram/errors/currency-total-amount-invalid/) | The total amount of all prices is invalid. |
| 400 | [`INVOICE_PAYLOAD_INVALID`](/reference/telegram/errors/invoice-payload-invalid/) | The specified invoice payload is invalid. |
| 400 | [`MEDIA_INVALID`](/reference/telegram/errors/media-invalid/) | Media invalid. |
| 400 | [`PAYMENT_PROVIDER_INVALID`](/reference/telegram/errors/payment-provider-invalid/) | The specified payment provider is invalid. |
| 400 | [`STARS_INVOICE_INVALID`](/reference/telegram/errors/stars-invoice-invalid/) | The specified Telegram Star invoice is invalid. |
| 400 | [`USER_BOT_REQUIRED`](/reference/telegram/errors/user-bot-required/) | This method can only be called by a bot. |
| 400 | [`WEBDOCUMENT_MIME_INVALID`](/reference/telegram/errors/webdocument-mime-invalid/) | Invalid webdocument mime type provided. |
| 400 | [`WEBDOCUMENT_URL_EMPTY`](/reference/telegram/errors/webdocument-url-empty/) | The passed web document URL is empty. |
| 401 | [`AUTH_KEY_UNREGISTERED`](/reference/telegram/errors/auth-key-unregistered/) | The specified authorization key is not registered in the system (for example, a PFS temporary key has expired). |

## Accepted types

[`InputMedia`](/reference/telegram/types/results/input-media/)
Known selected constructors: [`inputMediaContact`](/reference/telegram/types/base/input-media-contact/), [`inputMediaDice`](/reference/telegram/types/base/input-media-dice/), [`inputMediaDocument`](/reference/telegram/types/base/input-media-document/), [`inputMediaDocumentExternal`](/reference/telegram/types/base/input-media-document-external/), [`inputMediaEmpty`](/reference/telegram/types/base/input-media-empty/), [`inputMediaGame`](/reference/telegram/types/base/input-media-game/), [`inputMediaGeoLive`](/reference/telegram/types/base/input-media-geo-live/), [`inputMediaGeoPoint`](/reference/telegram/types/base/input-media-geo-point/), [`inputMediaInvoice`](/reference/telegram/types/base/input-media-invoice/), [`inputMediaPaidMedia`](/reference/telegram/types/base/input-media-paid-media/), [`inputMediaPhoto`](/reference/telegram/types/base/input-media-photo/), [`inputMediaPhotoExternal`](/reference/telegram/types/base/input-media-photo-external/), [`inputMediaPoll`](/reference/telegram/types/base/input-media-poll/), [`inputMediaStakeDice`](/reference/telegram/types/base/input-media-stake-dice/), [`inputMediaStory`](/reference/telegram/types/base/input-media-story/), [`inputMediaTodo`](/reference/telegram/types/base/input-media-todo/), [`inputMediaUploadedDocument`](/reference/telegram/types/base/input-media-uploaded-document/), [`inputMediaUploadedPhoto`](/reference/telegram/types/base/input-media-uploaded-photo/), [`inputMediaVenue`](/reference/telegram/types/base/input-media-venue/), [`inputMediaWebPage`](/reference/telegram/types/base/input-media-web-page/)

## Returned types

[`payments.ExportedInvoice`](/reference/telegram/types/results/payments-exported-invoice/)
Known selected constructors: [`payments.exportedInvoice`](/reference/telegram/types/payments/exported-invoice/)

## Related methods

[`bots.addPreviewMedia`](/reference/telegram/functions/bots/add-preview-media/), [`bots.deletePreviewMedia`](/reference/telegram/functions/bots/delete-preview-media/), [`bots.editPreviewMedia`](/reference/telegram/functions/bots/edit-preview-media/), [`bots.reorderPreviewMedias`](/reference/telegram/functions/bots/reorder-preview-medias/), [`ephemeral.editMessage`](/reference/telegram/functions/ephemeral/edit-message/), [`ephemeral.sendMessage`](/reference/telegram/functions/ephemeral/send-message/), [`messages.editInlineBotMessage`](/reference/telegram/functions/messages/edit-inline-bot-message/), [`messages.editMessage`](/reference/telegram/functions/messages/edit-message/), [`messages.saveDraft`](/reference/telegram/functions/messages/save-draft/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.uploadImportedMedia`](/reference/telegram/functions/messages/upload-imported-media/), [`messages.uploadMedia`](/reference/telegram/functions/messages/upload-media/), [`stories.editStory`](/reference/telegram/functions/stories/edit-story/), [`stories.sendStory`](/reference/telegram/functions/stories/send-story/)

## Availability evidence

- bot only
- business supported

## Provenance

- layer: 228
- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
