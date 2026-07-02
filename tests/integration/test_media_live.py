from __future__ import annotations

import asyncio
import time

from live_helpers import authorized_user_client, download_path, upload_file_path

from miniproto.media import media_from_raw
from miniproto.raw import functions, types
from miniproto.types import Media


def run(coro):
    return asyncio.run(coro)


def test_live_saved_messages_media_upload_download() -> None:
    async def scenario() -> None:
        client = await authorized_user_client("live-user")
        source = upload_file_path()
        target = download_path()
        caption = f"miniproto live media smoke {int(time.time())}"
        try:
            sent = await client.send_file("self", source, caption=caption, file_name=source.name)
            media = sent.media or await _find_recent_media(client, caption)
            assert media is not None
            await asyncio.to_thread(target.unlink, missing_ok=True)
            result = await client.download_media(media, target)
            source_size = await asyncio.to_thread(lambda: source.stat().st_size)
            assert result.bytes_downloaded == source_size
            downloaded = await asyncio.to_thread(target.read_bytes)
            expected = await asyncio.to_thread(source.read_bytes)
            assert downloaded == expected
        finally:
            await client.disconnect()

    run(scenario())


async def _find_recent_media(client, caption: str) -> Media | None:
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
    for message in getattr(history, "messages", ()):
        if getattr(message, "message", None) == caption:
            return media_from_raw(message)
    return None
