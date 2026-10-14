---
title: "miniproto.client.Client.send_file"
description: "Upload or reuse media, send it to ``peer`` and return the resulting message."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.send_file"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L960"
aliases: ["miniproto.Client.send_file"]
module: "miniproto.client"
---

## `miniproto.client.Client.send_file`

```python
send_file(peer: Peer | str | int, file: FileSource, **kwargs: Any) -> Message
```

Upload or reuse media, send it to ``peer`` and return the resulting message.

``file`` accepts local, in-memory or streaming sources and reusable file IDs. Uploads default to ``DEFAULT_CHUNK_SIZE``, ``DEFAULT_UPLOAD_CONCURRENCY`` and two media lanes. Configured media defaults fill omitted ``concurrency`` and ``max_buffer_size`` values. Unknown-size streams may be spooled to disk before upload.

**Parameters:**

- **peer** (<code>[Peer](#miniproto.types.Peer) | [str](#str) | [int](#int)</code>) – Destination peer object, numeric ID or username.
- **file** (<code>[FileSource](#miniproto.media.FileSource)</code>) – Uploadable source or an existing miniproto file ID to reuse without uploading bytes.
- ****kwargs** (<code>[Any](#typing.Any)</code>) – Upload sizing, buffering and progress options, caption/formatting, raw media flags and send controls. ``media_lanes`` defaults to 2, ``0`` uses the main sender. ``upload_limit_parts`` accepts a numeric part cap or ``"app_config"``. The upload ``file_id`` option is a numeric upload identifier.

**Raises:**

- <code>[TypeError](#TypeError)</code> – If unsupported keyword options are provided.
- <code>[Exception](#Exception)</code> – Propagates file processing, peer resolution and Telegram RPC failures.
