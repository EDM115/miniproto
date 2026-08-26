"""Retry-delay calculation for transient media-transfer failures."""

from __future__ import annotations

import random

DEFAULT_BACKOFF_BASE = 0.5
DEFAULT_BACKOFF_CAP = 10.0
DEFAULT_BACKOFF_JITTER = 0.2


def backoff_delay(
    attempt: int,
    *,
    base: float = DEFAULT_BACKOFF_BASE,
    cap: float = DEFAULT_BACKOFF_CAP,
    jitter: float = DEFAULT_BACKOFF_JITTER,
) -> float:
    """Calculate a jittered exponential delay for a transient non-flood retry.

    Args:
        attempt: Zero-based failed attempt; ``0`` produces approximately ``base`` seconds.
        base: Initial delay in seconds; defaults to :data:`DEFAULT_BACKOFF_BASE`.
        cap: Maximum unjittered delay in seconds; defaults to :data:`DEFAULT_BACKOFF_CAP`.
        jitter: Symmetric random fraction applied to the capped delay; defaults to :data:`DEFAULT_BACKOFF_JITTER`.

    Returns:
        A non-negative sleep duration in seconds. Randomization prevents synchronized retries.
    """
    delay = min(cap, base * (2 ** max(0, attempt)))
    spread = delay * jitter
    jittered = delay + random.uniform(-spread, spread)  # noqa: S311 - jitter, not crypto
    return max(0.0, jittered)


__all__ = ["backoff_delay"]
