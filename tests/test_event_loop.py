from __future__ import annotations

import sys

from miniproto import event_loop


def test_event_loop_backend_name_matches_platform() -> None:
    assert event_loop.backend_name() == ("winloop" if sys.platform == "win32" else "uvloop")


def test_event_loop_is_auto_installed_when_backend_is_available() -> None:
    backend = event_loop.backend()
    if backend is None:
        assert not event_loop.installed()
        assert event_loop.backend_version() is None
    else:
        assert event_loop.installed() or event_loop.install_error() is not None
        version = event_loop.backend_version()
        assert version is None or isinstance(version, str)


def test_event_loop_run_uses_available_backend_or_stdlib() -> None:
    async def compute() -> str:
        return "ok"

    assert event_loop.run(compute()) == "ok"
