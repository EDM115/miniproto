# Validate Telegram DH and SRP groups
## 0. Plan metadata
- Status: proposed
- Priority: P0 security
- Estimated size: M
- Risk: high; incorrect number-theory checks can reject authentication or permit attacker-controlled weak groups
- Base commit: cf7db29
- Dependencies: none
- Drift check: reopen src/miniproto/auth/key_exchange.py, src/miniproto/auth/password.py, tests/test_auth.py, and tests/test_crypto_vectors.py. Stop if both auth-key exchange and SRP already use one cached safe-prime/generator/public-value validator with official vectors.
## 1. Objective
Validate Telegram-provided 2048-bit safe primes, generator compatibility, and DH/SRP public values before expensive exponentiation or secret derivation.
## 2. Context and current state
Auth-key exchange converts server values and immediately computes:
> src/miniproto/auth/key_exchange.py:350-355 converts dh_prime and g_a, computes auth_key, and produces g_b.
The current validator is only a range check:
> src/miniproto/auth/key_exchange.py:552-560 accepts generators 2 through 7 and checks dh_prime > 3 and 1 < g_a < dh_prime - 1.
Password SRP is similarly permissive:
> src/miniproto/auth/password.py:22-41 accepts p > 3 and 1 < B < p - 1 before modular exponentiation.
The unit suite normalizes the weakness:
> tests/test_auth.py:133-161 uses the tiny prime 7919 and still expects a 256-byte auth key.
Root cause: protocol parsing validates shape and trivial range but not Telegram’s required safe-prime group or strong public-value bounds.
## 3. Scope
### In scope
- One shared validator for auth DH and password SRP.
- Exact 2048-bit size, primality of p, primality of (p - 1) / 2, allowed generator, generator residue rules, and strong public-value bounds.
- Fast path for Telegram’s published known prime and cached results for repeated SRP/auth use.
- Negative and official positive vectors.
### Out of scope
- Replacing Telegram’s SRP KDF.
- Supporting arbitrary non-Telegram DH group sizes.
- Introducing a heavyweight symbolic-math runtime dependency.
- Changing RSA/PQ factorization.
## 4. Design
### 4.1 Shared API
Create src/miniproto/auth/dh_validation.py with:
- validate_safe_prime_and_generator(p: int, g: int) -> None
- validate_public_value(value: int, p: int, name: str) -> None
- validate_dh_parameters(p: int, g: int, public_value: int, name: str) -> None
Decorate the immutable p/g validation with a bounded cache or functools.cache. Public-value checks remain uncached.
### 4.2 Required group checks
- p has exactly 2048 bits.
- p is prime.
- q = (p - 1) // 2 is prime.
- g is one of 2, 3, 4, 5, 6, or 7.
- Apply Telegram’s documented residue rule for each g: g=2 requires p mod 8 = 7; g=3 requires p mod 3 = 2; g=4 has no extra residue rule; g=5 requires p mod 5 in 1 or 4; g=6 requires p mod 24 in 19 or 23; g=7 requires p mod 7 in 3, 5, or 6.
- Every peer public value is strictly inside Telegram’s strong interval around zero and p, expected to use 2^(2048-64) as the boundary. Reconfirm this constant from the official source before implementation.
### 4.3 Primality strategy
Use an exact constant-time equality fast path for Telegram’s published prime. For any other server prime, use a well-reviewed probable-prime implementation with enough independent rounds for a cryptographic error bound and cryptographically random bases. Keep the implementation small and documented; do not invent an unreviewed custom deterministic claim for all 2048-bit inputs.
If the pure-Python fallback is too slow after caching, add a narrowly scoped Rust helper with the same fixtures and keep the Python implementation as correctness fallback.
### 4.4 Integration order
Auth-key exchange validates p/g/g_a immediately after decrypting and nonce-checking ServerDHInnerData, before generating b or computing auth_key. Validate generated g_b defensively before serialization.
SRP validates p/g/B before generating a. Validate generated A before computing u and S.
### 4.5 Rejected alternatives
- Accepting only the single published prime is simpler but may reject legitimate Telegram rotation; retain a validated fallback.
- Keeping the tiny test prime behind a test-only bypass is rejected because it would preserve an unsafe production branch.
- Checking only p bit length is rejected because composite and non-safe groups remain possible.
## 5. Files to change
| File | Change |
| --- | --- |
| src/miniproto/auth/dh_validation.py | Add shared cached group and public-value validation |
| src/miniproto/auth/key_exchange.py | Validate server p/g/g_a and generated g_b before key derivation |
| src/miniproto/auth/password.py | Validate SRP p/g/B and generated A |
| tests/test_auth.py | Replace tiny-prime success fixtures and add rejection cases |
| tests/test_crypto_vectors.py | Add official Telegram prime and boundary vectors |
| rust/miniproto/src/crypto.rs | Optional only if measured fallback cost requires native acceleration |
| tests/test_native_parity.py | Required only if a native helper is added |
## 6. Execution prerequisites
- Re-read https://core.telegram.org/mtproto/security_guidelines and https://core.telegram.org/api/srp.
- Copy the official prime from an authoritative Telegram source and assert its digest in the fixture to prevent transcription errors.
- Git workflow: read-only Git only; no branch, worktree, stage, commit, stash, revert, or push.
- STOP if official documents change the allowed generators or strong public-value interval.
- STOP before adding a new primality dependency; document footprint, maintenance, and supply-chain impact for user approval.
## 7. Implementation steps
1. Add official positive vectors and failing tiny/composite/non-safe/bad-residue/boundary vectors. Remove 7919 as a successful production validation fixture; retain it only in isolated arithmetic tests that do not call the production validator.  
   Verification: uv run pytest tests/test_auth.py tests/test_crypto_vectors.py
2. Implement cached p/g validation and public-value validation with testable primality randomness. Add cache-hit instrumentation only in tests, not public telemetry.  
   Verification: uv run pytest tests/test_crypto_vectors.py -k "prime or generator or public"
3. Wire auth-key exchange validation before exponentiation and assert no random private exponent is requested after invalid input.  
   Verification: uv run pytest tests/test_auth.py -k "key or dh"
4. Wire SRP validation before random A generation and KDF exponentiation. Add invalid B and invalid generated-A boundary tests.  
   Verification: uv run pytest tests/test_auth.py -k "password or srp"
5. Benchmark first validation and cached validation. The cached path should be negligible relative to the SRP KDF. If it is not, profile before adding Rust.  
   Verification: uv run python tools/bench/benchmark_native_fallback_crypto.py
6. If and only if profiling justifies native work, implement a parity-tested Rust helper without removing the fallback.  
   Verification: cargo test --all-features and uv run pytest tests/test_native_parity.py
7. Run full verification.  
   Verification: all commands in section 8 exit zero.
## 8. Testing strategy
### Focused
- uv run pytest tests/test_auth.py tests/test_crypto_vectors.py
- uv run python tools/bench/benchmark_native_fallback_crypto.py
### Full
- uv run ruff format --check .
- uv run ruff check .
- uv run ty check
- uv run python -m tools.schema.generate --check
- uv run pytest
- cargo fmt --check
- cargo clippy --all-targets --all-features -- -D warnings
- cargo test --all-features
### Required edge cases
- Published Telegram safe prime and every allowed compatible generator.
- 2047-bit and 2049-bit primes.
- Composite p and prime p whose q is composite.
- Every invalid generator residue.
- Public values at 1, lower boundary, p minus lower boundary, and p minus 1.
- Repeated validation hits cache but public values are still checked each call.
## 9. Done criteria
- Tiny or weak groups cannot reach pow for auth or SRP.
- Official Telegram vectors pass in both first and cached calls.
- Strong public-value boundaries are enforced for g_a, g_b, A, and B.
- No new large dependency is introduced without explicit approval.
- Focused, benchmark smoke, and full verification pass.
## 10. Rollback and recovery
If a legitimate Telegram group is rejected, capture p digest, g, bit length, residue results, and boundary status without any password or secret exponent. Add a regression vector and fix only the incorrect predicate; never restore the trivial p > 3 check.
## 11. Risks and mitigations
| Risk | Mitigation |
| --- | --- |
| Primality work blocks login | Official-prime fast path and cached fallback |
| A copied prime is wrong | Authoritative source plus digest assertion |
| Random probable-prime test is flaky | Fixed official vectors and deterministic injectable bases in tests |
| SRP secrets leak in diagnostics | Log only reason, p digest, bit length, and generator |
## 12. Maintenance and references
- Owner: unassigned
- Review trigger: changes to auth key exchange, SRP algorithms, supported schema password algorithm, crypto native helpers, or official Telegram security rules.
- Official references: https://core.telegram.org/mtproto/security_guidelines and https://core.telegram.org/api/srp
- Repository evidence: src/miniproto/auth/key_exchange.py, src/miniproto/auth/password.py, tests/test_auth.py, tests/test_crypto_vectors.py.
