---
title: "miniproto.updates.manager.UpdateManager.iter_updates"
description: "Yield normalized public updates from the FIFO queue until the consumer is cancelled."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.updates.manager.UpdateManager.iter_updates"
source_path: "src/miniproto/updates/manager.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/manager.py#L233"
aliases: ["miniproto.updates.UpdateManager.iter_updates"]
module: "miniproto.updates.manager"
---

## `miniproto.updates.manager.UpdateManager.iter_updates`

```python
iter_updates() -> AsyncGenerator[Update]
```

Yield normalized public updates from the FIFO queue until the consumer is cancelled.

The iterator becomes active on its first ``anext`` and stays active until closed or cancelled, including while its consumer processes an event. Multiple iterators compete for the same queue. Callback-only events emitted before activation are not retained, while clients without handlers retain the bounded pre-iteration backlog.

**Yields:**

- <code>[AsyncGenerator](#collections.abc.AsyncGenerator)[[Update](#miniproto.types.Update)]</code> – Updates accepted by the public queue. Dropped updates and items never processed due to drainer cancellation are not yielded.

<details class="cancellation" open markdown="1">
<summary>Cancellation</summary>

Stopping the manager does not end this iterator or wake a waiting consumer.

</details>
