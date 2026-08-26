---
title: "miniproto.mtproto.codec"
description: "MTProto encrypted framing and core service-message body codecs."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.mtproto.codec"
source_path: "src/miniproto/mtproto/codec.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/mtproto/codec.py"
module: "miniproto.mtproto.codec"
---

## `miniproto.mtproto.codec`

MTProto encrypted framing and core service-message body codecs.

## Public objects

- [`DecodedEncryptedMessage`](./decodedencryptedmessage/) — Authenticated encrypted MTProto envelope with decrypted body and padding.
- [`UnencryptedMessage`](./unencryptedmessage/) — Unencrypted MTProto envelope carrying a message ID and raw body.
- [`MsgsAck`](./msgsack/) — MTProto ``msgs_ack`` body acknowledging received message IDs.
- [`MsgsStateReq`](./msgsstatereq/) — MTProto ``msgs_state_req`` body requesting message states.
- [`MsgsStateInfo`](./msgsstateinfo/) — MTProto ``msgs_state_info`` body answering a state request.
- [`MsgResendReq`](./msgresendreq/) — MTProto ``msg_resend_req`` body requesting retransmission of message IDs.
- [`MessageContainerItem`](./messagecontaineritem/) — One message entry inside an MTProto message container.
- [`MessageContainer`](./messagecontainer/) — MTProto ``msg_container`` body containing ordered message entries.
- [`GzipPacked`](./gzippacked/) — MTProto ``gzip_packed`` service body holding compressed message bytes.
- [`Pong`](./pong/) — MTProto ``pong`` response correlating a server message and ping ID.
- [`BadMsgNotification`](./badmsgnotification/) — MTProto notice that a message ID, sequence number or other field was invalid.
- [`BadServerSalt`](./badserversalt/) — MTProto bad-message notice that additionally carries a replacement server salt.
- [`NewSessionCreated`](./newsessioncreated/) — MTProto notification that establishes a new server session and salt.
- [`RpcResult`](./rpcresult/) — MTProto ``rpc_result`` body containing raw or decoded result data.
- [`encode_unencrypted_message`](./encode-unencrypted-message/) — Frame an unencrypted MTProto message with ``auth_key_id = 0``.
- [`decode_unencrypted_message`](./decode-unencrypted-message/) — Validate and decode an unencrypted MTProto envelope.
- [`encode_encrypted_message`](./encode-encrypted-message/) — Encrypt and frame one MTProto message using the configured authorization key.
- [`decode_encrypted_message`](./decode-encrypted-message/) — Authenticate, decrypt and parse one MTProto encrypted envelope.
- [`encode_message_body`](./encode-message-body/) — Encode raw, generated or built-in MTProto service message bodies.
- [`decode_message_body`](./decode-message-body/) — Decode recognized MTProto service bodies, preserving unknown data as a view.
- [`encode_ping`](./encode-ping/) — Encode an MTProto ``ping`` service body.
- [`encode_ping_delay_disconnect`](./encode-ping-delay-disconnect/) — Encode an MTProto ``ping_delay_disconnect`` service body.
- [`gzip_pack`](./gzip-pack/) — Compress an encodable MTProto body into a ``gzip_packed`` service object.
