---
title: "miniproto.updates.state.UpdateCursor.channel_cursor"
description: "Return the channel cursor or a zero-PTS cursor when this channel is not known."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.updates.state.UpdateCursor.channel_cursor"
source_path: "src/miniproto/updates/state.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/state.py#L184"
aliases: ["miniproto.updates.UpdateCursor.channel_cursor"]
module: "miniproto.updates.state"
---

## `miniproto.updates.state.UpdateCursor.channel_cursor`

```python
channel_cursor(channel_id: int) -> ChannelUpdateCursor
```

Return the channel cursor or a zero-PTS cursor when this channel is not known.

**Parameters:**

- **channel_id** (<code>[int](#int)</code>) – Telegram channel identifier to look up.
