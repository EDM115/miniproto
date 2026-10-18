---
title: Security and reporting
description: Canonical vulnerability-reporting pointer and operational disclosure boundaries.
slug: /project/security/
generated: false
---

## Canonical policy

The repository's [SECURITY.md](https://github.com/EDM115/miniproto/blob/master/SECURITY.md) is the canonical security policy. It identifies the supported Alpha line, names the sensitive data that must never enter issues/logs/tests/fixtures/commits and directs suspected vulnerabilities to [GitHub private vulnerability reporting](https://github.com/EDM115/miniproto/security/advisories/new), with a maintainer-email fallback when that route is unavailable.

This page intentionally does not duplicate response-time promises, supported-version commitments or another reporting channel. Those details belong in the policy so that security reporting has one authoritative source.

## Report privately and minimize disclosure

Do not open a public issue containing an exploit proof of concept, API hash, phone number, authorization key, session key, bot token, 2FA value, proxy credential, session database or portable session string. Preserve the minimum evidence needed to reproduce the issue and use the private maintainer route described in the canonical policy.

For operational guidance on protecting session material, encrypted storage, redaction limits, native/fallback boundaries and Telegram API responsibility, see the [security model](../concepts/security-model.md) and [Session Security](../session-security.md). Those pages explain safe operation; they do not replace the reporting policy.
