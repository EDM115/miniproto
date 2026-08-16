---
title: "PREMIUM_ACCOUNT_REQUIRED"
description: "A premium account is required to execute this action."
generated: true
editUrl: false
language: "telegram"
kind: "error"
qualified_name: "403:PREMIUM_ACCOUNT_REQUIRED"
source_path: "tools/schema/rpc-errors.json"
source_url: "https://github.com/EDM115/miniproto/blob/master/tools/schema/rpc-errors.json"
namespace: "errors"
layer: 228
schema_source: "tdlib"
---

# `PREMIUM_ACCOUNT_REQUIRED`

A premium account is required to execute this action.

## Error details

- code: 403
- parameterized: no
- mapped methods: [`account.createBusinessChatLink`](/reference/telegram/functions/account/create-business-chat-link/), [`account.editBusinessChatLink`](/reference/telegram/functions/account/edit-business-chat-link/), [`account.setGlobalPrivacySettings`](/reference/telegram/functions/account/set-global-privacy-settings/), [`account.updateColor`](/reference/telegram/functions/account/update-color/), [`account.updateEmojiStatus`](/reference/telegram/functions/account/update-emoji-status/), `channels.createForumTopic` (not in selected Layer 228 schema), [`channels.searchPosts`](/reference/telegram/functions/channels/search-posts/), [`messages.checkQuickReplyShortcut`](/reference/telegram/functions/messages/check-quick-reply-shortcut/), [`messages.createForumTopic`](/reference/telegram/functions/messages/create-forum-topic/), [`messages.editQuickReplyShortcut`](/reference/telegram/functions/messages/edit-quick-reply-shortcut/), [`messages.forwardMessages`](/reference/telegram/functions/messages/forward-messages/), [`messages.reorderQuickReplies`](/reference/telegram/functions/messages/reorder-quick-replies/), [`messages.sendMedia`](/reference/telegram/functions/messages/send-media/), [`messages.sendMessage`](/reference/telegram/functions/messages/send-message/), [`messages.sendQuickReplyMessages`](/reference/telegram/functions/messages/send-quick-reply-messages/), [`messages.sendReaction`](/reference/telegram/functions/messages/send-reaction/), [`messages.toggleDialogFilterTags`](/reference/telegram/functions/messages/toggle-dialog-filter-tags/), [`messages.transcribeAudio`](/reference/telegram/functions/messages/transcribe-audio/), [`messages.updateSavedReactionTag`](/reference/telegram/functions/messages/update-saved-reaction-tag/)

## Python error class

```python
from miniproto.errors import PremiumAccountRequired
```

Public access: `miniproto.errors.PremiumAccountRequired`.

## Provenance

- layer: 228
- structural source: `tdlib`
- RPC error source: https://core.telegram.org/api/errors
- prose merge precedence: TDLib → Telegram Desktop → Core JSON
- source note: Canonical structure is the pinned TDLib telegram_api.tl; Layer 228 comes only from the matching Telegram Desktop end-of-file marker; core.telegram.org inputs enrich documentation and RPC error metadata without overriding structure.

## Source-diff notes

- tdlib_vs_core: changed_count=68; core_only_count=1; overlap_count=2302; tdlib_only_count=158
- tdlib_vs_tdesktop: changed_count=0; overlap_count=2448; tdesktop_only=null; tdlib_only=accessPointRule, ephemeral.editMessage, help.configSimple, inputPeerPhotoFileLocationLegacy, inputStickerSetThumbLegacy, invokeWithApnsSecretPrefix, invokeWithBusinessConnectionPrefix, invokeWithGooglePlayIntegrityPrefix, invokeWithReCaptchaPrefix, ipPort, ipPortSecret, updateEphemeralBotCallbackQuery
