---
title: "miniproto.auth.dc.TEST_DC_OPTIONS"
description: "Public attribute `miniproto.auth.dc.TEST_DC_OPTIONS`."
generated: true
editUrl: false
language: "python"
kind: "attribute"
qualified_name: "miniproto.auth.dc.TEST_DC_OPTIONS"
source_path: "src/miniproto/auth/dc.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/dc.py#L26"
aliases: ["miniproto.auth.TEST_DC_OPTIONS"]
module: "miniproto.auth.dc"
---

## `miniproto.auth.dc.TEST_DC_OPTIONS`

```python
TEST_DC_OPTIONS: tuple[DCOption, ...] = tuple(DCOption(id=dc_id, ip_address=f'test-dc-{dc_id}.telegram.local', port=443, static=True) for dc_id in range(1, 6))
```
