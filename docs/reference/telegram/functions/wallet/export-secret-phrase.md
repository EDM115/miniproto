---
title: "wallet.exportSecretPhrase"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "wallet.exportSecretPhrase"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0x9077c9ac"
---

# `wallet.exportSecretPhrase`

No description provided by the pinned schema.

## Signature

```tl
wallet.exportSecretPhrase#9077c9ac flags:# password:flags.0?InputCheckPasswordSRP = wallet.SecretPhraseParts;
```

## Result type

`wallet.SecretPhraseParts`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| password | flags.0?InputCheckPasswordSRP | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| password | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import WalletExportSecretPhrase
```

Public access: `miniproto.raw.functions.WalletExportSecretPhrase`.

## Class reference

```python
from miniproto.raw.functions import WalletExportSecretPhrase

# Refer to the raw request class without constructing it or calling Telegram
request_type = WalletExportSecretPhrase
```

## Result family

[`wallet.SecretPhraseParts`](/reference/telegram/types/results/wallet-secret-phrase-parts/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

[`InputCheckPasswordSRP`](/reference/telegram/types/results/input-check-password-srp/)
Known selected constructors: [`inputCheckPasswordEmpty`](/reference/telegram/types/base/input-check-password-empty/), [`inputCheckPasswordSRP`](/reference/telegram/types/base/input-check-password-srp/)

## Returned types

[`wallet.SecretPhraseParts`](/reference/telegram/types/results/wallet-secret-phrase-parts/)
Known selected constructors: [`wallet.secretPhraseParts`](/reference/telegram/types/wallet/secret-phrase-parts/)

## Related methods

[`account.deleteAccount`](/reference/telegram/functions/account/delete-account/), [`account.getPasswordSettings`](/reference/telegram/functions/account/get-password-settings/), [`account.getTmpPassword`](/reference/telegram/functions/account/get-tmp-password/), [`account.updatePasswordSettings`](/reference/telegram/functions/account/update-password-settings/), [`auth.checkPassword`](/reference/telegram/functions/auth/check-password/), [`messages.editChatCreator`](/reference/telegram/functions/messages/edit-chat-creator/), [`messages.getBotCallbackAnswer`](/reference/telegram/functions/messages/get-bot-callback-answer/), [`payments.getStarGiftWithdrawalUrl`](/reference/telegram/functions/payments/get-star-gift-withdrawal-url/), [`payments.getStarsRevenueWithdrawalUrl`](/reference/telegram/functions/payments/get-stars-revenue-withdrawal-url/), [`wallet.disableBackup`](/reference/telegram/functions/wallet/disable-backup/), [`wallet.replaceWallet`](/reference/telegram/functions/wallet/replace-wallet/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
