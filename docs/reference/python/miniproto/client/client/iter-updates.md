---
title: "miniproto.client.Client.iter_updates"
description: "Yield updates accepted by the update manager's public FIFO queue."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.iter_updates"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L1811"
aliases: ["miniproto.Client.iter_updates"]
module: "miniproto.client"
---

## `miniproto.client.Client.iter_updates`

```python
iter_updates() -> AsyncIterator[Update]
```

Yield updates accepted by the update manager's public FIFO queue.

Multiple iterators compete for items from the same queue. Raw processing persists cursor and duplicate state before delivery. Gap-recovered events may precede the live update that triggered recovery.

**Yields:**

- <code>[AsyncIterator](#collections.abc.AsyncIterator)[[Update](#miniproto.types.Update)]</code> – Public ``Update`` instances, subject to configured overflow and duplicate suppression.

<details class="lifecycle" open markdown="1">
<summary>Lifecycle</summary>

``disconnect`` does not end or wake this iterator. Cancel a waiting consumer yourself.

</details>
