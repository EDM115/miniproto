---
title: "miniproto.client.Client.wait_for_updates"
description: "Wait for the current update-processing task to stop or fail"
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.wait_for_updates"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L1957"
aliases: ["miniproto.Client.wait_for_updates"]
module: "miniproto.client"
---

## `miniproto.client.Client.wait_for_updates`

```python
wait_for_updates() -> None
```

Wait for the current update-processing task to stop or fail

Call after ``connect`` with updates enabled and before ``disconnect``. A normal disconnect completes the wait. Queue, handler, storage and recovery failures propagate as soon as the task fails. Cancelling this wait leaves update processing running. A later ``connect`` can start a new task after the failure's cause is resolved and requires a new wait, persisted events are not automatically replayed.

**Raises:**

- <code>[RuntimeError](#RuntimeError)</code> – If no update task has been started or it has already been stopped.
- <code>[Exception](#Exception)</code> – The current update task's processing failure.
