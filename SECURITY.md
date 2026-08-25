# Security Policy

## Supported versions

`miniproto` is in Alpha development. Security fixes target the active `0.1.x` line and the current development branch until a newer supported line is announced.

| Version                                  | Supported |
| ---------------------------------------- | --------- |
| `0.1.x` Alpha                            | Yes       |
| `0.0.x` reservation/development packages | No        |

Alpha support does not promise API stability. A security fix can require a breaking change when preserving the old behavior would retain an unsafe default or protocol boundary.

## Report a vulnerability privately

Use [GitHub private vulnerability reporting](https://github.com/EDM115/miniproto/security/advisories/new) for suspected vulnerabilities. If that route is unavailable, email [miniproto@edm115.dev](mailto:miniproto@edm115.dev) with a minimal, non-secret description and arrange a protected channel before sending exploit material or credentials.  
Do not open a public issue, discussion, pull request, or benchmark artifact containing exploit instructions, proof-of-concept payloads, account data, or authorization material. Include the affected version/commit, platform, impact, prerequisites, and the smallest safe reproduction description. Do not include a real Telegram credential merely to prove reachability.  
No fixed response or remediation deadline is promised. The maintainer will acknowledge and coordinate through the private route as availability permits; publication timing must be agreed before public disclosure.

## Credentials and session material

Treat all of the following as secrets or sensitive account data :

- Telegram `api_hash` values, bot tokens, phone numbers, login codes, two-step-verification passwords, authorization keys, server salts, and proxy credentials
- `MINIPROTO_SESSION_KEY`, encrypted SQLite session files, their backups, and any key material passed directly to a storage constructor
- Native miniproto, Telethon, and Pyrogram session strings. A passphrase-protected native string is encrypted at rest, but the imported value still grants account access
- Live-test environment files, CI secrets, benchmark sessions, logs, captures, crash dumps, and artifacts that may retain any of the above

Never place these values in source control, public issues, command-line arguments, shell transcripts, ordinary fixtures, screenshots, or unredacted logs. Use a deployment secret manager, restrict the session file to the service identity, provision a distinct storage path and key per account/deployment, and keep a portable-session passphrase separate from the encoded value where practical.  
The default durable client storage is encrypted SQLite and refuses to initialize without adequate constructor key material or `MINIPROTO_SESSION_KEY`. `InMemorySessionStorage()` avoids durable persistence but does not erase credentials from process memory. Redacted `repr` output and logging helpers reduce accidental disclosure; they do not protect direct attribute access, serialization, memory dumps, `dataclasses.asdict()`, a deliberately printed value, or arbitrary third-party logging.  
After suspected disclosure, revoke or rotate the Telegram authorization and replace affected bot/proxy/password credentials. Changing only the local storage key does not invalidate an authorization key or session string that an attacker already copied.

## Session import and migration risks

Telethon v1 and Pyrogram compatibility strings preserve only their respective wire fields and are not encrypted by miniproto. Native bearer mode adds corruption detection but no confidentiality or attacker-resistant authenticity. Use the protected native format for portable backups, verify the source account/configuration independently, keep clients disconnected while importing, and rely on the default refusal to overwrite nonempty storage unless replacement is deliberate.  
`allow_mismatch=True` and `replace=True` are explicit migration overrides, not safety checks. A successful import does not prove that the session belongs to the intended account, uses the intended Telegram environment, or has not already been copied.

## Live tests and benchmarks

Credentialed integration tests, session provisioning, live media benchmarks, compatibility matrices, and release-live checks can create Telegram-visible authorization, messages, uploads, downloads, flood waits, and session files. Run them only against accounts, peers, files, and datacenters you are authorized to use, through the documented opt-in environment gates.  
Do not enable live gates on untrusted pull requests or expose secrets to forked workflows. Review uploaded logs and artifacts before sharing them. Deterministic fake-server or offline benchmark success is not evidence that a live account, Telegram limit, CDN edge, proxy, or production deployment is secure.

## Dependencies, native code, and artifacts

Install release artifacts from the project's declared distribution channels and verify provenance/hashes when provided. A `miniproto` wheel contains native Rust code; an editable checkout, locally rebuilt extension, third-party mirror, or modified generated schema is a different trust boundary. Keep Python, Rust, Maturin, cryptography, event-loop backends, and operating-system dependencies current within the supported compatibility line.  
Official release candidates are constructed only by the manual **Build release artifacts** workflow, which attests each wheel, the Python sdist, the Cargo source package, and their checksum/provenance sidecars. The separate protected publisher verifies one exact build run and its attestations before exchanging GitHub OIDC identity for short-lived PyPI and crates.io credentials; the GitHub release stays a draft until both registries succeed. Never grant publication credentials to a build job, combine artifacts from different runs, or treat an unattested local rebuild as the same candidate.  
Public wrappers select available native capabilities and use supported fallbacks where defined. A missing native symbol is not by itself a vulnerability, and forcing an unverified native or fallback path can remove validation/performance assumptions. Report output or validation divergence privately with non-secret inputs.

## Scope and responsible use

Reports about miniproto's own protocol, storage, parser, native, packaging, or documentation behavior are in scope. Telegram service availability, account bans, platform policy, and vulnerabilities exclusively in an upstream dependency should normally be reported to the responsible upstream project, although a miniproto-specific unsafe integration remains relevant here.  
You are responsible for Telegram's Terms of Service and API rules, account consent, and lawful handling of user data. This policy does not authorize testing against accounts, peers, infrastructure, or credentials you do not control.
