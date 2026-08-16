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
_STDLIB_DEBUG_FALLBACK_THROUGH = {
    # https://github.com/MagicStack/uvloop/issues/715
    "uvloop": (0, 22, 1),
    "winloop": (0, 6, 3),
}


def backend_name() -> str:
    """Return the optimized event-loop package selected for this platform.

    Returns:
        ``winloop`` on Windows and ``uvloop`` on every other platform. The name
        is selected without importing or installing the package.
    """
    return _BACKEND_NAME


def backend() -> ModuleType | None:
    """Load and return the optimized backend module when it is available.

    Returns:
        The cached import of the platform-selected backend, or ``None`` when
        that package is not installed.

    Raises:
        Exception: Propagates an import failure raised inside the backend rather
            than treating a broken installation as unavailable.
    """
    return _load_backend()


def backend_version() -> str | None:
    """Return the installed optimized backend version, if available.

    Returns:
        Distribution metadata, then the backend's ``__version__`` fallback, or
        ``None`` when no backend is importable or exposes a version.

    Raises:
        Exception: Propagates failures while importing the selected backend.
    """
    selected_backend = _load_backend()
    if selected_backend is None:
        return None
    try:
        return metadata.version(_BACKEND_NAME)
    except metadata.PackageNotFoundError:
        version = getattr(selected_backend, "__version__", None)
        return version if isinstance(version, str) else None


def optimized_available() -> bool:
    """Return whether the platform's optimized event-loop backend can be loaded.

    Raises:
        Exception: Propagates import failures other than an absent selected
            backend package.
    """
    return _load_backend() is not None


def installed() -> bool:
    """Return whether :func:`install` last installed a legacy backend policy.

    This flag does not probe asyncio's current policy and remains false when
    applications use :func:`run` or :func:`new_event_loop` instead.
    """
    return _INSTALLED


def install_error() -> Exception | None:
    """Return the most recent explicit-install or backend-load error, if any.

    Returns:
        The stored exception from :func:`install` or backend import, otherwise
        ``None``. Reading this value never retries installation.
    """
    return _INSTALL_ERROR or _BACKEND_LOAD_ERROR


def install() -> bool:
    """Install the backend's deprecated global policy on Python before 3.16.

    Returns:
        ``True`` after the selected backend's legacy ``install`` hook succeeds;
        ``False`` if no backend/hook is available, installation fails, or Python
        3.16+ rejects policy installation.

    Raises:
        DeprecationWarning: Always warns because policy installation is a
            deprecated asyncio integration path.

    Notes:
        This process-global operation is not safe to race with other tasks that
        create loops. Prefer :func:`run` or ``asyncio.Runner`` with
        :func:`new_event_loop` for scoped lifecycle control.
    """
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
            _INSTALL_ERROR = RuntimeError(f"{_BACKEND_NAME} does not expose a legacy event-loop policy installer")
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
    """Create and register an optimized loop, falling back to asyncio's loop.

    Returns:
        A newly created event loop, also made current with
        :func:`asyncio.set_event_loop` for the calling thread.

    Raises:
        Exception: Propagates a selected backend import failure other than a
            missing package.

    Notes:
        Callers own the returned loop's lifecycle. Use it as an
        ``asyncio.Runner`` factory or close it after standalone use.
    """
    selected_backend = _load_backend()
    factory = getattr(selected_backend, "new_event_loop", None) if selected_backend else None
    loop = factory() if callable(factory) else asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop


def run[T](main: Coroutine[Any, Any, T], *, debug: bool | None = None) -> T:
    """Run one coroutine with an optimized ``asyncio.Runner`` when possible.

    Args:
        main: The coroutine to execute until it returns or raises.
        debug: Passed to ``asyncio.Runner``. ``None`` preserves asyncio's
            default; known backend/debug incompatibilities use the stdlib loop.

    Returns:
        The coroutine's result.

    Raises:
        BaseException: Any exception raised by ``main`` or backend setup.

    Notes:
        The runner creates, closes, and clears its loop. It must not be called
        while another event loop is running in this thread.
    """
    loop_factory = None if _requires_stdlib_debug_runner(debug) else new_event_loop
    try:
        with asyncio.Runner(debug=debug, loop_factory=loop_factory) as runner:
            return runner.run(main)
    finally:
        asyncio.set_event_loop(None)


def _requires_stdlib_debug_runner(debug: bool | None) -> bool:
    """Return whether debug mode needs asyncio's loop for this backend version.

    Args:
        debug: Requested ``asyncio.Runner`` debug setting.
    """
    if not debug:
        return False
    fallback_through = _STDLIB_DEBUG_FALLBACK_THROUGH.get(_BACKEND_NAME)
    if fallback_through is None:
        return False
    try:
        installed_version = metadata.version(_BACKEND_NAME)
    except metadata.PackageNotFoundError:
        return False
    numeric_parts = tuple(
        int(digits)
        for part in installed_version.split(".")[:3]
        if (digits := "".join(character for character in part if character.isdigit()))
    )
    return numeric_parts <= fallback_through


def _load_backend() -> ModuleType | None:
    """Import and cache the selected backend, distinguishing absence from breakage."""
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
