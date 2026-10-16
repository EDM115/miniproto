---
title: "wallet.replaceWallet"
description: "No description provided by the pinned schema."
generated: true
editUrl: false
language: "telegram"
kind: "function"
qualified_name: "wallet.replaceWallet"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
constructor_id: "0xd8c72eec"
---

# `wallet.replaceWallet`

No description provided by the pinned schema.

## Signature

```tl
wallet.replaceWallet#d8c72eec flags:# wallet:InputWalletReplacement password:flags.0?InputCheckPasswordSRP = WalletState;
```

## Result type

`WalletState`

## Parameters

| Name | Type | Flag | Default | Description |
| --- | --- | --- | --- | --- |
| flags | # | flag word | — | No description provided by the pinned schema. |
| wallet | InputWalletReplacement | — | — | No description provided by the pinned schema. |
| password | flags.0?InputCheckPasswordSRP | flags.0 | — | No description provided by the pinned schema. |

## Flags

| Parameter | Bit | Meaning |
| --- | ---: | --- |
| password | 0 | Controlled by `flags`; present when this bit is set. |

## Python binding

```python
from miniproto.raw.functions import WalletReplaceWallet
```

Public access: `miniproto.raw.functions.WalletReplaceWallet`.

## Class reference

```python
from miniproto.raw.functions import WalletReplaceWallet

# Refer to the raw request class without constructing it or calling Telegram
request_type = WalletReplaceWallet
```

## Result family

[`WalletState`](/reference/telegram/types/results/wallet-state/)

## RPC errors

No RPC errors are mapped to this method by the pinned error database.

## Accepted types

[`InputCheckPasswordSRP`](/reference/telegram/types/results/input-check-password-srp/), [`InputWalletReplacement`](/reference/telegram/types/results/input-wallet-replacement/)
Known selected constructors: [`inputCheckPasswordEmpty`](/reference/telegram/types/base/input-check-password-empty/), [`inputCheckPasswordSRP`](/reference/telegram/types/base/input-check-password-srp/), [`inputWalletImported`](/reference/telegram/types/base/input-wallet-imported/), [`inputWalletNew`](/reference/telegram/types/base/input-wallet-new/)

## Returned types

[`WalletState`](/reference/telegram/types/results/wallet-state/)
Known selected constructors: [`walletState`](/reference/telegram/types/base/wallet-state/), [`walletStateEmpty`](/reference/telegram/types/base/wallet-state-empty/)

## Related methods

[`account.deleteAccount`](/reference/telegram/functions/account/delete-account/), [`account.getPasswordSettings`](/reference/telegram/functions/account/get-password-settings/), [`account.getTmpPassword`](/reference/telegram/functions/account/get-tmp-password/), [`account.updatePasswordSettings`](/reference/telegram/functions/account/update-password-settings/), [`auth.checkPassword`](/reference/telegram/functions/auth/check-password/), [`messages.editChatCreator`](/reference/telegram/functions/messages/edit-chat-creator/), [`messages.getBotCallbackAnswer`](/reference/telegram/functions/messages/get-bot-callback-answer/), [`payments.getStarGiftWithdrawalUrl`](/reference/telegram/functions/payments/get-star-gift-withdrawal-url/), [`payments.getStarsRevenueWithdrawalUrl`](/reference/telegram/functions/payments/get-stars-revenue-withdrawal-url/), [`wallet.disableBackup`](/reference/telegram/functions/wallet/disable-backup/), [`wallet.enableBackup`](/reference/telegram/functions/wallet/enable-backup/), [`wallet.exportSecretPhrase`](/reference/telegram/functions/wallet/export-secret-phrase/), [`wallet.getState`](/reference/telegram/functions/wallet/get-state/)

## Provenance

- structural source: `tdlib`
- canonical schema: https://raw.githubusercontent.com/tdlib/td/refs/heads/master/td/generate/scheme/telegram_api.tl
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 230 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=55; core_only_count=18; overlap_count=2338; tdlib_only_count=225
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2553; tdesktop_only=null; tdlib_only=accessPointRule, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret
