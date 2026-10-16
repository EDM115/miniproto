---
title: Phone, Bot and 2FA Authorization
description: Authorize a user through a phone-code callback or a bot through its bearer token.
slug: /start/authentication/
generated: false
---

Authorization is a live Telegram operation. The examples deliberately obtain secrets at runtime and do not make a credentialed test claim. Before using a durable client, arrange a non-empty `MINIPROTO_SESSION_KEY` through a secret manager and review [Session Security](../session-security.md).

## Phone account with optional 2FA

`Client.sign_in_phone()` sends a code request. It calls `code_callback` when Telegram returns a code challenge and calls `password_callback` only when Telegram requires two-factor authentication. Each callback can return a string or an awaitable string.

```python
import getpass
import os

from miniproto import Client, ClientConfig, event_loop


def phone_code() -> str:
    return getpass.getpass("Telegram login code: ")


def two_factor_password() -> str:
    return getpass.getpass("Two-step password: ")


async def main() -> None:
    config = ClientConfig(api_id=int(os.environ["MINIPROTO_API_ID"]), api_hash=os.environ["MINIPROTO_API_HASH"])
    async with Client(config) as client:
        await client.sign_in_phone(
            os.environ["MINIPROTO_PHONE"], code_callback=phone_code, password_callback=two_factor_password
        )


event_loop.run(main())
```

An account that needs 2FA raises `PasswordRequired` if you omit the password callback. A phone number that needs registration raises `SignUpRequired`. miniproto does not create the account. Telegram classifies invalid codes as `InvalidCode`. Do not log callback results, phone numbers, API hashes or session mappings.

## Bot account

Bots use `Client.sign_in_bot(token)`. The token is a bearer credential, so retain it only in protected process configuration and do not place it in a URL, command line or repository file.

```python
import os

from miniproto import Client, ClientConfig, event_loop


async def main() -> None:
    config = ClientConfig(api_id=int(os.environ["MINIPROTO_API_ID"]), api_hash=os.environ["MINIPROTO_API_HASH"])
    async with Client(config) as client:
        await client.sign_in_bot(os.environ["MINIPROTO_BOT_TOKEN"])
        print((await client.get_me()).id)


event_loop.run(main())
```

After bot authorization, the client saves the bot identity in its selected storage and syncs update state when updates are enabled. Bot authorization does not grant user-account capabilities or access to every peer. Telegram still controls the bot's permissions and server-side limits.

## Reuse an authorized session

Use the same durable session path and key only for the same account. `Client.is_authorized()` checks stored state for an auth key or user identity. It does not prove that Telegram will permit the next network operation. Import a portable session while the client is disconnected. If storage already has a value, pass `replace=True` to replace it. [Session Security](../session-security.md) covers formats, lossy third-party conversions, encryption and rotation.
