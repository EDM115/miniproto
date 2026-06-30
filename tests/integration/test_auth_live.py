from __future__ import annotations

import os

import pytest

from miniproto.auth import dc_options_from_env

pytestmark = pytest.mark.skipif(
    os.environ.get("MINIPROTO_INTEGRATION") != "1",
    reason="set MINIPROTO_INTEGRATION=1 to run live Telegram integration tests",
)


def test_live_auth_environment_contract() -> None:
    required = ("MINIPROTO_API_ID", "MINIPROTO_API_HASH", "MINIPROTO_SESSION_KEY")
    missing = [name for name in required if not os.environ.get(name)]
    if missing:
        pytest.skip(f"missing live auth environment variables: {', '.join(missing)}")
    dc_options = dc_options_from_env()
    if not dc_options:
        pytest.skip("set at least one MINIPROTO_TEST_DC1..MINIPROTO_TEST_DC5 endpoint")
    if not (os.environ.get("MINIPROTO_TEST_PHONE") or os.environ.get("MINIPROTO_BOT_TOKEN")):
        pytest.skip("set MINIPROTO_TEST_PHONE or MINIPROTO_BOT_TOKEN")
    pytest.skip("live Telegram auth waits for the Phase 7 raw invoke transport path")
