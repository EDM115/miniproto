---
title: "miniproto.session.strings.import_session_string"
description: "Import a native, Telethon v1, or Pyrogram string into a validated record."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.strings.import_session_string"
source_path: "src/miniproto/session/strings.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/strings.py#L122"
aliases: ["miniproto.import_session_string","miniproto.session.import_session_string"]
module: "miniproto.session.strings"
---

## `miniproto.session.strings.import_session_string`

```python
import_session_string(value: str, *, format: SessionStringFormat = 'auto', passphrase: str | bytes | None = None) -> SessionRecord
```

Import a native, Telethon v1, or Pyrogram string into a validated record.

**Parameters:**

- **value** (<code>[str](#str)</code>) – Bearer session string; it is parsed without stripping characters.
- **format** (<code>[SessionStringFormat](#miniproto.session.strings.SessionStringFormat)</code>) – Explicit format or ``auto`` detection from strict wire shapes.
- **passphrase** (<code>[str](#str) | [bytes](#bytes) | None</code>) – Required only for protected native miniproto strings.

**Returns:**

- <code>[SessionRecord](#miniproto.session.models.SessionRecord)</code> – A normalized session record. Foreign formats set bootstrap metadata.

**Raises:**

- <code>[SessionEnvelopeError](#miniproto.errors.SessionEnvelopeError)</code> – If the string, envelope, protected-native authentication, or format is invalid.
- <code>[TypeError](#TypeError)</code> – If ``value`` is not a string.
