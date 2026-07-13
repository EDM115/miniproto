# Lazy-load the generated raw API
## 0. Plan metadata
- Status: proposed
- Priority: P1 startup performance and memory
- Estimated size: L
- Risk: high; generated-module layout, constructor decoding, typing, pickling, and public imports must stay compatible
- Base commit: cf7db29
- Dependencies: none
- Drift check: remeasure imports and reopen src/miniproto/__init__.py, src/miniproto/client.py, src/miniproto/raw/__init__.py, src/miniproto/raw/base.py, src/miniproto/raw/functions.py, src/miniproto/raw/types.py, src/miniproto/tl/codec.py, tools/schema/generate.py, tests/test_schema_generation.py, tests/test_tl_codec.py, and tools/bench/benchmark_runtime_paths.py. Stop if importing Client no longer executes every generated class or a different lazy registry already preserves public API.
## 1. Objective
Make import miniproto and from miniproto import Client avoid constructing the entire generated Telegram API, while preserving public raw attribute imports, class identity, deterministic generation, type information, and warmed codec throughput.
## 2. Context and current state
Top-level import reaches Client:
> src/miniproto/__init__.py:3-6 imports event_loop, auth services, Client, and config eagerly.
Client reaches both generated modules:
> src/miniproto/client.py:85 imports functions and types.
The raw namespace eagerly imports them too:
> src/miniproto/raw/__init__.py:3-4 imports errors, functions, and types.
The generator emits monolithic files:
> tools/schema/generate.py:23-28 lists src/miniproto/raw/types.py and functions.py in the deterministic manifest.
> tools/schema/generate.py:242 onward renders all entries for one module.
Constructor decode needs a global class map:
> src/miniproto/tl/codec.py:184-195 resolves a constructor id from _constructor_maps.
The audit’s warmed-filesystem subprocess sample at cf7db29 observed about 2.17 seconds and roughly 63 MiB of traced retained memory for import miniproto. These are orientation values, not portable absolutes; remeasure before implementation.
Root cause: one lightweight public import executes tens of thousands of generated class statements and builds global collections before any Telegram request is encoded or decoded.
## 3. Scope
### In scope
- Generate deterministic type/function shard modules and compact lazy facades.
- Resolve public class attributes and constructor ids on first use, then cache them.
- Preserve miniproto.raw.functions.Name and miniproto.raw.types.Name imports.
- Preserve class identity, repr/module path, pickling, __all__, dir, and static typing.
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
Each facade contains compact immutable manifests:
- public name to shard module;
- constructor id to public name and shard module;
- namespace metadata needed by __dir__ and __all__.
Module __getattr__ imports the owning shard, obtains the class, normalizes its __module__ to the public facade, stores it in facade globals, and returns it. Repeated lookup returns the identical class object. __dir__ merges loaded globals with manifest names.
Import locking is delegated to importlib, but facade caching must tolerate two tasks/threads asking for one class concurrently.
### 4.3 Constructor registry
Replace eager maps of constructor id to every class with a resolver that looks up the compact manifest and imports only the owner shard. Cache resolved ids. decode_object pays one lazy import the first time a constructor family is encountered and direct dictionary lookup thereafter.
Inventory ALL_TYPES, ALL_FUNCTIONS, and CONSTRUCTORS consumers. Preserve documented behavior with a lazy Sequence/Mapping view or make an explicit pre-alpha internal change; do not accidentally materialize every class from codec initialization.
### 4.4 Cross-shard references
Generated serializers/deserializers must refer to TL field types by schema string or lazy resolver, never import all related shards. If straight-line code needs a class, generate a local resolver call. Verify recursive types and vectors.
### 4.5 Static typing and pickling
Generate types.pyi and functions.pyi with the same public class signatures, or an equivalent TYPE_CHECKING-only surface, so editors and ty see all attributes without runtime imports. Include stubs in the manifest and wheel.
Normalize public __module__ and ensure unpickling asks the facade for the class through __getattr__. Add pickle round trips for representative namespaced and root classes.
### 4.6 Performance targets
Measure at least five fresh subprocesses with warmed filesystem before and after:
- Median import miniproto wall time improves at least 60 percent from the same-machine cf7db29 baseline.
- Tracemalloc retained memory after import improves at least 50 percent.
- Importing Client and ClientConfig loads no private raw shard.
- After one warm-up decode/encode, existing TL benchmark medians regress no more than 5 percent.
If a target misses, profile and record why before merging; do not hide import work in the first Client constructor call.
### 4.7 Rejected alternatives
- Only making raw/__init__.py lazy is rejected because Client still imports monolithic modules.
- One module per class is rejected due filesystem and import overhead.
- Editing generated files by hand is rejected because generation checks overwrite them.
- Dropping type visibility is rejected because typed raw API is a project requirement.
## 5. Files to change
| File | Change |
| --- | --- |
| tools/schema/generate.py | Generate facades, stable shards, stubs, manifests, and stale-shard cleanup |
| src/miniproto/raw/types.py | Regenerated lazy facade |
| src/miniproto/raw/functions.py | Regenerated lazy facade |
| src/miniproto/raw/_types_shards/ | New generated type implementation shards |
| src/miniproto/raw/_function_shards/ | New generated request implementation shards |
| src/miniproto/raw/types.pyi | New generated public typing surface |
| src/miniproto/raw/functions.pyi | New generated public typing surface |
| src/miniproto/raw/__init__.py | Avoid eager facade loading where possible |
| src/miniproto/tl/codec.py | Resolve constructor ids lazily and cache |
| src/miniproto/client.py | Avoid operations that materialize raw registries at module import |
| tests/test_schema_generation.py | Determinism, stale cleanup, manifest, and stub tests |
| tests/test_tl_codec.py | Lazy resolution, class identity, recursive decode, and pickle tests |
| tools/bench/benchmark_runtime_paths.py | Add repeatable import and cold/warm raw measurements or a companion script |
| docs/development.md | Document generated layout and benchmark command |
## 6. Execution prerequisites
- Capture cf7db29 subprocess import time, tracemalloc retained/peak memory, sys.modules raw-module list, wheel size, and warmed TL benchmark results.
- Search all ALL_TYPES, ALL_FUNCTIONS, CONSTRUCTORS, constructor_id_map, __module__, and pickling consumers.
- Git workflow: read-only Git only; no branch, worktree, stage, commit, stash, revert, or push.
- STOP if public compatibility requires a different shard/facade contract; update this plan before generator edits.
- STOP if type stubs cannot represent the runtime API without changing user imports.
## 7. Implementation steps
1. Add a subprocess benchmark/test harness that records wall time, tracemalloc, and loaded raw modules for import miniproto, import Client, first raw attribute, and first decode. Record baseline outside generated output.  
   Verification: uv run python tools/bench/benchmark_imports.py, or the final equivalent command.
2. Add generator golden tests for stable bucket assignment, deterministic output, removed-shard cleanup, and check-mode drift.  
   Verification: uv run pytest tests/test_schema_generation.py
3. Generate private shards and keep current eager facades temporarily so the full schema suite proves shard code independently.  
   Verification: uv run python -m tools.schema.generate and uv run pytest tests/test_schema_generation.py tests/test_tl_codec.py
4. Generate lazy facades, manifests, __getattr__, __dir__, and cache behavior. Add root/namespaced imports, repeated identity, star-import, and concurrent lookup tests.  
   Verification: uv run pytest tests/test_schema_generation.py tests/test_tl_codec.py
5. Replace eager constructor maps with lazy id resolution. Test unknown ids, recursive objects, vectors, RPC results, and full representative schema round trips.  
   Verification: uv run pytest tests/test_tl_codec.py tests/test_invoke.py
6. Generate and package stubs. Run ty against representative imports and build a wheel to inspect included files.  
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
| Risk | Mitigation |
| --- | --- |
| First-use latency spikes | Stable moderate shard count and explicit cold benchmark |
| Class identity or pickle breaks | Facade cache, public __module__, fresh-process tests |
| Type completion disappears | Generated pyi surfaces |
| Shards become stale | Generator-owned manifest and stale cleanup |
| Warm decode slows | Cached id resolver and 5 percent regression gate |
## 12. Maintenance and references
- Owner: unassigned
- Review trigger: schema layer update, generator layout, constructor registry, raw public exports, packaging, or type-checker changes.
- Repository evidence: src/miniproto/__init__.py, src/miniproto/client.py, src/miniproto/raw/__init__.py, src/miniproto/raw/base.py, src/miniproto/raw/functions.py, src/miniproto/raw/types.py, src/miniproto/tl/codec.py, tools/schema/generate.py, tests/test_schema_generation.py, tests/test_tl_codec.py, tools/bench/benchmark_runtime_paths.py.
