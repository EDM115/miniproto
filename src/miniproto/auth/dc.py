"""Normalize and select Telegram data-center connection options."""

from __future__ import annotations

import os
from collections.abc import Iterable, Mapping
from typing import Protocol

from miniproto.session.models import DCOption


class RawDCOption(Protocol):
    """Structural interface for raw Telegram ``dcOption`` values."""

    id: int
    ip_address: str
    port: int
    ipv6: bool
    media_only: bool
    cdn: bool
    tcpo_only: bool
    static: bool
    secret: bytes | None


TEST_DC_OPTIONS: tuple[DCOption, ...] = tuple(
    DCOption(id=dc_id, ip_address=f"test-dc-{dc_id}.telegram.local", port=443, static=True) for dc_id in range(1, 6)
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
    """Read local test-DC overrides from environment-style mappings.

    Args:
        environ: Mapping to read instead of :data:`os.environ`; defaults to the process environment.

    Returns:
        Static options for populated ``MINIPROTO_TEST_DC1`` through ``MINIPROTO_TEST_DC5`` entries.

    Raises:
        ValueError: If an override is not a valid ``host:port`` or ``[ipv6]:port`` endpoint.
    """
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
    """Return test overrides/defaults or the built-in production DC endpoints.

    Args:
        test_mode: Whether the client will connect to Telegram's test environment.

    Returns:
        Ordered static connection options suitable for the selected environment.
    """
    if test_mode:
        env_options = dc_options_from_env()
        return env_options or TEST_DC_OPTIONS
    return PRODUCTION_DC_OPTIONS


def dc_options_from_raw(raw_options: Iterable[RawDCOption]) -> tuple[DCOption, ...]:
    """Convert raw Telegram DC options to immutable session-model options.

    Args:
        raw_options: Decoded Telegram configuration options.

    Returns:
        Equivalent session options with optional raw flags normalized to booleans.
    """
    options: list[DCOption] = []
    for raw in raw_options:
        options.append(
            DCOption(
                id=int(raw.id),
                ip_address=str(raw.ip_address),
                port=int(raw.port),
                ipv6=bool(getattr(raw, "ipv6", False)),
                media_only=bool(getattr(raw, "media_only", False)),
                cdn=bool(getattr(raw, "cdn", False)),
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
    require_cdn: bool = False,
) -> DCOption:
    """Choose the best endpoint for a data center.

    Args:
        options: Candidate connection options.
        dc_id: Required Telegram data-center identifier.
        prefer_ipv6: Prefer an IPv6 candidate when one is available.
        allow_media_only: Permit endpoints reserved for media traffic.
        require_cdn: Restrict candidates to endpoints explicitly marked as CDN servers.

    Returns:
        A non-media endpoint when possible, otherwise the best available candidate.

    Raises:
        ValueError: If ``options`` has no endpoint for ``dc_id``.
    """
    candidates = [option for option in options if option.id == dc_id]
    if require_cdn:
        candidates = [option for option in candidates if option.cdn]
    if not candidates:
        kind = "CDN DC option" if require_cdn else "DC option"
        raise ValueError(f"no {kind} for dc_id={dc_id}")
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
    """Parse a configured hostname/port endpoint, including bracketed IPv6 literals.

    Args:
        value: Raw ``host:port`` or ``[ipv6]:port`` configuration value.
        field: Environment/configuration field name included in validation errors.
    """
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
