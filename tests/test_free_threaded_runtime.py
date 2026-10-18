from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]


def test_native_runtime_import_and_protected_sessions_do_not_require_cryptography() -> None:
    script = r"""
import importlib.abc
import sys


class BlockCryptography(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname == "cryptography" or fullname.startswith("cryptography."):
            raise ModuleNotFoundError("cryptography intentionally blocked", name=fullname)
        return None


sys.meta_path.insert(0, BlockCryptography())

import miniproto
from miniproto import _native

record = miniproto.SessionRecord()
protected = miniproto.export_session_string(record, passphrase="free-threaded acceptance")
assert miniproto.import_session_string(protected, passphrase="free-threaded acceptance") == record
assert _native.native_available()
assert "cryptography" not in sys.modules
"""
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT / "src")
    completed = subprocess.run(  # noqa: S603 - fixed current-interpreter command validates an isolated import.
        [sys.executable, "-I", "-c", script], cwd=ROOT, env=environment, text=True, capture_output=True, check=False
    )

    if "No module named 'miniproto._native'" in completed.stderr:
        pytest.skip("native extension is not built in this source checkout")
    assert completed.returncode == 0, completed.stderr
