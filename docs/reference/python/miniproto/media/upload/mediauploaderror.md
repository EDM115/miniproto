---
title: "miniproto.media.upload.MediaUploadError"
description: "Raised only for unsatisfiable part-count configuration or ``BoolFalse`` replies."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.media.upload.MediaUploadError"
source_path: "src/miniproto/media/upload.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/upload.py#L49"
aliases: ["miniproto.media.MediaUploadError"]
module: "miniproto.media.upload"
---

## `miniproto.media.upload.MediaUploadError`

Bases: <code>[RuntimeError](#RuntimeError)</code>

Raised only for unsatisfiable part-count configuration or ``BoolFalse`` replies.

Transport, RPC, cancellation, source and other invocation failures propagate
their original exceptions; this error marks a maximum-part-size constraint or
Telegram returning false after the configured false-result retry budget.
