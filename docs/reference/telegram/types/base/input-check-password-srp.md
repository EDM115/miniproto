---
title: "inputCheckPasswordSRP"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "type"
qualified_name: "inputCheckPasswordSRP"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "base"
schema_source: "tdlib"
constructor_id: "0xd27ff082"
---

# `inputCheckPasswordSRP`

No description provided by the pinned schema.

## Signature

```tl
inputCheckPasswordSRP#d27ff082 srp_id:long A:bytes M1:bytes = InputCheckPasswordSRP;
```

## Result type

`InputCheckPasswordSRP`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| srp_id | long | — | — | No description provided by the pinned schema. |
| A | bytes | — | — | No description provided by the pinned schema. |
| M1 | bytes | — | — | No description provided by the pinned schema. |

## Python binding

```python
from miniproto.raw.types import InputCheckPasswordSRP
```

Public access: `miniproto.raw.types.InputCheckPasswordSRP`.

## Safe usage shape

```python
from miniproto.raw.types import InputCheckPasswordSRP

# Naming the raw constructor class is local only; it performs no I/O or network request.
constructor_type = InputCheckPasswordSRP
```

## Result family

[`InputCheckPasswordSRP`](/reference/telegram/types/results/input-check-password-srp/)

## Relationships

- Result family: [`InputCheckPasswordSRP`](/reference/telegram/types/results/input-check-password-srp/)
- Related constructors: [`inputCheckPasswordEmpty`](/reference/telegram/types/base/input-check-password-empty/)
- Accepted by: [`account.deleteAccount`](/reference/telegram/functions/account/delete-account/), [`account.getPasswordSettings`](/reference/telegram/functions/account/get-password-settings/), [`account.getTmpPassword`](/reference/telegram/functions/account/get-tmp-password/), [`account.updatePasswordSettings`](/reference/telegram/functions/account/update-password-settings/), [`auth.checkPassword`](/reference/telegram/functions/auth/check-password/), [`messages.editChatCreator`](/reference/telegram/functions/messages/edit-chat-creator/), [`messages.getBotCallbackAnswer`](/reference/telegram/functions/messages/get-bot-callback-answer/), [`payments.getStarGiftWithdrawalUrl`](/reference/telegram/functions/payments/get-star-gift-withdrawal-url/), [`payments.getStarsRevenueWithdrawalUrl`](/reference/telegram/functions/payments/get-stars-revenue-withdrawal-url/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 229 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=78; core_only_count=18; overlap_count=2285; tdlib_only_count=195
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2470; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
