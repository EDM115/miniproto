---
title: "miniproto.mtproto"
description: "Public MTProto message framing, service-body, and state APIs."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.mtproto"
source_path: "src/miniproto/mtproto/__init__.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/__init__.py"
module: "miniproto.mtproto"
---

## `miniproto.mtproto`

Public MTProto message framing, service-body, and state APIs.

## Public objects

- [`BadMsgNotification`](./codec/badmsgnotification/) — MTProto notice that a message ID, sequence number, or other field was invalid.
- [`BadServerSalt`](./codec/badserversalt/) — MTProto bad-message notice that additionally carries a replacement server salt.
- [`DecodedEncryptedMessage`](./codec/decodedencryptedmessage/) — Authenticated encrypted MTProto envelope with decrypted body and padding.
- [`GzipPacked`](./codec/gzippacked/) — MTProto ``gzip_packed`` service body holding compressed message bytes.
- [`MessageContainer`](./codec/messagecontainer/) — MTProto ``msg_container`` body containing ordered message entries.
- [`MessageContainerItem`](./codec/messagecontaineritem/) — One message entry inside an MTProto message container.
- [`MsgResendReq`](./codec/msgresendreq/) — MTProto ``msg_resend_req`` body requesting retransmission of message IDs.
- [`MsgsAck`](./codec/msgsack/) — MTProto ``msgs_ack`` body acknowledging received message IDs.
- [`MsgsStateInfo`](./codec/msgsstateinfo/) — MTProto ``msgs_state_info`` body answering a state request.
- [`MsgsStateReq`](./codec/msgsstatereq/) — MTProto ``msgs_state_req`` body requesting message states.
- [`NewSessionCreated`](./codec/newsessioncreated/) — MTProto notification that establishes a new server session and salt.
- [`Pong`](./codec/pong/) — MTProto ``pong`` response correlating a server message and ping ID.
- [`RpcErrorBody`](./codec/rpcerrorbody/) — Decoded MTProto ``rpc_error`` result body.
- [`RpcResult`](./codec/rpcresult/) — MTProto ``rpc_result`` body containing raw or decoded result data.
- [`decode_encrypted_message`](./codec/decode-encrypted-message/) — Authenticate, decrypt, and parse one MTProto encrypted envelope.
- [`decode_message_body`](./codec/decode-message-body/) — Decode recognized MTProto service bodies, preserving unknown data as a view.
- [`decode_unencrypted_message`](./codec/decode-unencrypted-message/) — Validate and decode an unencrypted MTProto envelope.
- [`encode_encrypted_message`](./codec/encode-encrypted-message/) — Encrypt and frame one MTProto message using the configured authorization key.
- [`encode_message_body`](./codec/encode-message-body/) — Encode raw, generated, or built-in MTProto service message bodies.
- [`encode_unencrypted_message`](./codec/encode-unencrypted-message/) — Frame an unencrypted MTProto message with ``auth_key_id = 0``.
- [`gzip_pack`](./codec/gzip-pack/) — Compress an encodable MTProto body into a ``gzip_packed`` service object.
- [`MTProtoState`](./state/mtprotostate/) — Track one authorization key's MTProto session, timing, and acknowledgement state.
