"""Pure Python fallbacks for the bundled native extension."""


def native_available() -> bool:
    return False


def xor_bytes(left: bytes, right: bytes) -> bytes:
    if len(left) != len(right):
        raise ValueError("xor inputs must have the same length")

    return bytes(a ^ b for a, b in zip(left, right, strict=True))
