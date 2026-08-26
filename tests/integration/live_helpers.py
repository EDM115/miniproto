from __future__ import annotations

import os
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

from miniproto import Client, ClientConfig, EncryptedSQLiteSessionStorage
from miniproto.invoke import load_session_record
from miniproto.session.models import UserIdentity

_LOADED_DOTENV = False
_DOTENV_VALUES: dict[str, str] = {}


def load_dotenv() -> None:
    global _LOADED_DOTENV, _DOTENV_VALUES
    if _LOADED_DOTENV:
        return
    _LOADED_DOTENV = True
    dotenv = Path(".env")
    if not dotenv.exists():
        return
    for raw_line in dotenv.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        _DOTENV_VALUES.setdefault(key, value.strip().strip('"').strip("'"))


def require_live() -> None:
    load_dotenv()
    if _env("MINIPROTO_INTEGRATION") != "1":
        pytest.skip("set MINIPROTO_INTEGRATION=1 to run live Telegram integration tests")
    _require("MINIPROTO_API_ID", "MINIPROTO_API_HASH", "MINIPROTO_SESSION_KEY")


def require_real_live() -> None:
    require_live()
    if _env("MINIPROTO_REAL_INTEGRATION") != "1":
        pytest.skip("set MINIPROTO_REAL_INTEGRATION=1 to run production Telegram live tests")


def require_bot_token() -> str:
    require_real_live()
    return _require("MINIPROTO_BOT_TOKEN")["MINIPROTO_BOT_TOKEN"]


def require_real_phone() -> str:
    require_real_live()
    return _require("MINIPROTO_REAL_PHONE")["MINIPROTO_REAL_PHONE"]


def test_text() -> str:
    load_dotenv()
    return _env("MINIPROTO_TEST_SAVED_MESSAGE_TEXT") or "miniproto live saved-message smoke"


def upload_file_path() -> Path:
    require_real_live()
    path = Path(_require("MINIPROTO_TEST_UPLOAD_FILE")["MINIPROTO_TEST_UPLOAD_FILE"])
    if not path.exists():
        pytest.skip(f"MINIPROTO_TEST_UPLOAD_FILE does not exist: {path}")
    return path


def download_path() -> Path:
    load_dotenv()
    return Path(_env("MINIPROTO_TEST_DOWNLOAD_PATH") or ".tmp/miniproto-live-download.bin")


def allow_prompt() -> bool:
    load_dotenv()
    return _env("MINIPROTO_LIVE_PROMPT_CODE") == "1" and sys.stdin.isatty()


def code_callback() -> Callable[[], str]:
    if not allow_prompt():
        pytest.skip("set MINIPROTO_LIVE_PROMPT_CODE=1 and run interactively to enter the Telegram login code")

    def prompt() -> str:
        return input("Telegram login code: ").strip()

    return prompt


def password_callback() -> Callable[[], str] | None:
    load_dotenv()
    password = _env("MINIPROTO_REAL_PASSWORD")
    if password:
        return lambda: password
    if not allow_prompt():
        return None

    def prompt() -> str:
        return input("Telegram 2FA password: ")

    return prompt


def live_client(name: str, *, real: bool = True) -> Client:
    if real:
        require_real_live()
        dc_id = int(_env("MINIPROTO_REAL_DC_ID") or "2")
        test_mode = False
    else:
        require_live()
        dc_id = int(_env("MINIPROTO_TEST_DC_ID") or "2")
        test_mode = True
    Path(".tmp").mkdir(exist_ok=True)
    storage = EncryptedSQLiteSessionStorage(
        Path(".tmp") / f"miniproto-{name}.sqlite", key=_env_required("MINIPROTO_SESSION_KEY")
    )
    return Client(
        ClientConfig(
            api_id=int(_env_required("MINIPROTO_API_ID")),
            api_hash=_env_required("MINIPROTO_API_HASH"),
            session_storage=storage,
            dc_id=dc_id,
            test_mode=test_mode,
            request_timeout=45.0,
            max_request_retries=3,
        )
    )


async def authorized_user_client(name: str = "live-user") -> Client:
    client = live_client(name)
    await client.connect()
    user = await stored_user(client)
    if user is None or user.is_bot:
        await client.sign_in_phone(require_real_phone(), code_callback(), password_callback())
    return client


async def stored_user(client: Client) -> UserIdentity | None:
    storage = client.config.session_storage
    if storage is None:
        return None
    return load_session_record(await storage.load(), client.config.dc_id).user


def _require(*names: str) -> dict[str, str]:
    load_dotenv()
    missing = [name for name in names if not _env(name)]
    if missing:
        pytest.skip(f"missing live environment variables: {', '.join(missing)}")
    return {name: _env_required(name) for name in names}


def _env(name: str, default: str | None = None) -> str | None:
    load_dotenv()
    return os.environ.get(name) or _DOTENV_VALUES.get(name, default)


def _env_required(name: str) -> str:
    value = _env(name)
    if value is None:
        raise KeyError(name)
    return value
