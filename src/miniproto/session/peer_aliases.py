"""Shared canonical username handling for peer observations and lookup indexes."""

from __future__ import annotations

from collections.abc import Iterable, Mapping


def normalize_username(value: str) -> str | None:
    """Canonicalize @handles and t.me URLs, returning ``None`` for empty input.

    Args:
        value: User-entered handle or supported t.me URL.
    """
    rendered = value.strip()
    for prefix in ("https://t.me/", "http://t.me/", "t.me/"):
        if rendered.casefold().startswith(prefix):
            rendered = rendered[len(prefix) :]
            break
    rendered = rendered.removeprefix("@").split("/", 1)[0].strip().casefold()
    return rendered or None


def peer_usernames(username: str | None, raw: Mapping[str, object] | None) -> tuple[str, ...]:
    """Return unique normalized primary and extra usernames carried by an entry.

    Args:
        username: Optional primary username.
        raw: Optional raw fields containing an extra username collection.
    """
    values: list[str] = []
    primary = normalize_username(username or "")
    if primary is not None:
        values.append(primary)
    raw_usernames = raw.get("usernames", ()) if raw is not None else ()
    if isinstance(raw_usernames, Iterable) and not isinstance(raw_usernames, str | bytes):
        for raw_username in raw_usernames:
            normalized = normalize_username(str(raw_username))
            if normalized is not None and normalized not in values:
                values.append(normalized)
    return tuple(values)
