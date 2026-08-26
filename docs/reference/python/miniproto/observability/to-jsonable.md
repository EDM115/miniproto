---
title: "miniproto.observability.to_jsonable"
description: "Recursively convert supported observability values into JSON-compatible shapes."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.observability.to_jsonable"
source_path: "src/miniproto/observability.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/observability.py#L420"
aliases: ["miniproto.to_jsonable"]
module: "miniproto.observability"
---

## `miniproto.observability.to_jsonable`

```python
to_jsonable(value: object) -> object
```

Recursively convert supported observability values into JSON-compatible shapes.

**Parameters:**

- **value** (<code>[object](#object)</code>) – Snapshot, event, mapping, list, tuple or leaf value.

**Returns:**

- <code>[object](#object)</code> – Dataclasses as dictionaries, mappings with string keys, sequences as lists or the leaf unchanged.
