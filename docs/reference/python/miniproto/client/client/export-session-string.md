---
title: "miniproto.client.Client.export_session_string"
description: "Export the current stored session as a portable bearer-secret string."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.export_session_string"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L359"
aliases: ["miniproto.Client.export_session_string"]
module: "miniproto.client"
---

## `miniproto.client.Client.export_session_string`

```python
export_session_string(*, format: Literal['miniproto', 'telethon', 'pyrogram'] = 'miniproto', passphrase: str | bytes | None = None) -> SessionString
```

Export the current stored session as a portable bearer-secret string.

**Parameters:**

- **format** (<code>[Literal](#typing.Literal)['miniproto', 'telethon', 'pyrogram']</code>) – Portable session-string dialect, defaulting to miniproto's native format.
- **passphrase** (<code>[str](#str) | [bytes](#bytes) | None</code>) – Optional protection for native miniproto output. Telethon and Pyrogram output reject passphrases.

**Returns:**

- <code>[SessionString](#miniproto.session.strings.SessionString)</code> – A ``SessionString`` whose ``repr`` is redacted. Printing or converting it to ordinary text still exposes its contents.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If no session payload is stored.
- <code>[SessionEnvelopeError](#miniproto.errors.SessionEnvelopeError)</code> – If the selected format lacks required state or rejects the supplied options.

<details class="security" open markdown="1">
<summary>Security</summary>

The returned value contains bearer credentials, optionally protected by a native-format passphrase. Avoid logging or exposing it.

</details>
