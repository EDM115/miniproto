---
title: "Telegram functions: payments"
description: "Layer 229 index of 65 canonical Telegram functions in the payments namespace from tdlib."
generated: true
editUrl: false
language: "telegram"
kind: "index"
qualified_name: "telegram.functions.payments"
source_path: "tools/schema/schema.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/schema.json"
namespace: "payments"
schema_source: "tdlib"
---

## Layer 229 payments functions

Selected canonical functions in this namespace: 65.

## Declarations

- [`payments.applyGiftCode`](/reference/telegram/functions/payments/apply-gift-code/): `Updates`
- [`payments.assignAppStoreTransaction`](/reference/telegram/functions/payments/assign-app-store-transaction/): `Updates`
- [`payments.assignPlayMarketTransaction`](/reference/telegram/functions/payments/assign-play-market-transaction/): `Updates`
- [`payments.botCancelStarsSubscription`](/reference/telegram/functions/payments/bot-cancel-stars-subscription/): `Bool`
- [`payments.canPurchaseStore`](/reference/telegram/functions/payments/can-purchase-store/): `Bool`
- [`payments.changeStarsSubscription`](/reference/telegram/functions/payments/change-stars-subscription/): `Bool`
- [`payments.checkCanSendGift`](/reference/telegram/functions/payments/check-can-send-gift/): `payments.CheckCanSendGiftResult`
- [`payments.checkGiftCode`](/reference/telegram/functions/payments/check-gift-code/): `payments.CheckedGiftCode`
- [`payments.clearSavedInfo`](/reference/telegram/functions/payments/clear-saved-info/): `Bool`
- [`payments.connectStarRefBot`](/reference/telegram/functions/payments/connect-star-ref-bot/): `payments.ConnectedStarRefBots`
- [`payments.convertStarGift`](/reference/telegram/functions/payments/convert-star-gift/): `Bool`
- [`payments.craftStarGift`](/reference/telegram/functions/payments/craft-star-gift/): `Updates`
- [`payments.createStarGiftCollection`](/reference/telegram/functions/payments/create-star-gift-collection/): `StarGiftCollection`
- [`payments.deleteStarGiftCollection`](/reference/telegram/functions/payments/delete-star-gift-collection/): `Bool`
- [`payments.editConnectedStarRefBot`](/reference/telegram/functions/payments/edit-connected-star-ref-bot/): `payments.ConnectedStarRefBots`
- [`payments.exportInvoice`](/reference/telegram/functions/payments/export-invoice/): `payments.ExportedInvoice`
- [`payments.fulfillStarsSubscription`](/reference/telegram/functions/payments/fulfill-stars-subscription/): `Bool`
- [`payments.getBankCardData`](/reference/telegram/functions/payments/get-bank-card-data/): `payments.BankCardData`
- [`payments.getConnectedStarRefBot`](/reference/telegram/functions/payments/get-connected-star-ref-bot/): `payments.ConnectedStarRefBots`
- [`payments.getConnectedStarRefBots`](/reference/telegram/functions/payments/get-connected-star-ref-bots/): `payments.ConnectedStarRefBots`
- [`payments.getCraftStarGifts`](/reference/telegram/functions/payments/get-craft-star-gifts/): `payments.SavedStarGifts`
- [`payments.getGiveawayInfo`](/reference/telegram/functions/payments/get-giveaway-info/): `payments.GiveawayInfo`
- [`payments.getPaymentForm`](/reference/telegram/functions/payments/get-payment-form/): `payments.PaymentForm`
- [`payments.getPaymentReceipt`](/reference/telegram/functions/payments/get-payment-receipt/): `payments.PaymentReceipt`
- [`payments.getPremiumGiftCodeOptions`](/reference/telegram/functions/payments/get-premium-gift-code-options/): `Vector<PremiumGiftCodeOption>`
- [`payments.getResaleStarGifts`](/reference/telegram/functions/payments/get-resale-star-gifts/): `payments.ResaleStarGifts`
- [`payments.getSavedInfo`](/reference/telegram/functions/payments/get-saved-info/): `payments.SavedInfo`
- [`payments.getSavedStarGift`](/reference/telegram/functions/payments/get-saved-star-gift/): `payments.SavedStarGifts`
- [`payments.getSavedStarGifts`](/reference/telegram/functions/payments/get-saved-star-gifts/): `payments.SavedStarGifts`
- [`payments.getStarGiftActiveAuctions`](/reference/telegram/functions/payments/get-star-gift-active-auctions/): `payments.StarGiftActiveAuctions`
- [`payments.getStarGiftAuctionAcquiredGifts`](/reference/telegram/functions/payments/get-star-gift-auction-acquired-gifts/): `payments.StarGiftAuctionAcquiredGifts`
- [`payments.getStarGiftAuctionState`](/reference/telegram/functions/payments/get-star-gift-auction-state/): `payments.StarGiftAuctionState`
- [`payments.getStarGiftCollections`](/reference/telegram/functions/payments/get-star-gift-collections/): `payments.StarGiftCollections`
- [`payments.getStarGiftUpgradeAttributes`](/reference/telegram/functions/payments/get-star-gift-upgrade-attributes/): `payments.StarGiftUpgradeAttributes`
- [`payments.getStarGiftUpgradePreview`](/reference/telegram/functions/payments/get-star-gift-upgrade-preview/): `payments.StarGiftUpgradePreview`
- [`payments.getStarGiftWithdrawalUrl`](/reference/telegram/functions/payments/get-star-gift-withdrawal-url/): `payments.StarGiftWithdrawalUrl`
- [`payments.getStarGifts`](/reference/telegram/functions/payments/get-star-gifts/): `payments.StarGifts`
- [`payments.getStarsGiftOptions`](/reference/telegram/functions/payments/get-stars-gift-options/): `Vector<StarsGiftOption>`
- [`payments.getStarsGiveawayOptions`](/reference/telegram/functions/payments/get-stars-giveaway-options/): `Vector<StarsGiveawayOption>`
- [`payments.getStarsRevenueAdsAccountUrl`](/reference/telegram/functions/payments/get-stars-revenue-ads-account-url/): `payments.StarsRevenueAdsAccountUrl`
- [`payments.getStarsRevenueStats`](/reference/telegram/functions/payments/get-stars-revenue-stats/): `payments.StarsRevenueStats`
- [`payments.getStarsRevenueWithdrawalUrl`](/reference/telegram/functions/payments/get-stars-revenue-withdrawal-url/): `payments.StarsRevenueWithdrawalUrl`
- [`payments.getStarsStatus`](/reference/telegram/functions/payments/get-stars-status/): `payments.StarsStatus`
- [`payments.getStarsSubscriptions`](/reference/telegram/functions/payments/get-stars-subscriptions/): `payments.StarsStatus`
- [`payments.getStarsTopupOptions`](/reference/telegram/functions/payments/get-stars-topup-options/): `Vector<StarsTopupOption>`
- [`payments.getStarsTransactions`](/reference/telegram/functions/payments/get-stars-transactions/): `payments.StarsStatus`
- [`payments.getStarsTransactionsByID`](/reference/telegram/functions/payments/get-stars-transactions-by-id/): `payments.StarsStatus`
- [`payments.getSuggestedStarRefBots`](/reference/telegram/functions/payments/get-suggested-star-ref-bots/): `payments.SuggestedStarRefBots`
- [`payments.getUniqueStarGift`](/reference/telegram/functions/payments/get-unique-star-gift/): `payments.UniqueStarGift`
- [`payments.getUniqueStarGiftValueInfo`](/reference/telegram/functions/payments/get-unique-star-gift-value-info/): `payments.UniqueStarGiftValueInfo`
- [`payments.launchPrepaidGiveaway`](/reference/telegram/functions/payments/launch-prepaid-giveaway/): `Updates`
- [`payments.refundStarsCharge`](/reference/telegram/functions/payments/refund-stars-charge/): `Updates`
- [`payments.reorderStarGiftCollections`](/reference/telegram/functions/payments/reorder-star-gift-collections/): `Bool`
- [`payments.resolveStarGiftOffer`](/reference/telegram/functions/payments/resolve-star-gift-offer/): `Updates`
- [`payments.saveStarGift`](/reference/telegram/functions/payments/save-star-gift/): `Bool`
- [`payments.sendPaymentForm`](/reference/telegram/functions/payments/send-payment-form/): `payments.PaymentResult`
- [`payments.sendStarGiftOffer`](/reference/telegram/functions/payments/send-star-gift-offer/): `Updates`
- [`payments.sendStarsForm`](/reference/telegram/functions/payments/send-stars-form/): `payments.PaymentResult`
- [`payments.toggleChatStarGiftNotifications`](/reference/telegram/functions/payments/toggle-chat-star-gift-notifications/): `Bool`
- [`payments.toggleStarGiftsPinnedToTop`](/reference/telegram/functions/payments/toggle-star-gifts-pinned-to-top/): `Bool`
- [`payments.transferStarGift`](/reference/telegram/functions/payments/transfer-star-gift/): `Updates`
- [`payments.updateStarGiftCollection`](/reference/telegram/functions/payments/update-star-gift-collection/): `StarGiftCollection`
- [`payments.updateStarGiftPrice`](/reference/telegram/functions/payments/update-star-gift-price/): `Updates`
- [`payments.upgradeStarGift`](/reference/telegram/functions/payments/upgrade-star-gift/): `Updates`
- [`payments.validateRequestedInfo`](/reference/telegram/functions/payments/validate-requested-info/): `payments.ValidatedRequestedInfo`
