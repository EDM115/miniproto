---
title: "miniproto.auth"
description: "Telegram authorization, data-center selection, key exchange, and SRP helpers."
generated: true
editUrl: false
language: "python"
kind: "module"
qualified_name: "miniproto.auth"
source_path: "src/miniproto/auth/__init__.py"
source_url: "https://github.com/EDM115/miniproto/blob/master/src/miniproto/auth/__init__.py"
module: "miniproto.auth"
---

## `miniproto.auth`

Telegram authorization, data-center selection, key exchange, and SRP helpers.

## Public objects

- [`TEST_DC_OPTIONS`](./dc/test-dc-options/) — Public attribute `miniproto.auth.dc.TEST_DC_OPTIONS`.
- [`dc_options_from_env`](./dc/dc-options-from-env/) — Read local test-DC overrides from environment-style mappings.
- [`dc_options_from_raw`](./dc/dc-options-from-raw/) — Convert raw Telegram DC options to immutable session-model options.
- [`select_dc_option`](./dc/select-dc-option/) — Choose the best endpoint for a data center.
- [`AuthKeyExchange`](./key_exchange/authkeyexchange/) — Perform Telegram's RSA- and DH-protected MTProto authorization handshake.
- [`AuthKeyExchangeResult`](./key_exchange/authkeyexchangeresult/) — Authenticated MTProto key material and metadata produced by an exchange.
- [`AuthKeyTransport`](./key_exchange/authkeytransport/) — Transport capability required for Telegram's unencrypted handshake.
- [`ClientDHInnerData`](./key_exchange/clientdhinnerdata/) — Client DH public value encrypted into ``set_client_DH_params``.
- [`DHGenFail`](./key_exchange/dhgenfail/) — ``dh_gen_fail`` response containing the third new-nonce hash.
- [`DHGenOk`](./key_exchange/dhgenok/) — ``dh_gen_ok`` response containing the first new-nonce hash.
- [`DHGenRetry`](./key_exchange/dhgenretry/) — ``dh_gen_retry`` response containing the second new-nonce hash.
- [`PQInnerDataDC`](./key_exchange/pqinnerdatadc/) — Plaintext ``p_q_inner_data_dc`` encrypted into ``req_DH_params``.
- [`RSAKey`](./key_exchange/rsakey/) — Telegram RSA public key used to encrypt the ``req_DH_params`` payload.
- [`ReqDHParams`](./key_exchange/reqdhparams/) — Serialized ``req_DH_params`` request containing RSA-encrypted inner data.
- [`ReqPQMulti`](./key_exchange/reqpqmulti/) — Serialized ``req_pq_multi`` request carrying a client nonce.
- [`ResPQ`](./key_exchange/respq/) — Decoded ``resPQ`` response received at the start of key exchange.
- [`ServerDHInnerData`](./key_exchange/serverdhinnerdata/) — Validated plaintext DH group and server public value from Telegram.
- [`ServerDHParamsFail`](./key_exchange/serverdhparamsfail/) — ``server_DH_params_fail`` response proving Telegram rejected the request.
- [`ServerDHParamsOk`](./key_exchange/serverdhparamsok/) — Successful ``server_DH_params_ok`` wrapper for encrypted DH parameters.
- [`SetClientDHParams`](./key_exchange/setclientdhparams/) — Serialized ``set_client_DH_params`` request carrying AES-IGE ciphertext.
- [`compute_auth_key`](./key_exchange/compute-auth-key/) — Compute the 256-byte MTProto key from validated DH peer and private values.
- [`compute_new_nonce_hash`](./key_exchange/compute-new-nonce-hash/) — Compute Telegram's keyed new-nonce confirmation hash number 1, 2, or 3.
- [`decrypt_server_dh_answer`](./key_exchange/decrypt-server-dh-answer/) — Decrypt, integrity-check, and decode Telegram's encrypted DH inner payload.
- [`derive_tmp_aes_key_iv`](./key_exchange/derive-tmp-aes-key-iv/) — Derive the temporary AES-256-IGE key and IV defined by MTProto key exchange.
- [`encode_client_dh_inner_data`](./key_exchange/encode-client-dh-inner-data/) — Serialize ``client_DH_inner_data`` before temporary AES-IGE encryption.
- [`encode_pq_inner_data_dc`](./key_exchange/encode-pq-inner-data-dc/) — Serialize ``p_q_inner_data_dc`` before applying Telegram RSA padding.
- [`factorize_pq`](./key_exchange/factorize-pq/) — Factor Telegram's small composite ``pq`` and return its factors in ascending order.
- [`public_rsa_fingerprint`](./key_exchange/public-rsa-fingerprint/) — Calculate Telegram's signed little-endian 64-bit RSA fingerprint.
- [`rsa_pad`](./key_exchange/rsa-pad/) — Apply Telegram's randomized RSA_PAD encryption to a small inner payload.
- [`select_rsa_key`](./key_exchange/select-rsa-key/) — Select the first server-offered fingerprint present in trusted ``keys``.
- [`server_salt`](./key_exchange/server-salt/) — Derive the MTProto server salt by XORing the first nonce bytes.
- [`compute_check_password`](./password/compute-check-password/) — Build the request payload required to verify an account password.
- [`AuthService`](./service/authservice/) — Run sign-in and data-center authorization flows for one client session.
