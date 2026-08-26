"""Bootstrap and persist the MTProto authorization key for a session."""

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
    """Exchange unencrypted MTProto authorization packets over one transport.

    Args:
        endpoint: Telegram data-center address to contact.
        config: Client transport configuration used when opening the connection.
    """

    def __init__(self, endpoint: ConnectionEndpoint, config: ClientConfig) -> None:
        """Store connection details and defer opening the transport until first use.

        Args:
            endpoint: Telegram data-center address to contact.
            config: Transport configuration used to open the connection.
        """
        self.endpoint = endpoint
        self.config = config
        self._transport: Transport | None = None
        self._last_msg_id = 0

    async def send_unencrypted(self, body: bytes) -> bytes:
        """Send one unencrypted MTProto body and return its response body.

        Args:
            body: Serialized MTProto authorization request.

        Returns:
            The decoded unencrypted response body.

        Raises:
            ConnectionError: If the server sends a quick ACK instead of a response packet.
        """
        if self._transport is None:
            self._transport = await open_transport(self.endpoint, self.config.transport)
        msg_id = self._next_msg_id()
        await self._transport.send(encode_unencrypted_message(msg_id, body))
        packet = await self._transport.recv()
        if not isinstance(packet, bytes):
            raise ConnectionError("unexpected quick ACK during unencrypted auth exchange")
        return bytes(decode_unencrypted_message(packet).body)

    async def close(self) -> None:
        """Close the opened transport, if any and make the instance reusable."""
        transport = self._transport
        self._transport = None
        if transport is not None:
            await transport.close()

    def _next_msg_id(self) -> int:
        """Return a monotonically increasing, four-byte-aligned MTProto message ID."""
        candidate = int(time.time() * 2**32) & ~3
        if candidate <= self._last_msg_id:
            candidate = self._last_msg_id + 4
        self._last_msg_id = candidate
        return candidate


async def ensure_auth_key(config: ClientConfig, storage: SessionStorage) -> None:
    """Ensure that ``storage`` contains a usable MTProto key and DC options.

    Existing keys are preserved. When no key is present, this performs Telegram's
    unencrypted authorization-key exchange, then atomically stores its key, salt,
    server-time offset and resolved data-center options.

    Args:
        config: Client configuration, including target DC and test-mode selection.
        storage: Mutable session store to inspect and update.

    Raises:
        ValueError: If the configured DC or Telegram key-exchange response is invalid.
        ConnectionError: If the unencrypted exchange receives an unexpected quick ACK.
    """
    record = load_session_record(await storage.load(), config.dc_id)
    dc_options = record.dc_options or default_dc_options(test_mode=config.test_mode)
    dc_id = record.dc_id or config.dc_id
    if record.auth_key is not None:
        if record.dc_options:
            return

        def persist_options(payload):
            """Add fallback DC options without overwriting a concurrent update.

            Args:
                payload: Latest stored session mapping supplied by ``storage.mutate``.
            """
            current = load_session_record(payload, config.dc_id)
            if current.dc_options:
                return current
            return replace(current, dc_options=dc_options)

        await storage.mutate(persist_options)
        return
    option = select_dc_option(dc_options, dc_id)
    transport = UnencryptedAuthKeyTransport(ConnectionEndpoint(option.ip_address, option.port), config)
    try:
        result = await AuthKeyExchange(
            transport,
            dc_id=dc_id,
            rsa_keys=telegram_rsa_public_keys(test_mode=config.test_mode),
            test_mode=config.test_mode,
        ).create_auth_key()
    finally:
        await transport.close()

    def persist_auth(payload):
        """Persist the completed exchange while retaining concurrent session data.

        Args:
            payload: Latest stored session mapping supplied by ``storage.mutate``.
        """
        current = load_session_record(payload, config.dc_id)
        metadata = dict(current.metadata)
        metadata["server_salt"] = result.server_salt
        metadata["time_offset"] = result.time_offset
        return replace(
            current,
            dc_id=result.dc_id,
            auth_key=AuthKey(
                dc_id=result.dc_id,
                key=result.auth_key,
                key_id=int.from_bytes(auth_key_id(result.auth_key), "little", signed=False),
            ),
            dc_options=current.dc_options or dc_options,
            metadata=metadata,
        )

    await storage.mutate(persist_auth)


def telegram_rsa_public_keys(*, test_mode: bool) -> tuple[RSAKey, ...]:
    """Return Telegram's trusted RSA public keys for the selected environment.

    Args:
        test_mode: Select Telegram's test-server keys instead of production keys.

    Returns:
        Parsed public keys whose fingerprints may be advertised by Telegram.
    """
    return tuple(rsa_key_from_pem(pem) for pem in (_TEST_RSA_PUBLIC_KEYS if test_mode else _PRODUCTION_RSA_PUBLIC_KEYS))


def rsa_key_from_pem(pem: str) -> RSAKey:
    """Parse the minimal PKCS#1 RSA public-key DER payload embedded in ``pem``.

    Args:
        pem: ASCII PEM text containing an RSA public-key DER payload.
    """
    lines = [line.strip() for line in pem.splitlines() if line and "-----" not in line]
    der = base64.b64decode("".join(lines), validate=True)
    offset = _read_tag(der, 0, 0x30)[1]
    modulus, offset = _read_integer(der, offset)
    exponent, offset = _read_integer(der, offset)
    if offset != len(der):
        raise ValueError("RSA public key has trailing DER data")
    return RSAKey(modulus=modulus, exponent=exponent)


def _read_tag(data: bytes, offset: int, expected_tag: int) -> tuple[bytes, int]:
    """Read a DER TLV value and return its content with its content offset.

    Args:
        data: Complete DER byte sequence being parsed.
        offset: Byte offset of the expected tag.
        expected_tag: ASN.1 tag byte required at ``offset``.
    """
    if offset >= len(data) or data[offset] != expected_tag:
        raise ValueError("unexpected DER tag in RSA public key")
    length, content_offset = _read_length(data, offset + 1)
    end = content_offset + length
    if end > len(data):
        raise ValueError("DER length exceeds RSA public key data")
    return data[content_offset:end], content_offset


def _read_integer(data: bytes, offset: int) -> tuple[int, int]:
    """Read one positive DER INTEGER and the offset following its content.

    Args:
        data: Complete DER byte sequence being parsed.
        offset: Byte offset of the INTEGER tag.
    """
    value, content_offset = _read_tag(data, offset, 0x02)
    next_offset = content_offset + len(value)
    return int.from_bytes(value.lstrip(b"\x00") or b"\x00", "big", signed=False), next_offset


def _read_length(data: bytes, offset: int) -> tuple[int, int]:
    """Decode a bounded DER definite-length field at ``offset``.

    Args:
        data: Complete DER byte sequence being parsed.
        offset: Byte offset of the first DER length octet.
    """
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
