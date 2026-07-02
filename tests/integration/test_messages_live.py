from __future__ import annotations

import time

from live_helpers import authorized_user_client
from live_helpers import test_text as live_test_text

from miniproto import event_loop
from miniproto.raw import functions, types


def run(coro):
    return event_loop.run(coro)


def test_live_saved_messages_send_and_history_read() -> None:
    async def scenario() -> None:
        client = await authorized_user_client("live-user")
        text = f"{live_test_text()} {int(time.time())}"
        try:
            sent = await client.send_message("self", text)
            assert sent.id > 0
            assert sent.text == text
            history = await client.invoke(
                functions.MessagesGetHistory(
                    peer=types.InputPeerSelf(),
                    offset_id=0,
                    offset_date=0,
                    add_offset=0,
                    limit=10,
                    max_id=0,
                    min_id=0,
                    hash=0,
                )
            )
            messages = tuple(getattr(history, "messages", ()))
            assert any(getattr(message, "message", None) == text for message in messages)
        finally:
            await client.disconnect()

    run(scenario())
