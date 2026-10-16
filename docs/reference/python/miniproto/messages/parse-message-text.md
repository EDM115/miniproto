---
title: "miniproto.messages.parse_message_text"
description: "Render the supported lightweight Markdown delimiters into MTProto entities."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.messages.parse_message_text"
source_path: "src/miniproto/messages.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/messages.py#L31"
module: "miniproto.messages"
---

## `miniproto.messages.parse_message_text`

```python
parse_message_text(text: str, parse_mode: str | None = None) -> ParsedMessageText
```

Render the supported lightweight Markdown delimiters into MTProto entities.

**Parameters:**

- **text** (<code>[str](#str)</code>) – Source message text. In Markdown mode, a backslash outside a delimited span escapes the next character.
- **parse_mode** (<code>[str](#str) | None</code>) – ``markdown``, ``markdown-lite`` or ``md`` parses ``**bold**``, ``__italic__``, inline backticks and triple-backtick blocks without nesting or language tags. ``None``, an empty spelling, ``plain``, ``text`` and ``none`` preserve text verbatim.

**Returns:**

- <code>[ParsedMessageText](#miniproto.messages.ParsedMessageText)</code> – Rendered text and entities whose offsets and lengths use UTF-16 code units.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``parse_mode`` is not a supported spelling.
