---
title: "miniproto.tl.fast"
description: "Optional native fast paths for selected generated TL constructors."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.tl.fast"
source_path: "src/miniproto/tl/fast.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/tl/fast.py"
module: "miniproto.tl.fast"
---

## `miniproto.tl.fast`

Optional native fast paths for selected generated TL constructors.

## Public objects

- [`encode_fast`](./encode-fast/) — Attempt native serialization for a generated TL constructor.
- [`decode_fast`](./decode-fast/) — Attempt native deserialization for a generated TL constructor.
- [`materialize_empty_object`](./materialize-empty-object/) — Resolve a native empty-object token to its generated TL instance.
- [`native_fast_paths_available`](./native-fast-paths-available/) — Report whether both native TL encode and decode fast paths were imported.
