---
title: "miniproto.media.upload.MediaUploadError"
description: "Raised for an unsatisfiable part cap or exhausted non-true save results."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.media.upload.MediaUploadError"
source_path: "src/miniproto/media/upload.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/upload.py#L46"
aliases: ["miniproto.media.MediaUploadError"]
module: "miniproto.media.upload"
---

## `miniproto.media.upload.MediaUploadError`

Bases: <code>[RuntimeError](#RuntimeError)</code>

Raised for an unsatisfiable part cap or exhausted non-true save results.

Transport, RPC, cancellation and source failures propagate their original exceptions. This error marks a part cap that cannot fit 512 KiB parts, or a save result other than ``True`` or ``BoolTrue`` after retries are exhausted.
