from __future__ import annotations

from pathlib import Path

import pytest
from tools.bench.benchmark_multi_session_download import (
    MIB,
    duplicate_auth_key_groups,
    parse_args,
    plan_contiguous_ranges,
    resolve_session_paths,
)


def test_explicit_session_paths_come_from_cli() -> None:
    args = parse_args(
        [
            "--actor",
            "user",
            "--file-id",
            "mpf1_test",
            "--session",
            ".tmp/a.sqlite",
            "--session",
            ".tmp/b.sqlite",
        ],
        {},
    )

    assert resolve_session_paths(args, {}) == (Path(".tmp/a.sqlite"), Path(".tmp/b.sqlite"))


def test_session_paths_can_come_from_env() -> None:
    args = parse_args(
        ["--actor", "bot", "--file-id", "mpf1_test"],
        {"MINIPROTO_MULTI_SESSION_DOWNLOAD_SESSIONS": ".tmp/a.sqlite;.tmp/b.sqlite,.tmp/c.sqlite"},
    )

    assert resolve_session_paths(args, {}) == (
        Path(".tmp/a.sqlite"),
        Path(".tmp/b.sqlite"),
        Path(".tmp/c.sqlite"),
    )


def test_default_session_paths_follow_actor_client_count_and_dc() -> None:
    args = parse_args(
        ["--actor", "bot", "--file-id", "mpf1_test", "--clients", "3", "--dc-id", "4"], {}
    )

    assert resolve_session_paths(args, {}) == (
        Path(".tmp/miniproto-multi-session-download-bot-0-dc4.sqlite"),
        Path(".tmp/miniproto-multi-session-download-bot-1-dc4.sqlite"),
        Path(".tmp/miniproto-multi-session-download-bot-2-dc4.sqlite"),
    )


def test_contiguous_plan_splits_on_one_mib_boundaries_and_keeps_tail_on_last_worker() -> None:
    ranges = plan_contiguous_ranges(10 * MIB + 512 * 1024, requested_workers=3)

    assert [(item.index, item.offset, item.limit) for item in ranges] == [
        (0, 0, 4 * MIB),
        (1, 4 * MIB, 3 * MIB),
        (2, 7 * MIB, 3 * MIB + 512 * 1024),
    ]


def test_contiguous_plan_uses_fewer_workers_when_file_is_smaller_than_worker_count() -> None:
    ranges = plan_contiguous_ranges(2 * MIB + 512 * 1024, requested_workers=4)

    assert [(item.index, item.offset, item.limit) for item in ranges] == [
        (0, 0, MIB),
        (1, MIB, MIB + 512 * 1024),
    ]


def test_duplicate_auth_key_groups_ignore_missing_values() -> None:
    assert duplicate_auth_key_groups((None, "aaa", "bbb", "aaa", None, "bbb")) == {
        "aaa": (1, 3),
        "bbb": (2, 5),
    }


def test_parser_rejects_non_positive_client_count() -> None:
    with pytest.raises(SystemExit):
        parse_args(["--actor", "user", "--file-id", "mpf1_test", "--clients", "0"], {})
