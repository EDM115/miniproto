---
title: "miniproto.messages"
description: "Parse lightweight message markup and normalize Telegram message responses."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.messages"
source_path: "src/miniproto/messages.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/messages.py"
module: "miniproto.messages"
---

## `miniproto.messages`

Parse lightweight message markup and normalize Telegram message responses.

## Public objects

- [`MessageParseMode`](./messageparsemode/) — Public attribute `miniproto.messages.MessageParseMode`.
- [`ParsedMessageText`](./parsedmessagetext/) — Rendered message text and UTF-16-indexed MTProto entities.
- [`parse_message_text`](./parse-message-text/) — Render the supported lightweight Markdown delimiters into MTProto entities.
- [`make_random_id`](./make-random-id/) — Return a non-zero random 63-bit client message identifier.
- [`message_from_send_result`](./message-from-send-result/) — Normalize a send response, retaining supplied values when Telegram omits a message.
- [`message_from_raw`](./message-from-raw/) — Convert a raw Telegram message using ``fallback_peer`` for unknown peer forms.
- [`message_from_update_result`](./message-from-update-result/) — Normalize an update response or create a fallback message when none is present.
- [`messages_from_history_result`](./messages-from-history-result/) — Convert only concrete raw messages from a history result in source order.
