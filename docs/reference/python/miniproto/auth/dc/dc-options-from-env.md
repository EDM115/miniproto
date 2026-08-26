---
title: "miniproto.auth.dc.dc_options_from_env"
description: "Read local test-DC overrides from environment-style mappings."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.dc.dc_options_from_env"
source_path: "src/miniproto/auth/dc.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/dc.py#L41"
aliases: ["miniproto.auth.dc_options_from_env"]
module: "miniproto.auth.dc"
---

## `miniproto.auth.dc.dc_options_from_env`

```python
dc_options_from_env(environ: Mapping[str, str] | None = None) -> tuple[DCOption, ...]
```

Read local test-DC overrides from environment-style mappings.

**Parameters:**

- **environ** (<code>[Mapping](#collections.abc.Mapping)[[str](#str), [str](#str)] | None</code>) – Mapping to read instead of :data:`os.environ`; defaults to the process environment.

**Returns:**

- <code>[tuple](#tuple)[[DCOption](#miniproto.session.models.DCOption), ...]</code> – Static options for populated ``MINIPROTO_TEST_DC1`` through ``MINIPROTO_TEST_DC5`` entries.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If an override is not a valid ``host:port`` or ``[ipv6]:port`` endpoint.
