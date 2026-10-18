---
title: "miniproto.messages.ParsedMessageText"
description: "Rendered message text and UTF-16-indexed MTProto entities."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.messages.ParsedMessageText"
source_path: "src/miniproto/messages.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/messages.py#L18"
module: "miniproto.messages"
---

## `miniproto.messages.ParsedMessageText`

```python
ParsedMessageText(text: str, entities: tuple[object, ...] = ()) -> None
```

Rendered message text and UTF-16-indexed MTProto entities.

**Attributes:**

- [**text**](#miniproto.messages.ParsedMessageText.text) (<code>[str](#str)</code>) – Rendered text after supported delimiters and escapes are removed.
- [**entities**](#miniproto.messages.ParsedMessageText.entities) (<code>[tuple](#tuple)[[object](#object), ...]</code>) – Immutable entities whose offsets and lengths are UTF-16 code units.
