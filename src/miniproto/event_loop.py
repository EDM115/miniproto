"""Explicit optimized asyncio event-loop selection."""

from __future__ import annotations

import asyncio
import sys
import warnings
from collections.abc import Coroutine
from importlib import import_module, metadata
from types import ModuleType
from typing import Any

_BACKEND_NAME = "winloop" if sys.platform == "win32" else "uvloop"
_BACKEND: ModuleType | None = None
_BACKEND_LOADED = False
_BACKEND_LOAD_ERROR: Exception | None = None
_INSTALL_ERROR: Exception | None = None
_INSTALLED = False


def backend_name() -> str:
    """Return the optimized event-loop package selected for this platform."""
    return _BACKEND_NAME


def backend() -> ModuleType | None:
    """Load and return the optimized backend module when it is available."""
    return _load_backend()


def backend_version() -> str | None:
    """Return the installed optimized backend version, if available."""
    selected_backend = _load_backend()
    if selected_backend is None:
        return None
    try:
        return metadata.version(_BACKEND_NAME)
    except metadata.PackageNotFoundError:
        version = getattr(selected_backend, "__version__", None)
        return version if isinstance(version, str) else None


def optimized_available() -> bool:
    """Return whether the platform's optimized event-loop backend can be loaded."""
    return _load_backend() is not None


def installed() -> bool:
    """Return whether miniproto installed an optimized event-loop policy."""
    return _INSTALLED


def install_error() -> Exception | None:
    """Return the most recent explicit-install or backend-load error, if any."""
    return _INSTALL_ERROR or _BACKEND_LOAD_ERROR


def install() -> bool:
    """Explicitly install the legacy optimized event-loop policy before Python 3.16."""
    global _INSTALLED, _INSTALL_ERROR
    warnings.warn(
        "event_loop.install() uses the deprecated asyncio policy system; use event_loop.run() or asyncio.Runner(loop_factory=event_loop.new_event_loop)",
        DeprecationWarning,
        stacklevel=2,
    )
    if sys.version_info >= (3, 16):
        _INSTALL_ERROR = RuntimeError("asyncio event-loop policies are unsupported on Python 3.16+")
        _INSTALLED = False
        return False
    try:
        selected_backend = _load_backend()
        if selected_backend is None:
            _INSTALLED = False
            return False
        install_func = getattr(selected_backend, "install", None)
        if not callable(install_func):
            _INSTALL_ERROR = RuntimeError(
                f"{_BACKEND_NAME} does not expose a legacy event-loop policy installer"
            )
            _INSTALLED = False
            return False
        install_func()
    except Exception as exc:
        _INSTALL_ERROR = exc
        _INSTALLED = False
        return False
    _INSTALLED = True
    _INSTALL_ERROR = None
    return True


def new_event_loop() -> asyncio.AbstractEventLoop:
    """Create an optimized event loop when available, otherwise create a stdlib loop."""
    selected_backend = _load_backend()
    factory = getattr(selected_backend, "new_event_loop", None) if selected_backend else None
    loop = factory() if callable(factory) else asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop


def run[T](main: Coroutine[Any, Any, T], *, debug: bool | None = None) -> T:
    """Run a coroutine with Runner and the optimized backend factory when available."""
    loop_factory = None if _requires_stdlib_debug_runner(debug) else new_event_loop
    try:
        with asyncio.Runner(debug=debug, loop_factory=loop_factory) as runner:
            return runner.run(main)
    finally:
        asyncio.set_event_loop(None)


def _requires_stdlib_debug_runner(debug: bool | None) -> bool:
    if not debug or _BACKEND_NAME != "winloop" or sys.version_info < (3, 14):
        return False
    try:
        installed_version = metadata.version("winloop")
    except metadata.PackageNotFoundError:
        return False
    numeric_parts = tuple(
        int(digits)
        for part in installed_version.split(".")[:3]
        if (digits := "".join(character for character in part if character.isdigit()))
    )
    return numeric_parts <= (0, 6, 3)


def _load_backend() -> ModuleType | None:
    global _BACKEND, _BACKEND_LOADED, _BACKEND_LOAD_ERROR
    if _BACKEND_LOADED:
        if _BACKEND_LOAD_ERROR is not None:
            raise _BACKEND_LOAD_ERROR
        return _BACKEND
    try:
        _BACKEND = import_module(_BACKEND_NAME)
    except ModuleNotFoundError as exc:
        if exc.name != _BACKEND_NAME:
            _BACKEND_LOAD_ERROR = exc
            raise
        _BACKEND = None
    except Exception as exc:
        _BACKEND_LOAD_ERROR = exc
        raise
    finally:
        _BACKEND_LOADED = True
    return _BACKEND


__all__ = [
    "backend",
    "backend_name",
    "backend_version",
    "install",
    "install_error",
    "installed",
    "new_event_loop",
    "optimized_available",
    "run",
]
