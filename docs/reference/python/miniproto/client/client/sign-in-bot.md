---
title: "miniproto.client.Client.sign_in_bot"
description: "Authorize the client as a bot and synchronize updates when enabled."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.client.Client.sign_in_bot"
source_path: "src/miniproto/client.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L553"
aliases: ["miniproto.Client.sign_in_bot"]
module: "miniproto.client"
---

## `miniproto.client.Client.sign_in_bot`

```python
sign_in_bot(token: str) -> object
```

Authorize the client as a bot and synchronize updates when enabled.

**Parameters:**

- **token** (<code>[str](#str)</code>) – BotFather-issued bearer token.

**Returns:**

- <code>[object](#object)</code> – Telegram's authorization result.

<details class="security" open markdown="1">
<summary>Security</summary>

The token is retained in memory for auxiliary bot download sessions; callers must keep it secret.

</details>
