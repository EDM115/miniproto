from __future__ import annotations

import base64
import time
from dataclasses import replace

from miniproto.auth.dc import default_dc_options, select_dc_option
from miniproto.auth.key_exchange import AuthKeyExchange, RSAKey
from miniproto.config import ClientConfig
from miniproto.connection.transport import ConnectionEndpoint, Transport, open_transport
from miniproto.crypto.mtproto import auth_key_id
from miniproto.invoke import load_session_record
from miniproto.mtproto.codec import decode_unencrypted_message, encode_unencrypted_message
from miniproto.session.models import AuthKey
from miniproto.session.storage import SessionStorage

_PRODUCTION_RSA_PUBLIC_KEYS = (
    """-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEA6LszBcC1LGzyr992NzE0ieY+BSaOW622Aa9Bd4ZHLl+TuFQ4lo4g
5nKaMBwK/BIb9xUfg0Q29/2mgIR6Zr9krM7HjuIcCzFvDtr+L0GQjae9H0pRB2OO
62cECs5HKhT5DZ98K33vmWiLowc621dQuwKWSQKjWf50XYFw42h21P2KXUGyp2y/
+aEyZ+uVgLLQbRA1dEjSDZ2iGRy12Mk5gpYc397aYp438fsJoHIgJ2lgMv5h7WY9
t6N/byY9Nw9p21Og3AoXSL2q/2IJ1WRUhebgAdGVMlV1fkuOQoEzR7EdpqtQD9Cs
5+bfo3Nhmcyvk5ftB0WkJ9z6bNZ7yxrP8wIDAQAB
-----END RSA PUBLIC KEY-----""",
)

_TEST_RSA_PUBLIC_KEYS = (
    """-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAyMEdY1aR+sCR3ZSJrtztKTKqigvO/vBfqACJLZtS7QMgCGXJ6XIR
yy7mx66W0/sOFa7/1mAZtEoIokDP3ShoqF4fVNb6XeqgQfaUHd8wJpDWHcR2OFwv
plUUI1PLTktZ9uW2WE23b+ixNwJjJGwBDJPQEQFBE+vfmH0JP503wr5INS1poWg/
j25sIWeYPHYeOrFp/eXaqhISP6G+q2IeTaWTXpwZj4LzXq5YOpk4bYEQ6mvRq7D1
aHWfYmlEGepfaYR8Q0YqvvhYtMte3ITnuSJs171+GDqpdKcSwHnd6FudwGO4pcCO
j4WcDuXc2CTHgH8gFTNhp/Y8/SpDOhvn9QIDAQAB
-----END RSA PUBLIC KEY-----""",
)


class UnencryptedAuthKeyTransport:
    def __init__(self, endpoint: ConnectionEndpoint, config: ClientConfig) -> None:
        self.endpoint = endpoint
        self.config = config
        self._transport: Transport | None = None
        self._last_msg_id = 0

    async def send_unencrypted(self, body: bytes) -> bytes:
        if self._transport is None:
            self._transport = await open_transport(self.endpoint, self.config.transport)
        msg_id = self._next_msg_id()
        await self._transport.send(encode_unencrypted_message(msg_id, body))
        return decode_unencrypted_message(await self._transport.recv()).body

    async def close(self) -> None:
        transport = self._transport
        self._transport = None
        if transport is not None:
            await transport.close()

    def _next_msg_id(self) -> int:
        candidate = int(time.time() * 2**32) & ~3
        if candidate <= self._last_msg_id:
            candidate = self._last_msg_id + 4
        self._last_msg_id = candidate
        return candidate


async def ensure_auth_key(config: ClientConfig, storage: SessionStorage) -> None:
    record = load_session_record(await storage.load(), config.dc_id)
    dc_options = record.dc_options or default_dc_options(test_mode=config.test_mode)
    dc_id = record.dc_id or config.dc_id
    if record.auth_key is not None:
        if record.dc_options:
            return
        await storage.save(replace(record, dc_options=dc_options))
        return
    option = select_dc_option(dc_options, dc_id)
    transport = UnencryptedAuthKeyTransport(
        ConnectionEndpoint(option.ip_address, option.port), config
    )
    try:
        result = await AuthKeyExchange(
            transport,
            dc_id=dc_id,
            rsa_keys=telegram_rsa_public_keys(test_mode=config.test_mode),
            test_mode=config.test_mode,
        ).create_auth_key()
    finally:
        await transport.close()
    metadata = dict(record.metadata)
    metadata["server_salt"] = result.server_salt
    metadata["time_offset"] = result.time_offset
    await storage.save(
        replace(
            record,
            dc_id=result.dc_id,
            auth_key=AuthKey(
                dc_id=result.dc_id,
                key=result.auth_key,
                key_id=int.from_bytes(auth_key_id(result.auth_key), "little", signed=False),
            ),
            dc_options=dc_options,
            metadata=metadata,
        )
    )


def telegram_rsa_public_keys(*, test_mode: bool) -> tuple[RSAKey, ...]:
    return tuple(
        _rsa_key_from_pem(pem)
        for pem in (_TEST_RSA_PUBLIC_KEYS if test_mode else _PRODUCTION_RSA_PUBLIC_KEYS)
    )


def _rsa_key_from_pem(pem: str) -> RSAKey:
    lines = [line.strip() for line in pem.splitlines() if line and "-----" not in line]
    der = base64.b64decode("".join(lines), validate=True)
    offset = _read_tag(der, 0, 0x30)[1]
    modulus, offset = _read_integer(der, offset)
    exponent, offset = _read_integer(der, offset)
    if offset != len(der):
        raise ValueError("RSA public key has trailing DER data")
    return RSAKey(modulus=modulus, exponent=exponent)


def _read_tag(data: bytes, offset: int, expected_tag: int) -> tuple[bytes, int]:
    if offset >= len(data) or data[offset] != expected_tag:
        raise ValueError("unexpected DER tag in RSA public key")
    length, content_offset = _read_length(data, offset + 1)
    end = content_offset + length
    if end > len(data):
        raise ValueError("DER length exceeds RSA public key data")
    return data[content_offset:end], content_offset


def _read_integer(data: bytes, offset: int) -> tuple[int, int]:
    value, content_offset = _read_tag(data, offset, 0x02)
    next_offset = content_offset + len(value)
    return int.from_bytes(value.lstrip(b"\x00") or b"\x00", "big", signed=False), next_offset


def _read_length(data: bytes, offset: int) -> tuple[int, int]:
    if offset >= len(data):
        raise ValueError("missing DER length")
    first = data[offset]
    offset += 1
    if first < 0x80:
        return first, offset
    size = first & 0x7F
    if size == 0 or size > 4 or offset + size > len(data):
        raise ValueError("unsupported DER length")
    return int.from_bytes(data[offset : offset + size], "big", signed=False), offset + size


__all__ = ["UnencryptedAuthKeyTransport", "ensure_auth_key", "telegram_rsa_public_keys"]
