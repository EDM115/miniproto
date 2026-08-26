---
title: "miniproto.client.Client.delete_messages"
description: "Delete one or more messages and return Telegram's raw affected-history result."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.delete_messages"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L872"
aliases: ["miniproto.Client.delete_messages"]
module: "miniproto.client"
---

## `miniproto.client.Client.delete_messages`

```python
delete_messages(peer: Peer | str | int, message_ids: int | Iterable[int], *, revoke: bool = True, request_timeout: float | None = None, flood_sleep_threshold: int | None = None, retry: bool | None = None) -> object
```

Delete one or more messages and return Telegram's raw affected-history result.

Channel messages use Telegram's channel deletion method; other peers use the regular method and honor ``revoke``. Empty ``message_ids`` are rejected.

**Parameters:**

- **peer** (<code>[Peer](#miniproto.types.Peer) | [str](#str) | [int](#int)</code>) – Conversation containing the messages.
- **message_ids** (<code>[int](#int) | [Iterable](#collections.abc.Iterable)[[int](#int)]</code>) – One message ID or an iterable of message IDs to delete.
- **revoke** (<code>[bool](#bool)</code>) – Whether non-channel deletions should be revoked for other participants, defaulting to ``True``.
- **request_timeout** (<code>[float](#float) | None</code>) – Optional per-request timeout overriding client configuration.
- **flood_sleep_threshold** (<code>[int](#int) | None</code>) – Optional maximum flood-wait seconds to sleep automatically.
- **retry** (<code>[bool](#bool) | None</code>) – Whether to force or suppress retry eligibility.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``message_ids`` is empty.
