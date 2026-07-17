# Lazy-load the generated raw API

## 0. Plan metadata

- Status: completed
- Priority: P1 startup performance and memory
- Estimated size: L
- Risk: high; generated-module layout, constructor decoding, typing, pickling, and public imports must stay compatible
- Base commit: cf7db29
- Dependencies: none
- Drift check: remeasure imports and reopen src/miniproto/**init**.py, src/miniproto/client.py, src/miniproto/raw/**init**.py, src/miniproto/raw/base.py, src/miniproto/raw/functions.py, src/miniproto/raw/types.py, src/miniproto/tl/codec.py, tools/schema/generate.py, tests/test_schema_generation.py, tests/test_tl_codec.py, and tools/bench/benchmark_runtime_paths.py. Stop if importing Client no longer executes every generated class or a different lazy registry already preserves public API.

## 1. Objective

Make import miniproto and from miniproto import Client avoid constructing the entire generated Telegram API, while preserving public raw attribute imports, class identity, deterministic generation, type information, and warmed codec throughput.

## 2. Context and current state

Top-level import reaches Client:

> src/miniproto/**init**.py:3-6 imports event_loop, auth services, Client, and config eagerly.

Client reaches both generated modules:

> src/miniproto/client.py:85 imports functions and types.

The raw namespace eagerly imports them too:

> src/miniproto/raw/**init**.py:3-4 imports errors, functions, and types.

The generator emits monolithic files:

> tools/schema/generate.py:23-28 lists src/miniproto/raw/types.py and functions.py in the deterministic manifest.
> tools/schema/generate.py:242 onward renders all entries for one module.

Constructor decode needs a global class map:

> src/miniproto/tl/codec.py:184-195 resolves a constructor id from _constructor_maps.

The audit’s warmed-filesystem subprocess sample at cf7db29 observed about 2.17 seconds and roughly 63 MiB of traced retained memory for import miniproto. A 2026-07-16 rebaseline at 664a56c after plan 013 measured about 4.09 seconds without tracemalloc and 65.6 MiB retained/65.7 MiB peak with tracemalloc; five raw modules were loaded (`raw`, `base`, `errors`, `functions`, and `types`). These are orientation values, not portable absolutes; the implementation benchmark must capture five fresh subprocess runs on the same machine before and after.
Root cause: one lightweight public import executes tens of thousands of generated class statements and builds global collections before any Telegram request is encoded or decoded.

## 3. Scope

### In scope

- Generate deterministic type/function shard modules and compact lazy facades.
- Resolve public class attributes and constructor ids on first use, then cache them.
- Preserve miniproto.raw.functions.Name and miniproto.raw.types.Name imports.
- Preserve class identity, repr/module path, pickling, **all**, dir, and static typing.
- Add import time/memory and warmed codec performance gates.
- Regenerate outputs only through tools/schema/generate.py.

### Out of scope

- Dynamic schema download or network access at import.
- Changing Telegram layer or schema inputs.
- Lazy-loading handwritten core modules unrelated to raw classes except the minimal top-level changes needed to avoid forcing raw facades.
- Accepting a steady-state codec regression for a startup win.

## 4. Design

### 4.1 Generated layout

Keep public facade modules at src/miniproto/raw/types.py and functions.py. Generate implementation shards under private directories such as src/miniproto/raw/_types_shards/ and _function_shards/.
Assign each entry to a stable bucket derived from constructor id, not list position, so schema additions do not rewrite unrelated shards. Start with 64 type buckets and 32 function buckets, then adjust only if measurements show pathologically large or tiny modules.

### 4.2 Lazy facade

Generate one compact private `_registry.py` shared by both facades. It maps public names and constructor ids to facade kind, stable shard module, and attribute name without importing a shard.
Each facade contains or references compact immutable manifests:

- public name to shard module;
- constructor id to public name and shard module;
- namespace metadata needed by **dir** and **all**.
  Module **getattr** imports the owning shard, obtains the class, normalizes its **module** to the public facade, stores it in facade globals, and returns it. Repeated lookup returns the identical class object. **dir** merges loaded globals with manifest names.
  Import locking is delegated to importlib, but facade caching must tolerate two tasks/threads asking for one class concurrently.

### 4.3 Constructor registry

Replace eager maps of constructor id to every class with a cached lazy Mapping view whose `get`/index operations look up the compact manifest and import only the owner shard. Preserve the cached singleton identity currently returned by `_constructor_maps()`. `decode_object` pays one lazy import the first time a constructor family is encountered and direct lookup thereafter; it must not iterate or materialize the mapping.
Inventory ALL_TYPES, ALL_FUNCTIONS, and CONSTRUCTORS consumers. Preserve documented behavior with a lazy Sequence/Mapping view or make an explicit pre-alpha internal change; do not accidentally materialize every class from codec initialization.

### 4.4 Cross-shard references

Generated serializers/deserializers must refer to TL field types by schema string or lazy resolver, never import all related shards. If straight-line code needs a class, generate a local resolver call. Verify recursive types and vectors.

### 4.5 Static typing and pickling

Generate types.pyi and functions.pyi with the same public class signatures, or an equivalent TYPE_CHECKING-only surface, so editors and ty see all attributes without runtime imports. Include stubs in the manifest and wheel.
Normalize public **module** and ensure unpickling asks the facade for the class through **getattr**. Add pickle round trips for representative namespaced and root classes.

### 4.6 Performance targets

Measure at least five fresh subprocesses with warmed filesystem before and after:

- Median import miniproto wall time improves at least 60 percent from the same-machine cf7db29 baseline.
- Tracemalloc retained memory after import improves at least 50 percent.
- Importing Client and ClientConfig loads no private raw shard.
- After one warm-up decode/encode, existing TL benchmark medians regress no more than 5 percent.
  If a target misses, profile and record why before merging; do not hide import work in the first Client constructor call.

### 4.7 Rejected alternatives

- Only making raw/**init**.py lazy is rejected because Client still imports monolithic modules.
- One module per class is rejected due filesystem and import overhead.
- Editing generated files by hand is rejected because generation checks overwrite them.
- Dropping type visibility is rejected because typed raw API is a project requirement.

## 5. Files to change

| File                                   | Change                                                                                    |
| -------------------------------------- | ----------------------------------------------------------------------------------------- |
| tools/schema/generate.py               | Generate facades, stable shards, stubs, manifests, and stale-shard cleanup                |
| tools/schema/update.py                 | Keep its generated-output manifest synchronized with the generator                        |
| src/miniproto/raw/types.py             | Regenerated lazy facade                                                                   |
| src/miniproto/raw/functions.py         | Regenerated lazy facade                                                                   |
| src/miniproto/raw/_registry.py         | Compact generated name/id-to-shard registry and lazy collection views                     |
| src/miniproto/raw/_types_shards/       | New generated type implementation shards                                                  |
| src/miniproto/raw/_function_shards/    | New generated request implementation shards                                               |
| src/miniproto/raw/types.pyi            | New generated public typing surface                                                       |
| src/miniproto/raw/functions.pyi        | New generated public typing surface                                                       |
| src/miniproto/raw/**init**.py          | Avoid eager facade loading where possible                                                 |
| src/miniproto/tl/codec.py              | Resolve constructor ids lazily and cache                                                  |
| src/miniproto/client.py                | Avoid operations that materialize raw registries at module import                         |
| tests/test_schema_generation.py        | Determinism, stale cleanup, manifest, and stub tests                                      |
| tests/test_tl_codec.py                 | Lazy resolution, class identity, recursive decode, and pickle tests                       |
| tests/test_invoke.py                   | Representative RPC result decoding through the lazy registry                              |
| tools/bench/benchmark_imports.py       | Add isolated fresh-process import, memory, first-attribute, and first-decode measurements |
| tools/bench/benchmark_runtime_paths.py | Preserve warmed codec throughput measurements                                             |
| docs/development.md                    | Document generated layout and benchmark command                                           |

## 6. Execution prerequisites

- Capture a fresh current-HEAD subprocess baseline for import time, tracemalloc retained/peak memory, sys.modules raw-module list, wheel size, and warmed TL benchmark results. Do not reuse the stale placeholder wheel currently under dist.
- Search all ALL_TYPES, ALL_FUNCTIONS, CONSTRUCTORS, constructor_id_map, **module**, and pickling consumers.
- Git workflow: read-only Git only; no branch, worktree, stage, commit, stash, revert, or push.
- STOP if public compatibility requires a different shard/facade contract; update this plan before generator edits.
- STOP if type stubs cannot represent the runtime API without changing user imports.

## 7. Implementation steps

1. Add a subprocess benchmark/test harness that records wall time, tracemalloc, and loaded raw modules for import miniproto, import Client, first raw attribute, and first decode. Record baseline outside generated output.  
   Verification: uv run python tools/bench/benchmark_imports.py, or the final equivalent command.
2. Add generator golden tests for stable bucket assignment, deterministic output, removed-shard cleanup, and check-mode drift.  
   Verification: uv run pytest tests/test_schema_generation.py
3. Generate the private registry and shards and keep current eager facades temporarily so the full schema suite proves shard code independently. Extend generator ownership so `--check` reports unexpected generated `.py` files in shard directories and normal generation removes only generator-owned stale shards.  
   Verification: uv run python -m tools.schema.generate and uv run pytest tests/test_schema_generation.py tests/test_tl_codec.py
4. Generate lazy facades, manifests, **getattr**, **dir**, and cache behavior. Add root/namespaced imports, repeated identity, star-import, and concurrent lookup tests.  
   Verification: uv run pytest tests/test_schema_generation.py tests/test_tl_codec.py
5. Replace eager constructor maps with lazy id resolution. Test unknown ids, recursive objects, vectors, RPC results, and full representative schema round trips.  
   Verification: uv run pytest tests/test_tl_codec.py tests/test_invoke.py
6. Generate and package stubs. Run ty against representative imports, synchronize the duplicate manifest in tools/schema/update.py, and build a fresh wheel to inspect facades, registry, shards, and `.pyi` files.  
   Verification: uv run ty check and uv run maturin build.
7. Add pickle/repr/module-path tests and ensure no private shard path leaks from public classes.  
   Verification: uv run pytest tests/test_tl_codec.py -k "pickle or module or lazy"
8. Measure cold import, first-use cost, warmed throughput, memory, and wheel size. Meet section 4.6 targets or STOP for profiling.  
   Verification: import benchmark plus uv run python tools/bench/benchmark_runtime_paths.py.
9. Run generated-file check and full verification.  
   Verification: all section 8 commands pass.

## 8. Testing strategy

### Focused

- uv run pytest tests/test_schema_generation.py tests/test_tl_codec.py tests/test_invoke.py
- uv run python -m tools.schema.generate --check
- uv run python tools/bench/benchmark_imports.py
- uv run python tools/bench/benchmark_runtime_paths.py
- uv run maturin build

### Full

- uv run ruff format --check .
- uv run ruff check .
- uv run ty check
- uv run python -m tools.schema.generate --check
- uv run pytest
- cargo fmt --check
- cargo clippy --all-targets --all-features -- -D warnings
- cargo test --all-features
- uv run maturin build

### Required edge cases

- Root and namespaced type/function names.
- Two simultaneous first lookups return one class identity.
- Recursive fields and constructor ids from different shards.
- Unknown name and unknown constructor errors remain clear.
- Pickle round trip in a fresh subprocess.
- Removed schema entry deletes stale shard output in generation check.

## 9. Done criteria

- Importing miniproto or Client loads no raw implementation shard.
- Public raw import syntax and class identity remain compatible.
- Constructor decode imports and caches only the needed shard.
- Stubs preserve type checking and wheel packaging.
- Relative startup/memory targets and warmed-throughput guard pass.
- Generation is deterministic and --check is clean.

## 10. Rollback and recovery

If lazy generation breaks compatibility, keep the benchmark and failing compatibility fixture, restore the monolithic generator through a user-owned Git action, and redesign the facade. Never hand-edit generated outputs or disable generation checks.

## 11. Risks and mitigations

| Risk                            | Mitigation                                              |
| ------------------------------- | ------------------------------------------------------- |
| First-use latency spikes        | Stable moderate shard count and explicit cold benchmark |
| Class identity or pickle breaks | Facade cache, public **module**, fresh-process tests    |
| Type completion disappears      | Generated pyi surfaces                                  |
| Shards become stale             | Generator-owned manifest and stale cleanup              |
| Warm decode slows               | Cached id resolver and 5 percent regression gate        |

## 12. Maintenance and references

- Owner: unassigned
- Review trigger: schema layer update, generator layout, constructor registry, raw public exports, packaging, or type-checker changes.
- Repository evidence: src/miniproto/**init**.py, src/miniproto/client.py, src/miniproto/raw/**init**.py, src/miniproto/raw/base.py, src/miniproto/raw/functions.py, src/miniproto/raw/types.py, src/miniproto/tl/codec.py, tools/schema/generate.py, tests/test_schema_generation.py, tests/test_tl_codec.py, tools/bench/benchmark_runtime_paths.py.

## 13. 2026-07-16 fresh verification handoff

- Final correction removed the broad `Any` from the schema-generation test boundary. Focused and repository-wide static gates plus the exact generator test are green; the independent re-review APPROVED the correction.
- Shared repository gate passed: 627 Python tests passed with 4 skipped; 16 Rust tests passed; Ruff, ty, schema generation, Rust format, Clippy, maturin develop, and dev/release wheel builds passed.
- Runtime/stub assertion correction: tests/test_schema_generation.py now verifies `help = lazy_namespace("functions", "help")` in the generated runtime facade; `class help:` and `GetConfig = HelpGetConfig` remain verified only in functions.pyi. The stale runtime `GetConfig = HelpGetConfig` assertion was removed.
- Focused tests: `uv run pytest tests/test_schema_generation.py tests/test_tl_codec.py tests/test_invoke.py --basetemp=.pytest-tmp/plan010-fresh/run-20260716-d` passed, 82 passed in 74.32 seconds.
- Generator drift: `uv run python -m tools.schema.generate --check` passed with `schema generated files are fresh`.
- Fresh-process import benchmark: `uv run python tools/bench/benchmark_imports.py --runs 5` passed. `import miniproto` median was 0.5520567000057781 seconds; `import Client` median was 0.4964465000011842 seconds. Tracemalloc `import miniproto` median was 0.8912517999997362 seconds, 16,456,000 retained bytes, and 16,501,006 peak bytes. Plain miniproto and Client imports loaded the facades and registry but no private shard. First decode loaded only `_types_shards.bucket_09`.
- Relative startup/memory evidence: against the plan's same-machine 4.09-second and approximately 65.6-MiB rebaseline, the fresh 0.5521-second import is approximately 86.5 percent faster and 16,456,000 retained bytes is approximately 76.1 percent lower. Earlier interleaved same-process evidence measured warmed decode delta at +0.666 percent, within the 5 percent gate.
- Lazy-codec profile: `uv run python tools/bench/profile_lazy_raw_codec.py` passed; `facade_is_shard` and `serialize_code_identity` were both true. Medians included `decode_full_100` 71.9498 ms, `constructor_codec_hot_cache_100k` 18.5158 ms, and `facade_attribute_100k` 16.7125 ms.
- Runtime paths: `uv run python tools/bench/benchmark_runtime_paths.py` passed. Median results were update dispatch 74.064 ms, media upload 40.779 ms, media download 369.524 ms, TL encode 258.077 ms, TL decode 12.172 ms, and pending requests 11.222 ms.
- Build: `uv run maturin build` passed and produced `target/wheels/miniproto-0.0.1-cp314-cp314-win_amd64.whl`. Rust emitted one non-fatal linker-message warning.
- Wheel inspection passed: the wheel contains `miniproto/raw/types.py`, `functions.py`, `_registry.py`, `types.pyi`, `functions.pyi`, all 64 type shard files, and all 32 function shard files.
- Final static correction removed the broad `Any` boundary; focused and repository-wide Ruff/ty plus the exact generator test passed, independent re-review APPROVED, and the 2026-07-17 shared repository gate passed.
