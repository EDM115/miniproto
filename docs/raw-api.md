# Raw API

Status: generated Telegram Schema Layer 223 surface with implemented runtime transport support and lazy raw loading.

## Source

The raw API classes are generated from the official Telegram JSON schema at [https://core.telegram.org/schema/json](https://core.telegram.org/schema/json). The pinned canonical schema lives at `tools/schema/schema.json` with SHA-256 `7440a69d834e495fb0be30cb4ee0e4dd101199f83574aa5ece64598c5b8ea1ac`. A mirrored TL schema is kept at `tools/schema/schema.tl` with SHA-256 `e91d38be1709d0af9ae28bfd41ffa0c04e5092bc62dba0ad560f1660ca098ef5`.

RPC error metadata is generated from Telegram's error database linked from [https://core.telegram.org/api/errors](https://core.telegram.org/api/errors). The pinned JSON lives at `tools/schema/rpc-errors.json` with SHA-256 `7cb5ea5c8574e61b300c538e75290b742760d595a879552a5d0b613cd9fdf029`.

## Generated Surface

- Constructors: 1546
- Functions: 757
- RPC errors: 818
- RPC errors layer: 227
- Latest changelog layer observed during update: 225
- Generated files: src/miniproto/raw/base.py, src/miniproto/raw/types.py, src/miniproto/raw/types.pyi, src/miniproto/raw/functions.py, src/miniproto/raw/functions.pyi, src/miniproto/raw/_registry.py, src/miniproto/raw/_types_shards/*.py, src/miniproto/raw/_function_shards/*.py, src/miniproto/raw/errors.py, docs/raw-api.md

## Usage Shape

```python
from miniproto.raw import functions

request = functions.help.GetConfig()
```

## Lazy Loading and Typing

Facade imports stay lightweight: they load generated facades and the registry, not implementation shards. Requested symbols load and cache their generated shard on first attribute, namespace, constructor-ID, or name-map lookup. Mapping and sequence iteration may realize classes as needed. The `.pyi` facades retain static type declarations. Update generated artifacts only through `python -m tools.schema.generate`.

## Current Runtime Scope

The runtime handles binary TL primitive encoding, generated object serialization/deserialization, flags, vectors, boxed constructors, RPC error metadata, gzip-packed payloads, message containers, transport framing, and RPC response correlation.

## Current Limits

Transport-level quick-ack frame decoding and its fake-server/live-trace validation remain deferred.

## Samples

Early generated type constructors include: boolFalse, boolTrue, true, vector, error, null, inputPeerEmpty, inputPeerSelf.

Early generated functions include: invokeAfterMsg, invokeAfterMsgs, auth.sendCode, auth.signUp, auth.signIn, auth.logOut, auth.resetAuthorizations, auth.exportAuthorization.
