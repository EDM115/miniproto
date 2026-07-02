from __future__ import annotations

import os
from collections.abc import Iterable, Mapping
from typing import Protocol

from miniproto.session.models import DCOption


class RawDCOption(Protocol):
    id: int
    ip_address: str
    port: int
    ipv6: bool
    media_only: bool
    tcpo_only: bool
    static: bool
    secret: bytes | None


TEST_DC_OPTIONS: tuple[DCOption, ...] = tuple(
    DCOption(id=dc_id, ip_address=f"test-dc-{dc_id}.telegram.local", port=443, static=True)
    for dc_id in range(1, 6)
)

PRODUCTION_DC_OPTIONS: tuple[DCOption, ...] = (
    DCOption(id=1, ip_address="149.154.175.50", port=443, static=True),
    DCOption(id=2, ip_address="149.154.167.50", port=443, static=True),
    DCOption(id=2, ip_address="149.154.167.51", port=443, static=True),
    DCOption(id=2, ip_address="95.161.76.100", port=443, static=True),
    DCOption(id=3, ip_address="149.154.175.100", port=443, static=True),
    DCOption(id=4, ip_address="149.154.167.91", port=443, static=True),
    DCOption(id=5, ip_address="149.154.171.5", port=443, static=True),
)


def dc_options_from_env(environ: Mapping[str, str] | None = None) -> tuple[DCOption, ...]:
    source = os.environ if environ is None else environ
    options: list[DCOption] = []
    for dc_id in range(1, 6):
        value = source.get(f"MINIPROTO_TEST_DC{dc_id}")
        if not value:
            continue
        host, port = _parse_endpoint(value, field=f"MINIPROTO_TEST_DC{dc_id}")
        options.append(DCOption(id=dc_id, ip_address=host, port=port, static=True))
    return tuple(options)


def default_dc_options(*, test_mode: bool) -> tuple[DCOption, ...]:
    if test_mode:
        env_options = dc_options_from_env()
        return env_options or TEST_DC_OPTIONS
    return PRODUCTION_DC_OPTIONS


def dc_options_from_raw(raw_options: Iterable[RawDCOption]) -> tuple[DCOption, ...]:
    options: list[DCOption] = []
    for raw in raw_options:
        options.append(
            DCOption(
                id=int(raw.id),
                ip_address=str(raw.ip_address),
                port=int(raw.port),
                ipv6=bool(getattr(raw, "ipv6", False)),
                media_only=bool(getattr(raw, "media_only", False)),
                tcpo_only=bool(getattr(raw, "tcpo_only", False)),
                static=bool(getattr(raw, "static", False)),
                secret=getattr(raw, "secret", None),
            )
        )
    return tuple(options)


def select_dc_option(
    options: Iterable[DCOption],
    dc_id: int,
    *,
    prefer_ipv6: bool = False,
    allow_media_only: bool = False,
) -> DCOption:
    candidates = [option for option in options if option.id == dc_id]
    if not candidates:
        raise ValueError(f"no DC option for dc_id={dc_id}")
    filtered = [option for option in candidates if allow_media_only or not option.media_only]
    if not filtered:
        filtered = candidates
    if prefer_ipv6:
        for option in filtered:
            if option.ipv6:
                return option
    for option in filtered:
        if not option.ipv6:
            return option
    return filtered[0]


def _parse_endpoint(value: str, *, field: str) -> tuple[str, int]:
    if value.startswith("["):
        host, separator, rest = value[1:].partition("]:")
        if separator != "]:":
            raise ValueError(f"{field} must use host:port or [ipv6]:port")
        port_text = rest
    else:
        host, separator, port_text = value.rpartition(":")
        if not separator:
            raise ValueError(f"{field} must use host:port")
    if not host:
        raise ValueError(f"{field} host must not be empty")
    try:
        port = int(port_text)
    except ValueError as exc:
        raise ValueError(f"{field} port must be an integer") from exc
    if not 0 < port < 65536:
        raise ValueError(f"{field} port must be between 1 and 65535")
    return host, port
