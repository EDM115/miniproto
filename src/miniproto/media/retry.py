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
    """Jittered exponential backoff for transient (non-flood) media retries.

    ``attempt`` is the zero-based attempt that just failed, so the first retry
    sleeps roughly ``base`` seconds and each further retry doubles it up to ``cap``,
    with +/- ``jitter`` (fraction) of randomization to avoid thundering herds.
    """
    delay = min(cap, base * (2 ** max(0, attempt)))
    spread = delay * jitter
    jittered = delay + random.uniform(-spread, spread)  # noqa: S311 - jitter, not crypto
    return max(0.0, jittered)


__all__ = ["backoff_delay"]
