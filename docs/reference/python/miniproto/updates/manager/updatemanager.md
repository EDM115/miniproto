---
title: "miniproto.updates.manager.UpdateManager"
description: "Process Telegram updates into public events while persisting recovery state."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.updates.manager.UpdateManager"
source_path: "src/miniproto/updates/manager.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/updates/manager.py#L51"
aliases: ["miniproto.updates.UpdateManager"]
module: "miniproto.updates.manager"
---

## `miniproto.updates.manager.UpdateManager`

```python
UpdateManager(config: ClientConfig, storage: SessionStorage, invoke: UpdateInvoker) -> None
```

Process Telegram updates into public events while persisting recovery state.

**Parameters:**

- **config** (<code>[ClientConfig](#miniproto.config.ClientConfig)</code>) – Client configuration defining queue capacities, overflow policy, and duplicate-window size.
- **storage** (<code>[SessionStorage](#miniproto.session.storage.SessionStorage)</code>) – Session storage used to load and atomically persist update cursors and discovered entities.
- **invoke** (<code>[UpdateInvoker](#miniproto.updates.manager.UpdateInvoker)</code>) – Async raw-RPC invoker used for ``updates.getState`` and difference recovery.

<details class="lifecycle" open markdown="1">
<summary>Lifecycle</summary>

``start`` restores state and launches a raw-update drainer. ``stop`` cancels that drainer but does not close or sentinel the public queue; consumers of ``iter_updates`` remain blocked until cancellation or a future event.

</details>

<details class="persistence" open markdown="1">
<summary>Persistence</summary>

Raw update processing holds a state lock, applies cursor/entity/duplicate changes, and persists them before emitted public events are queued and handlers are called. Persisted state is therefore ahead of, or equal to, observable delivery; it does not provide application-level exactly-once handling.

</details>

Initialize bounded raw/public queues and uninitialized persistent cursor state.

**Parameters:**

- **config** (<code>[ClientConfig](#miniproto.config.ClientConfig)</code>) – Client queue capacities, overflow policy, and duplicate-window settings.
- **storage** (<code>[SessionStorage](#miniproto.session.storage.SessionStorage)</code>) – Session storage used to load and atomically persist cursor state.
- **invoke** (<code>[UpdateInvoker](#miniproto.updates.manager.UpdateInvoker)</code>) – Async raw-RPC callable used for state and difference recovery.
