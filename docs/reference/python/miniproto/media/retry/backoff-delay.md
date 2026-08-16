---
title: "miniproto.media.retry.backoff_delay"
description: "Calculate a jittered exponential delay for a transient non-flood retry."
generated: true
editUrl: false
language: "python"
kind: "function"
qualified_name: "miniproto.media.retry.backoff_delay"
source_path: "src/miniproto/media/retry.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/media/retry.py#L12"
module: "miniproto.media.retry"
---

## `miniproto.media.retry.backoff_delay`

```python
backoff_delay(attempt: int, *, base: float = DEFAULT_BACKOFF_BASE, cap: float = DEFAULT_BACKOFF_CAP, jitter: float = DEFAULT_BACKOFF_JITTER) -> float
```

Calculate a jittered exponential delay for a transient non-flood retry.

**Parameters:**

- **attempt** (<code>[int](#int)</code>) – Zero-based failed attempt; ``0`` produces approximately ``base`` seconds.
- **base** (<code>[float](#float)</code>) – Initial delay in seconds; defaults to :data:`DEFAULT_BACKOFF_BASE`.
- **cap** (<code>[float](#float)</code>) – Maximum unjittered delay in seconds; defaults to :data:`DEFAULT_BACKOFF_CAP`.
- **jitter** (<code>[float](#float)</code>) – Symmetric random fraction applied to the capped delay; defaults to :data:`DEFAULT_BACKOFF_JITTER`.

**Returns:**

- <code>[float](#float)</code> – A non-negative sleep duration in seconds. Randomization prevents synchronized retries.
