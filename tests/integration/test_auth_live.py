from __future__ import annotations

from live_helpers import authorized_user_client, live_client, require_bot_token, stored_user

from miniproto import event_loop


def run(coro):
    return event_loop.run(coro)


def test_live_bot_auth_get_me() -> None:
    async def scenario() -> None:
        token = require_bot_token()
        client = live_client("live-bot")
        try:
            await client.connect()
            user = await stored_user(client)
            if user is None or not user.is_bot:
                await client.sign_in_bot(token)
            me = await client.get_me(refresh=True)
            assert me.is_bot is True
            assert me.id > 0
        finally:
            await client.disconnect()

    run(scenario())


def test_live_phone_auth_get_me_and_reconnect() -> None:
    async def scenario() -> None:
        client = await authorized_user_client("live-user")
        try:
            me = await client.get_me(refresh=True)
            assert me.is_bot is False
            assert me.is_self is True
            assert me.id > 0
        finally:
            await client.disconnect()

        reconnected = live_client("live-user")
        try:
            await reconnected.connect()
            user = await stored_user(reconnected)
            assert user is not None
            assert user.is_bot is False
            me = await reconnected.get_me(refresh=True)
            assert me.id == user.id
        finally:
            await reconnected.disconnect()

    run(scenario())
