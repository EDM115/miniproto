---
title: "miniproto.client.Client.import_session_string"
description: "Import a portable session into a disconnected client."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.import_session_string"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L390"
aliases: ["miniproto.Client.import_session_string"]
module: "miniproto.client"
---

## `miniproto.client.Client.import_session_string`

```python
import_session_string(value: str, *, format: SessionStringFormat = 'auto', passphrase: str | bytes | None = None, replace: bool = False, allow_mismatch: bool = False) -> SessionRecord
```

Import a portable session into a disconnected client.

**Parameters:**

- **value** (<code>[str](#str)</code>) – Serialized session string containing authorization state.
- **format** (<code>[SessionStringFormat](#miniproto.session.strings.SessionStringFormat)</code>) – Expected input dialect or ``"auto"`` for detection.
- **passphrase** (<code>[str](#str) | [bytes](#bytes) | None</code>) – Optional passphrase required to decode a protected string.
- **replace** (<code>[bool](#bool)</code>) – Whether any existing stored payload may be overwritten, defaulting to ``False``.
- **allow_mismatch** (<code>[bool](#bool)</code>) – Whether to bypass Pyrogram API, test-mode and account-kind compatibility checks.

**Returns:**

- <code>[SessionRecord](#miniproto.session.models.SessionRecord)</code> – The imported and stored record, without contacting Telegram to verify its authorization.

**Raises:**

- <code>[ConnectionError](#ConnectionError)</code> – If the local client lifecycle is connected.
- <code>[ValueError](#ValueError)</code> – If storage already contains a payload and ``replace`` is false, or Pyrogram compatibility checks fail.
- <code>[SessionEnvelopeError](#miniproto.errors.SessionEnvelopeError)</code> – If session-string decoding or authentication fails.

<details class="security" open markdown="1">
<summary>Security</summary>

``value`` and ``passphrase`` are sensitive credentials. Import is rejected while connected to avoid replacing active state.

</details>
