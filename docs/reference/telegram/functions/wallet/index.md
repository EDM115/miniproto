---
title: "Telegram functions: wallet"
description: "Layer 230 index of 25 canonical Telegram functions in the wallet namespace from tdlib."
generated: true
editUrl: false
language: "telegram"
kind: "index"
qualified_name: "telegram.functions.wallet"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "wallet"
schema_source: "tdlib"
---

## Layer 230 wallet functions

Selected canonical functions in this namespace: 25.

## Declarations

- [`wallet.disableBackup`](/reference/telegram/functions/wallet/disable-backup/): `WalletState`
- [`wallet.enableBackup`](/reference/telegram/functions/wallet/enable-backup/): `WalletState`
- [`wallet.exportSecretPhrase`](/reference/telegram/functions/wallet/export-secret-phrase/): `wallet.SecretPhraseParts`
- [`wallet.fetchEncryptedSecretPhrasePart`](/reference/telegram/functions/wallet/fetch-encrypted-secret-phrase-part/): `wallet.EncryptedSecretPhrasePart`
- [`wallet.getBackupHolderDcs`](/reference/telegram/functions/wallet/get-backup-holder-dcs/): `Vector<wallet.HolderDc>`
- [`wallet.getExistingWaltBalance`](/reference/telegram/functions/wallet/get-existing-walt-balance/): `wallet.ExistingBalance`
- [`wallet.getGaslessInfo`](/reference/telegram/functions/wallet/get-gasless-info/): `Updates`
- [`wallet.getNfts`](/reference/telegram/functions/wallet/get-nfts/): `wallet.NftItems`
- [`wallet.getProofChallenge`](/reference/telegram/functions/wallet/get-proof-challenge/): `wallet.ProofChallenge`
- [`wallet.getState`](/reference/telegram/functions/wallet/get-state/): `WalletState`
- [`wallet.getTransactions`](/reference/telegram/functions/wallet/get-transactions/): `wallet.Transactions`
- [`wallet.getTransactionsByIDs`](/reference/telegram/functions/wallet/get-transactions-by-ids/): `wallet.Transactions`
- [`wallet.getTransactionsByMsgHash`](/reference/telegram/functions/wallet/get-transactions-by-msg-hash/): `wallet.Transactions`
- [`wallet.getUserAddresses`](/reference/telegram/functions/wallet/get-user-addresses/): `wallet.UserAddresses`
- [`wallet.replaceWallet`](/reference/telegram/functions/wallet/replace-wallet/): `WalletState`
- [`wallet.sendTransfer`](/reference/telegram/functions/wallet/send-transfer/): `Updates`
- [`wallet.tonConnectClaimRequest`](/reference/telegram/functions/wallet/ton-connect-claim-request/): `Bool`
- [`wallet.tonConnectCloseSession`](/reference/telegram/functions/wallet/ton-connect-close-session/): `Bool`
- [`wallet.tonConnectCreateSession`](/reference/telegram/functions/wallet/ton-connect-create-session/): `TonConnectSession`
- [`wallet.tonConnectGetPending`](/reference/telegram/functions/wallet/ton-connect-get-pending/): `wallet.TonConnectPending`
- [`wallet.tonConnectGetSessions`](/reference/telegram/functions/wallet/ton-connect-get-sessions/): `wallet.TonConnectSessions`
- [`wallet.tonConnectNextEventId`](/reference/telegram/functions/wallet/ton-connect-next-event-id/): `TonConnectNextEventId`
- [`wallet.tonConnectRegisterKey`](/reference/telegram/functions/wallet/ton-connect-register-key/): `wallet.TonConnectChallenge`
- [`wallet.tonConnectSubmitConnectResult`](/reference/telegram/functions/wallet/ton-connect-submit-connect-result/): `Bool`
- [`wallet.tonConnectSubmitResponse`](/reference/telegram/functions/wallet/ton-connect-submit-response/): `Bool`
