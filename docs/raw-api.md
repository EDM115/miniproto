# Raw API

Status: generated documentation stub for Telegram Layer 214.

## Source

The raw API classes are generated from the official Telegram TL schema at [https://core.telegram.org/schema](https://core.telegram.org/schema). The pinned schema lives at `tools/schema/schema.tl` with SHA-256 `74c5d1aea2997b179283e4069a0019f4c09f5cffda665b3a7083a8bf0d071517`.

RPC error metadata is generated from Telegram's error database linked from [https://core.telegram.org/api/errors](https://core.telegram.org/api/errors). The pinned JSON lives at `tools/schema/rpc-errors.json` with SHA-256 `de6aa3cbdb92f1bda9562964ff1312abce0b3db7f966b7e03440193b569f0e0f`.

## Generated Surface

- Constructors: 1479
- Functions: 727
- RPC errors: 753
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

Early generated functions include: invokeAfterMsg, invokeAfterMsgs, initConnection, invokeWithLayer, invokeWithoutUpdates, invokeWithMessagesRange, invokeWithTakeout, invokeWithBusinessConnection.
