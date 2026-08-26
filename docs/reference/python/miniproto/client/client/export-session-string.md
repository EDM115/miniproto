---
title: "miniproto.client.Client.export_session_string"
description: "Export the current stored session as a portable bearer-secret string."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.export_session_string"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L350"
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
- **passphrase** (<code>[str](#str) | [bytes](#bytes) | None</code>) – Optional passphrase used by formats that support protected export.

<details class="security" open markdown="1">
<summary>Security</summary>

The returned value is a bearer credential or a protected representation of one; callers must avoid logging or exposing it.

</details>
