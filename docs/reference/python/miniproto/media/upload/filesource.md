---
title: "miniproto.media.upload.FileSource"
description: "Public type alias `miniproto.media.upload.FileSource`."
generated: true
editUrl: false
language: "python"
kind: "type"
qualified_name: "miniproto.media.upload.FileSource"
source_path: "src/miniproto/media/upload.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/upload.py#L44"
aliases: ["miniproto.media.FileSource"]
module: "miniproto.media.upload"
---

## `miniproto.media.upload.FileSource`

```python
type FileSource = (
    str | os.PathLike[str] | bytes | bytearray | memoryview | BinaryIO | Iterable[bytes] | AsyncIterable[bytes]
)
```
