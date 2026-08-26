---
title: "miniproto.session.strings"
description: "Import and export validated portable bearer session strings without client dependencies."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.session.strings"
source_path: "src/miniproto/session/strings.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/strings.py"
module: "miniproto.session.strings"
---

## `miniproto.session.strings`

Import and export validated portable bearer session strings without client dependencies.

Only protected native strings use scrypt-derived AES-256-GCM authenticated encryption.
Plain native strings, Telethon strings and Pyrogram strings are bearer encodings:
they are validated for shape and may carry a checksum, but do not authenticate a
holder or protect their contained authorization key.

## Public objects

- [`SessionStringFormat`](./sessionstringformat/) — Public attribute `miniproto.session.strings.SessionStringFormat`.
- [`NATIVE_SESSION_PREFIX`](./native-session-prefix/) — Public attribute `miniproto.session.strings.NATIVE_SESSION_PREFIX`.
- [`MAX_SESSION_PAYLOAD_BYTES`](./max-session-payload-bytes/) — Public attribute `miniproto.session.strings.MAX_SESSION_PAYLOAD_BYTES`.
- [`MAX_SESSION_STRING_CHARS`](./max-session-string-chars/) — Public attribute `miniproto.session.strings.MAX_SESSION_STRING_CHARS`.
- [`MAX_DC_OPTIONS`](./max-dc-options/) — Public attribute `miniproto.session.strings.MAX_DC_OPTIONS`.
- [`MAX_PEERS`](./max-peers/) — Public attribute `miniproto.session.strings.MAX_PEERS`.
- [`SessionString`](./sessionstring/) — A bearer-secret string whose representation is always redacted.
- [`export_session_string`](./export-session-string/) — Export a typed or decoded session record in a portable bearer format.
- [`import_session_string`](./import-session-string/) — Import a native, Telethon v1 or Pyrogram string into a validated record.
