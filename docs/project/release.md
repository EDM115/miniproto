---
title: Release
description: Release evidence, clean-artifact checks, and the boundary between validation and user-controlled publishing.
slug: /project/release/
generated: false
---

## Release is evidence, not a command that publishes

`miniproto-release-check` is the canonical non-mutating aggregate release diagnostic. It streams its checks, preserves failures, and writes evidence such as environment details, benchmark reports, distribution hashes, and clean-import results under a caller-owned artifact directory. Its modes do not format, fix, publish, tag, or accept secret-bearing command-line arguments.

Use the exact invocation and diagnostic stages in the [development guide](../development.md). Start with narrow checks while changing a focused surface, then run the appropriate aggregate gate before claiming release readiness. A passing local check is not authorization to publish a package, create a Git tag, or operate release credentials.

## What a release must establish

A release candidate must be built as a wheel and source distribution, inspected for the intended Python/generated/native sources and no checkout linkage or secrets, then installed non-editably in a clean environment. The acceptance evidence must show imports of the public package, raw API, representative Layer 228 symbols, and native capability under the selected interpreter.

The wheel matrix includes normal and free-threaded supported CPython environments, with dependency-resolving installation rather than an editable checkout shortcut. Native import behavior, declared dependencies, platform tags, and generated schema provenance must all match the artifact, not merely the source tree.

## Live gates stay separate

The credentialed release extension is deliberately guarded and is not normal pull-request CI. When the required secrets, test account, runner, or Telegram conditions are unavailable, record that live acceptance was not run or is externally blocked. Do not reinterpret missing live evidence as a passing gate, and do not turn a deterministic test into a claim about real-account behavior.

## Publishing and history

Publishing credentials, package promotion, tags, and the public release decision remain user-controlled operations. Read the repository [CHANGELOG.md](https://github.com/EDM115/miniproto/blob/master/CHANGELOG.md) for the complete Alpha capability summary and breaking notes; this page intentionally does not duplicate or pre-write changelog entries.
