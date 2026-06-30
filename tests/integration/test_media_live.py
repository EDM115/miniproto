from __future__ import annotations

import os

import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("MINIPROTO_INTEGRATION") != "1",
    reason="set MINIPROTO_INTEGRATION=1 to run live Telegram integration tests",
)


def test_live_saved_messages_media_environment_contract() -> None:
    required = (
        "MINIPROTO_API_ID",
        "MINIPROTO_API_HASH",
        "MINIPROTO_SESSION_KEY",
        "MINIPROTO_TEST_UPLOAD_FILE",
    )
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        pytest.skip(f"missing live media environment variables: {', '.join(missing)}")
    if not (os.environ.get("MINIPROTO_TEST_PHONE") or os.environ.get("MINIPROTO_BOT_TOKEN")):
        pytest.skip("set MINIPROTO_TEST_PHONE or MINIPROTO_BOT_TOKEN")
    pytest.skip(
        "live Saved Messages media upload/download waits for maintained test credentials and transport validation"
    )
