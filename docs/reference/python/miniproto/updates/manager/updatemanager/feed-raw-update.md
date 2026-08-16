---
title: "miniproto.updates.manager.UpdateManager.feed_raw_update"
description: "Offer a raw Telegram update to the bounded background-processing queue."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.updates.manager.UpdateManager.feed_raw_update"
source_path: "src/miniproto/updates/manager.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/manager.py#L135"
aliases: ["miniproto.updates.UpdateManager.feed_raw_update"]
module: "miniproto.updates.manager"
---

## `miniproto.updates.manager.UpdateManager.feed_raw_update`

```python
feed_raw_update(raw_update: object) -> None
```

Offer a raw Telegram update to the bounded background-processing queue.

Queue-full behavior is controlled by ``ClientConfig.update_queue_overflow``: ``"raise"`` propagates ``asyncio.QueueFull``, ``"drop_newest"`` discards this update, and ``"drop_oldest"`` replaces the oldest queued update.

**Parameters:**

- **raw_update** (<code>[object](#object)</code>) – Decoded Telegram update or update-container object to enqueue.
