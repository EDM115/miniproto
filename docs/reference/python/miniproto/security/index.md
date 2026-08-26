---
title: "miniproto.security"
description: "Public helpers for redacting sensitive values before diagnostic output."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.security"
source_path: "src/miniproto/security/__init__.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/security/__init__.py"
module: "miniproto.security"
---

## `miniproto.security`

Public helpers for redacting sensitive values before diagnostic output.

## Public objects

- [`REDACTED`](./redaction/redacted/) — Public attribute `miniproto.security.redaction.REDACTED`.
- [`is_sensitive_key`](./redaction/is-sensitive-key/) — Return whether a mapping key is recognized as sensitive.
- [`redact_mapping`](./redaction/redact-mapping/) — Return a recursively sanitized copy of a mapping.
- [`redact_text`](./redaction/redact-text/) — Mask recognized ``key=value`` and ``key: value`` secrets in text.
- [`redact_value`](./redaction/redact-value/) — Replace a value with the fixed redaction marker.
- [`safe_repr`](./redaction/safe-repr/) — Return a representation after recursively redacting supported secret shapes.
