---
title: "miniproto.client.Client.edit_message"
description: "Edit a message's text and optional media settings, returning the updated message."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.edit_message"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L795"
aliases: ["miniproto.Client.edit_message"]
module: "miniproto.client"
---

## `miniproto.client.Client.edit_message`

```python
edit_message(peer: Peer | str | int, message_id: int, text: str, *, parse_mode: str | None = None, entities: Iterable[object] | None = None, no_webpage: bool = False, invert_media: bool = False, media: object | None = None, reply_markup: object | None = None, schedule_date: int | None = None, quick_reply_shortcut_id: int | None = None, request_timeout: float | None = None, flood_sleep_threshold: int | None = None, retry: bool | None = None) -> Message
```

Edit a message's text and optional media settings, returning the updated message.

Explicit ``entities`` take precedence over ``parse_mode``. Request timeout, flood-wait and retry arguments follow ``invoke`` semantics.

**Parameters:**

- **peer** (<code>[Peer](#miniproto.types.Peer) | [str](#str) | [int](#int)</code>) – Conversation containing the target message.
- **message_id** (<code>[int](#int)</code>) – Telegram message ID to edit within ``peer``.
- **text** (<code>[str](#str)</code>) – Replacement source text.
- **parse_mode** (<code>[str](#str) | None</code>) – Optional parser for ``text`` when explicit entities are absent.
- **entities** (<code>[Iterable](#collections.abc.Iterable)[[object](#object)] | None</code>) – Optional low-level formatting entities that bypass ``parse_mode``.
- **no_webpage** (<code>[bool](#bool)</code>) – Whether Telegram should suppress an automatic webpage preview.
- **invert_media** (<code>[bool](#bool)</code>) – Whether Telegram should place existing media after the text when supported.
- **media** (<code>[object](#object) | None</code>) – Optional replacement raw input-media object.
- **reply_markup** (<code>[object](#object) | None</code>) – Optional replacement raw reply-markup object.
- **schedule_date** (<code>[int](#int) | None</code>) – Optional Unix timestamp for scheduled editing where Telegram permits it.
- **quick_reply_shortcut_id** (<code>[int](#int) | None</code>) – Optional quick-reply shortcut context identifier.
- **request_timeout** (<code>[float](#float) | None</code>) – Optional per-request timeout overriding client configuration.
- **flood_sleep_threshold** (<code>[int](#int) | None</code>) – Optional maximum flood-wait seconds to sleep automatically.
- **retry** (<code>[bool](#bool) | None</code>) – Whether to force or suppress retry eligibility.
