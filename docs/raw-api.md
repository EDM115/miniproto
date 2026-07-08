# Raw API

Status: generated documentation stub for Telegram Schema Layer 223.

## Source

The raw API classes are generated from the official Telegram JSON schema at [https://core.telegram.org/schema/json](https://core.telegram.org/schema/json). The pinned canonical schema lives at `tools/schema/schema.json` with SHA-256 `7440a69d834e495fb0be30cb4ee0e4dd101199f83574aa5ece64598c5b8ea1ac`. A mirrored TL schema is kept at `tools/schema/schema.tl` with SHA-256 `e91d38be1709d0af9ae28bfd41ffa0c04e5092bc62dba0ad560f1660ca098ef5`.

RPC error metadata is generated from Telegram's error database linked from [https://core.telegram.org/api/errors](https://core.telegram.org/api/errors). The pinned JSON lives at `tools/schema/rpc-errors.json` with SHA-256 `7cb5ea5c8574e61b300c538e75290b742760d595a879552a5d0b613cd9fdf029`.

## Generated Surface

- Constructors: 1546
- Functions: 757
- RPC errors: 818
- RPC errors layer: 227
- Latest changelog layer observed during update: 225
- Generated files: src/miniproto/raw/base.py, src/miniproto/raw/types.py, src/miniproto/raw/functions.py, src/miniproto/raw/errors.py, docs/raw-api.md

## Usage Shape

```python
from miniproto.raw import functions

request = functions.help.GetConfig()
```

## Current Limits

Phase 4 implements binary TL primitive encoding, generated object serialization/deserialization, flags, vectors, boxed constructors, and RPC error metadata. Gzip payload handling, message containers, transport framing, and RPC response correlation land in later runtime phases.

## Samples

Early generated type constructors include: boolFalse, boolTrue, true, vector, error, null, inputPeerEmpty, inputPeerSelf.

Early generated functions include: invokeAfterMsg, invokeAfterMsgs, auth.sendCode, auth.signUp, auth.signIn, auth.logOut, auth.resetAuthorizations, auth.exportAuthorization.
