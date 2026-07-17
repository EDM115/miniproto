from __future__ import annotations

import asyncio
import json
import subprocess
import sys
from types import ModuleType

import pytest

from miniproto import event_loop


def test_event_loop_backend_name_matches_platform() -> None:
    assert event_loop.backend_name() == ("winloop" if sys.platform == "win32" else "uvloop")


def test_import_has_no_event_loop_policy_or_backend_side_effects() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import asyncio,json,sys; "
                "before=id(asyncio.get_event_loop_policy()); "
                "import miniproto; "
                "after=id(asyncio.get_event_loop_policy()); "
                "print(json.dumps({'same_policy':before==after,'backend_loaded':"
                "'winloop' in sys.modules or 'uvloop' in sys.modules}))"
            ),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    result = json.loads(completed.stdout)
    assert result == {"same_policy": True, "backend_loaded": False}


def test_event_loop_backend_loads_on_demand() -> None:
    backend = event_loop.backend()
    if backend is None:
        assert not event_loop.installed()
        assert event_loop.backend_version() is None
    else:
        assert not event_loop.installed()
        assert event_loop.install_error() is None
        version = event_loop.backend_version()
        assert version is None or isinstance(version, str)


def test_event_loop_run_uses_available_backend_or_stdlib() -> None:
    async def compute() -> str:
        return "ok"

    assert event_loop.run(compute()) == "ok"


def test_event_loop_run_uses_runner_cleanup_and_debug() -> None:
    generator_closed = False

    async def values():
        nonlocal generator_closed
        try:
            yield 1
        finally:
            generator_closed = True

    async def compute() -> bool:
        generator = values()
        assert await anext(generator) == 1
        return asyncio.get_running_loop().get_debug()

    assert event_loop.run(compute(), debug=True)
    assert generator_closed


def test_event_loop_run_propagates_factory_and_coroutine_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    async def fail() -> None:
        raise LookupError("sentinel")

    with pytest.raises(LookupError, match="sentinel"):
        event_loop.run(fail())

    def broken_factory() -> asyncio.AbstractEventLoop:
        raise RuntimeError("factory sentinel")

    coroutine = asyncio.sleep(0)
    monkeypatch.setattr(event_loop, "new_event_loop", broken_factory)
    try:
        with pytest.raises(RuntimeError, match="factory sentinel"):
            event_loop.run(coroutine)
    finally:
        coroutine.close()


def test_backend_nested_module_error_is_cached(monkeypatch: pytest.MonkeyPatch) -> None:
    nested_error = ModuleNotFoundError("nested dependency missing", name="backend_dependency")

    def fail_import(_name: str) -> ModuleType:
        raise nested_error

    monkeypatch.setattr(event_loop, "_BACKEND", None)
    monkeypatch.setattr(event_loop, "_BACKEND_LOADED", False)
    monkeypatch.setattr(event_loop, "_BACKEND_LOAD_ERROR", None)
    monkeypatch.setattr(event_loop, "import_module", fail_import)

    with pytest.raises(ModuleNotFoundError) as first:
        event_loop.backend()
    with pytest.raises(ModuleNotFoundError) as second:
        event_loop.backend()
    assert first.value is nested_error
    assert second.value is nested_error


def test_event_loop_install_is_explicit_and_deprecated() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import json,warnings; from miniproto import event_loop; "
                "warnings.simplefilter('always'); "
                "caught=[]; "
                "manager=warnings.catch_warnings(record=True); "
                "caught=manager.__enter__(); "
                "installed=event_loop.install(); "
                "manager.__exit__(None,None,None); "
                "print(json.dumps({'installed':installed,'warning':any(item.category is DeprecationWarning for item in caught),"
                "'error':event_loop.install_error() is not None,'backend':event_loop.backend() is not None}))"
            ),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(completed.stdout)
    assert result["warning"]
    if sys.version_info >= (3, 16):
        assert not result["installed"]
        assert result["error"]
    elif not result["backend"]:
        assert not result["installed"]
    else:
        assert result["installed"]
