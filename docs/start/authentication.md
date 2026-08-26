---
title: Phone, Bot and 2FA Authorization
description: Authorize a user through a phone-code callback or a bot through its bearer token.
slug: /start/authentication/
generated: false
---

Authorization is a live Telegram operation. The examples deliberately obtain secrets at runtime and do not make a credentialed test claim. Before using a durable client, arrange a non-empty `MINIPROTO_SESSION_KEY` through a secret manager and review [Session Security](../session-security.md).

## Phone account with optional 2FA

`Client.sign_in_phone()` sends a code request, calls `code_callback` and calls `password_callback` only if Telegram requests two-factor authentication. Both callbacks can return a string directly or return an awaitable string.

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

Without a password callback, an account that needs 2FA raises `PasswordRequired`. A phone number that needs registration raises `SignUpRequired`; this SDK does not silently create the account. Invalid Telegram codes are classified as `InvalidCode`. Do not log a callback return value, phone number, API hash or resulting session mapping.

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

The client persists the authorized bot identity in its selected storage, then synchronizes update state when updates are enabled. Do not infer that bot authorization grants user-account capabilities, access to every peer or permission to send in a particular chat; Telegram still applies the bot's own permissions and server-side limits.

## Reuse an authorized session

Use the same durable session path and key for the same account only. `Client.is_authorized()` checks whether stored state has an auth key or user identity; it does not prove that a subsequent network operation will be permitted. Importing a portable session requires a disconnected client and requires explicit replacement when storage already has a value. The format, lossy third-party conversions, encryption and rotation guidance are all in [Session Security](../session-security.md).
