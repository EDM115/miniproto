---
title: "miniproto.session.strings.export_session_string"
description: "Export a typed or decoded session record in a portable bearer format."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.session.strings.export_session_string"
source_path: "src/miniproto/session/strings.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/strings.py#L80"
aliases: ["miniproto.export_session_string","miniproto.session.export_session_string"]
module: "miniproto.session.strings"
---

## `miniproto.session.strings.export_session_string`

```python
export_session_string(record_or_mapping: SessionRecord | Mapping[str, Any], *, format: Literal['miniproto', 'telethon', 'pyrogram'] = 'miniproto', passphrase: str | bytes | None = None, api_id: int | None = None, test_mode: bool | None = None) -> SessionString
```

Export a typed or decoded session record in a portable bearer format.

**Parameters:**

- **record_or_mapping** (<code>[SessionRecord](#miniproto.session.models.SessionRecord) | [Mapping](#collections.abc.Mapping)[[str](#str), [Any](#typing.Any)]</code>) – A validated record or an already decoded record mapping.
- **format** (<code>[Literal](#typing.Literal)['miniproto', 'telethon', 'pyrogram']</code>) – Native ``miniproto`` (default), ``telethon``, or ``pyrogram``.
- **passphrase** (<code>[str](#str) | [bytes](#bytes) | None</code>) – Optional native-only authenticated encryption using scrypt and AES-256-GCM.
- **api_id** (<code>[int](#int) | None</code>) – Required for Pyrogram when absent from record metadata.
- **test_mode** (<code>[bool](#bool) | None</code>) – Required for Pyrogram when absent from record metadata.

**Returns:**

- <code>[SessionString](#miniproto.session.strings.SessionString)</code> – A redacted-on-representation bearer session string.

**Raises:**

- <code>[SessionEnvelopeError](#miniproto.errors.SessionEnvelopeError)</code> – If data, authentication material, limits, or format options are invalid.
- <code>[TypeError](#TypeError)</code> – If the input is neither a record nor mapping.

Protected native strings authenticate and encrypt their payload. Plain native,
Telethon, and Pyrogram outputs remain validated bearer encodings. Generic
asynchronous storage is exported through ``Client.export_session_string``; this
layer deliberately only accepts already loaded state.
