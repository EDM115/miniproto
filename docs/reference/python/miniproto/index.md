---
title: "miniproto"
description: "Public API for miniproto."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto"
source_path: "src/miniproto/__init__.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/__init__.py"
module: "miniproto"
---

## `miniproto`

Public API for miniproto.

## Public objects

- [`event_loop`](./event_loop/) — Explicit optimized asyncio event-loop selection.
- [`AuthKeyExchange`](./auth/key_exchange/authkeyexchange/) — Perform Telegram's RSA- and DH-protected MTProto authorization handshake.
- [`AuthKeyExchangeResult`](./auth/key_exchange/authkeyexchangeresult/) — Authenticated MTProto key material and metadata produced by an exchange.
- [`AuthService`](./auth/service/authservice/) — Run sign-in and data-center authorization flows for one client session.
- [`Client`](./client/client/) — Async client facade for MTProto operations.
- [`ClientConfig`](./config/clientconfig/) — Immutable client configuration for authentication, session storage, RPCs, updates, and media.
- [`DeviceInfo`](./config/deviceinfo/) — Application and device identity sent when initializing a Telegram session.
- [`TransportConfig`](./config/transportconfig/) — Connection transport settings with validated timeouts and payload limits.
- [`UpdateQueueOverflowPolicy`](./config/updatequeueoverflowpolicy/) — Public attribute `miniproto.config.UpdateQueueOverflowPolicy`.
- [`QuickAckReceipt`](./connection/sender/quickackreceipt/) — Early transport-acknowledgement metadata for one encrypted send attempt.
- [`AmbiguousRpcResult`](./errors/ambiguousrpcresult/) — The transport failed after an RPC may already have reached Telegram.
- [`AuthError`](./errors/autherror/) — Base exception for authentication and authorization flow failures.
- [`AuthKeyNotFound`](./errors/authkeynotfound/) — Authentication key is invalid, unregistered, or no longer available.
- [`AuthKeyRegenerationRequired`](./errors/authkeyregenerationrequired/) — Authentication key is duplicated or unsynchronized and must be replaced.
- [`BadRequest`](./errors/badrequest/) — Classified client-side Telegram RPC error, normally status code 400.
- [`ClientDisconnected`](./errors/clientdisconnected/) — Raised when invocation cannot continue because the client disconnected.
- [`DatacenterMigration`](./errors/datacentermigration/) — Telegram directs the request to ``dc_id`` for a named migration kind.
- [`FloodWait`](./errors/floodwait/) — Telegram pacing failure that exposes the required wait duration in seconds.
- [`Forbidden`](./errors/forbidden/) — Classified Telegram permission failure with status code 403.
- [`InternalServerError`](./errors/internalservererror/) — Classified retryable server failure, normally a 5xx RPC code.
- [`InvalidCode`](./errors/invalidcode/) — Authentication flow failure for a missing, expired, or invalid phone code.
- [`InvalidDatacenter`](./errors/invaliddatacenter/) — Telegram rejects the current data centre, commonly before a migration hint.
- [`InvokeError`](./errors/invokeerror/) — Base exception for raw invocation failures before Telegram returns a typed RPC error.
- [`NotFound`](./errors/notfound/) — Classified Telegram missing-resource failure with status code 404.
- [`PasswordInvalid`](./errors/passwordinvalid/) — Authentication flow received an invalid two-factor password.
- [`PasswordRequired`](./errors/passwordrequired/) — Authentication flow requires a configured two-factor password.
- [`PendingRpcLimitExceeded`](./errors/pendingrpclimitexceeded/) — Raised when a sender has too many in-flight RPCs and cannot accept more.
- [`RequestTimeout`](./errors/requesttimeout/) — Raised when the client-side request deadline expires.
- [`ResultTypeMismatch`](./errors/resulttypemismatch/) — Raised when an RPC result does not match the requested result contract.
- [`RpcError`](./errors/rpcerror/) — Raw or classified Telegram RPC failure with redaction-safe diagnostics.
- [`RpcTimeout`](./errors/rpctimeout/) — Classified Telegram-side or transport RPC timeout, commonly code -503.
- [`SessionEnvelopeError`](./errors/sessionenvelopeerror/) — Raised when an encrypted session envelope fails validation or authentication.
- [`SessionStorageError`](./errors/sessionstorageerror/) — Raised when session persistence cannot safely continue.
- [`SignUpRequired`](./errors/signuprequired/) — Authentication flow requires creating a Telegram account first.
- [`TransportFlood`](./errors/transportflood/) — Raised for transport-level 429 responses, not ordinary RPC flood waits.
- [`Unauthorized`](./errors/unauthorized/) — Classified Telegram authorization failure with status code 401.
- [`DecodedFileId`](./file_id/decodedfileid/) — Decoded local file-id fields used to recreate a media location or input media.
- [`FILE_ID_PREFIX`](./file_id/file-id-prefix/) — Public attribute `miniproto.file_id.FILE_ID_PREFIX`.
- [`decode_file_id`](./file_id/decode-file-id/) — Decode an ``mpf1_`` file ID without contacting Telegram.
- [`encode_file_id`](./file_id/encode-file-id/) — Encode supported Telegram media or input locations into a local file ID.
- [`input_media_from_file_id`](./file_id/input-media-from-file-id/) — Decode a file ID into Telegram input media.
- [`is_file_id`](./file_id/is-file-id/) — Return whether a value has the miniproto file-id prefix.
- [`media_from_file_id`](./file_id/media-from-file-id/) — Decode a local file ID into a reusable ``Media`` value.
- [`try_encode_file_id`](./file_id/try-encode-file-id/) — Best-effort variant of :func:`encode_file_id`.
- [`CdnIntegrityError`](./media/cdn/cdnintegrityerror/) — Raised when a CDN range lacks valid ``FileHash`` coverage or verification fails.
- [`MediaDownloadResult`](./media/download/mediadownloadresult/) — Completed materialized-download metadata and optional in-memory payload.
- [`MediaIntegrityError`](./media/download/mediaintegrityerror/) — Raised when declared file hashes or download-range invariants are violated.
- [`MediaUploadResult`](./media/upload/mediauploadresult/) — Completed upload metadata and the MTProto input-file reference to reuse.
- [`iter_download`](./media/download/iter-download/) — Stream an exact media range as ordered, bounded byte chunks.
- [`InMemoryMetrics`](./observability/inmemorymetrics/) — Simple in-memory ``MetricsSink`` useful for tests and local diagnostics.
- [`LogFormat`](./observability/logformat/) — Public attribute `miniproto.observability.LogFormat`.
- [`MemoryDelta`](./observability/memorydelta/) — Start, end, and peak resource snapshots for one monitored interval.
- [`MemoryMonitor`](./observability/memorymonitor/) — Collect resource snapshots and optionally manage a temporary tracemalloc session.
- [`MetricEvent`](./observability/metricevent/) — Immutable metric event recorded with a unit, attributes, and wall-clock timestamp.
- [`MetricsSink`](./observability/metricssink/) — Protocol implemented by destinations that accept metric events.
- [`ResourceSnapshot`](./observability/resourcesnapshot/) — Point-in-time process and tracemalloc memory counters.
- [`StructuredFormatter`](./observability/structuredformatter/) — Formatter that redacts structured events and optionally emits compact JSON.
- [`configure_logging`](./observability/configure-logging/) — Install one redacting handler on the miniproto root logger.
- [`current_process_id`](./observability/current-process-id/) — Return the current operating-system process identifier.
- [`emit_event`](./observability/emit-event/) — Emit one structured miniproto event if the level is enabled.
- [`get_logger`](./observability/get-logger/) — Return the root miniproto logger or a named child logger.
- [`get_metrics_sink`](./observability/get-metrics-sink/) — Return the currently configured process-global metrics sink, if any.
- [`process_rss_bytes`](./observability/process-rss-bytes/) — Return this process's reported RSS/working-set byte count when available.
- [`record_metric`](./observability/record-metric/) — Record a metric through the configured sink, suppressing sink failures.
- [`resource_snapshot`](./observability/resource-snapshot/) — Capture current RSS, active tracemalloc counters, and GC object count.
- [`set_metrics_sink`](./observability/set-metrics-sink/) — Set the process-global metrics destination, or disable metric recording.
- [`to_jsonable`](./observability/to-jsonable/) — Recursively convert supported observability values into JSON-compatible shapes.
- [`AuthKey`](./session/models/authkey/) — Validated non-empty MTProto authorization key bound to a positive DC.
- [`DCOption`](./session/models/dcoption/) — One validated Telegram data-centre endpoint and optional transport secret.
- [`PeerCacheEntry`](./session/models/peercacheentry/) — Durable peer lookup metadata with a shallow-copied optional raw-field mapping.
- [`SessionRecord`](./session/models/sessionrecord/) — Complete versioned session state with frozen, shallow collection snapshots.
- [`UpdateState`](./session/models/updatestate/) — Monotonic Telegram update cursors and their latest server timestamp.
- [`UserIdentity`](./session/models/useridentity/) — Durable Telegram user identity with optional private contact metadata.
- [`EncryptedSQLiteSessionStorage`](./session/storage/encryptedsqlitesessionstorage/) — Thread-safe SQLite persistence with per-domain authenticated encryption.
- [`InMemorySessionStorage`](./session/storage/inmemorysessionstorage/) — Thread-safe in-process storage that snapshots all values by serialization.
- [`SessionStorage`](./session/storage/sessionstorage/) — Async session persistence contract with atomic synchronous transforms.
- [`SessionString`](./session/strings/sessionstring/) — A bearer-secret string whose representation is always redacted.
- [`SessionStringFormat`](./session/strings/sessionstringformat/) — Public attribute `miniproto.session.strings.SessionStringFormat`.
- [`export_session_string`](./session/strings/export-session-string/) — Export a typed or decoded session record in a portable bearer format.
- [`import_session_string`](./session/strings/import-session-string/) — Import a native, Telethon v1, or Pyrogram string into a validated record.
- [`Media`](./types/media/) — Normalized Telegram media descriptor used for upload and download helpers.
- [`Message`](./types/message/) — Normalized Telegram message returned by high-level messaging helpers.
- [`NewMessage`](./types/newmessage/) — Update emitted for a newly received message.
- [`Peer`](./types/peer/) — Telegram peer reference suitable for high-level client operations.
- [`Update`](./types/update/) — Base normalized update with a UTC creation timestamp and optional raw payload.
- [`User`](./types/user/) — Normalized Telegram user returned by peer and authorization helpers.
