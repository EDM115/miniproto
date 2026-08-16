---
title: "miniproto.auth.dc.select_dc_option"
description: "Choose the best endpoint for a data center."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.auth.dc.select_dc_option"
source_path: "src/miniproto/auth/dc.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/dc.py#L104"
aliases: ["miniproto.auth.select_dc_option"]
module: "miniproto.auth.dc"
---

## `miniproto.auth.dc.select_dc_option`

```python
select_dc_option(options: Iterable[DCOption], dc_id: int, *, prefer_ipv6: bool = False, allow_media_only: bool = False) -> DCOption
```

Choose the best endpoint for a data center.

**Parameters:**

- **options** (<code>[Iterable](#collections.abc.Iterable)[[DCOption](#miniproto.session.models.DCOption)]</code>) – Candidate connection options.
- **dc_id** (<code>[int](#int)</code>) – Required Telegram data-center identifier.
- **prefer_ipv6** (<code>[bool](#bool)</code>) – Prefer an IPv6 candidate when one is available.
- **allow_media_only** (<code>[bool](#bool)</code>) – Permit endpoints reserved for media traffic.

**Returns:**

- <code>[DCOption](#miniproto.session.models.DCOption)</code> – A non-media endpoint when possible, otherwise the best available candidate.

**Raises:**

- <code>[ValueError](#ValueError)</code> – If ``options`` has no endpoint for ``dc_id``.
