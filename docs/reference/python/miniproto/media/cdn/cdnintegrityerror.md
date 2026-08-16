---
title: "miniproto.media.cdn.CdnIntegrityError"
description: "Raised when a CDN range lacks valid ``FileHash`` coverage or verification fails."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.media.cdn.CdnIntegrityError"
source_path: "src/miniproto/media/cdn.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/cdn.py#L26"
aliases: ["miniproto.CdnIntegrityError","miniproto.media.CdnIntegrityError"]
module: "miniproto.media.cdn"
---

## `miniproto.media.cdn.CdnIntegrityError`

Bases: <code>[CdnError](#miniproto.media.cdn.CdnError)</code>

Raised when a CDN range lacks valid ``FileHash`` coverage or verification fails.

This includes missing hash metadata, non-positive declared ``FileHash.limit``,
a response shorter than that declared limit, and SHA-256 mismatches. The
declared limit controls exactly how many decrypted bytes form each verified
range; it is not assumed to be a fixed-size block.
