"""Automatic optimized asyncio event-loop selection."""

from __future__ import annotations

import asyncio
import sys
import warnings
from collections.abc import Callable, Coroutine
from importlib import import_module, metadata
from types import ModuleType
from typing import Any

_BACKEND_NAME = "winloop" if sys.platform == "win32" else "uvloop"
_BACKEND: ModuleType | None = None
_INSTALL_ERROR: Exception | None = None
_INSTALLED = False


def backend_name() -> str:
    """Return the optimized event-loop package selected for this platform."""
    return _BACKEND_NAME


def backend() -> ModuleType | None:
    """Return the imported optimized backend module when it is installed."""
    return _BACKEND


def backend_version() -> str | None:
    """Return the installed optimized backend version, if available."""
    if _BACKEND is None:
        return None
    try:
        return metadata.version(_BACKEND_NAME)
    except metadata.PackageNotFoundError:
        version = getattr(_BACKEND, "__version__", None)
        return version if isinstance(version, str) else None


def installed() -> bool:
    """Return whether miniproto installed an optimized event-loop policy."""
    return _INSTALLED


def install_error() -> Exception | None:
    """Return the suppressed auto-install error, if any."""
    return _INSTALL_ERROR


def install() -> bool:
    """Install the optimized event-loop policy when the platform backend is available."""
    global _INSTALLED, _INSTALL_ERROR
    if _BACKEND is None:
        return False
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            install_func = getattr(_BACKEND, "install", None)
            if install_func is None:
                return False
            install_func()
    except RuntimeError as exc:
        _INSTALL_ERROR = exc
        return False
    _INSTALLED = True
    _INSTALL_ERROR = None
    return True


def new_event_loop() -> asyncio.AbstractEventLoop:
    """Create an optimized event loop when available, otherwise create a stdlib loop."""
    if _BACKEND is None:
        return asyncio.new_event_loop()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        factory = getattr(_BACKEND, "new_event_loop", None)
        if factory is not None:
            return factory()
        policy_factory = getattr(_BACKEND, "EventLoopPolicy", None)
        if policy_factory is None:
            return asyncio.new_event_loop()
        return policy_factory().new_event_loop()


def run[T](main: Coroutine[Any, Any, T], *, debug: bool | None = None) -> T:
    """Run a coroutine on the optimized backend when it is installed."""
    if _BACKEND is not None:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            run_func = getattr(_BACKEND, "run", None)
        if run_func is not None:
            return run_func(main, debug=debug)
        loop_factory: Callable[[], asyncio.AbstractEventLoop] | None = new_event_loop
    else:
        loop_factory = None
    with asyncio.Runner(debug=debug, loop_factory=loop_factory) as runner:
        return runner.run(main)


def _load_backend() -> ModuleType | None:
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            return import_module(_BACKEND_NAME)
    except ModuleNotFoundError as exc:
        if exc.name != _BACKEND_NAME:
            raise
        return None


_BACKEND = _load_backend()
install()

__all__ = [
    "backend",
    "backend_name",
    "backend_version",
    "install",
    "install_error",
    "installed",
    "new_event_loop",
    "run",
]
