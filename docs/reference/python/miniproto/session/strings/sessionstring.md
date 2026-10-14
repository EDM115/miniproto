---
title: "miniproto.session.strings.SessionString"
description: "Session contents with a redacted ``repr``."
generated: true
editUrl: false
language: "python"
kind: "class"
qualified_name: "miniproto.session.strings.SessionString"
source_path: "src/miniproto/session/strings.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/session/strings.py#L69"
aliases: ["miniproto.SessionString","miniproto.session.SessionString"]
module: "miniproto.session.strings"
---

## `miniproto.session.strings.SessionString`

Bases: <code>[str](#str)</code>

Session contents with a redacted ``repr``.

Printing, formatting or converting the value with ``str`` exposes its contents, including bearer credentials in unprotected formats.
