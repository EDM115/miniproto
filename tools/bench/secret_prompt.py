"""Non-echoing terminal input for opted-in live authentication prompts."""

from __future__ import annotations

import getpass
import warnings


def prompt_secret(prompt: str) -> str:
    """Read a credential without allowing a fallback to visible terminal input.

    Args:
        prompt: Public label displayed before reading the credential.

    Returns:
        The entered value with its whitespace preserved.

    Raises:
        RuntimeError: If the terminal cannot hide the input.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("error", getpass.GetPassWarning)
        try:
            return getpass.getpass(prompt)
        except getpass.GetPassWarning:
            raise RuntimeError(
                "Cannot hide terminal input, use a terminal that supports hidden credential entry"
            ) from None
