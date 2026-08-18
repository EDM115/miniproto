"""Exercise deterministic static Rust reference-page normalization."""

from __future__ import annotations

import ast
import json
from pathlib import Path
from subprocess import CompletedProcess
from typing import Any

import pytest
import tools.docs.generate_rust as generate_rust
from tools.docs.audit import audit_maintained_rust_docs
from tools.docs.generate_rust import (
    RustDocumentationError,
    cargo_docs_md_command,
    cargo_docs_md_install_command,
    ensure_pinned_nightly_available,
    generate_pinned_rustdoc_json,
    generate_rust_pages,
    load_cargo_docs_md_fragments,
    load_documentation_toolchain,
    pinned_rustdoc_command,
)


def _rustdoc_fixture(*, reverse_index: bool = False, include_docs: bool = True) -> dict[str, Any]:
    """Build a minimal rustdoc JSON artifact with public and PyO3-only items.

    Args:
        reverse_index: Whether to reverse insertion order to exercise deterministic sorting.
        include_docs: Whether the selected Python-visible function receives documentation.

    Returns:
        Rustdoc JSON data covering module, item, method, generated, and private cases.
    """
    crypto_docs = "Seal packets for the native extension.\n\n# Arguments\n\n- `secret`: Bytes authenticated by the operation.\n- `nonce`: Sequence value used once per packet."
    index = {
        "0": {
            "crate_id": 0,
            "name": "miniproto_native",
            "docs": "Native acceleration crate.",
            "visibility": "public",
            "span": {"filename": "rust/miniproto/src/lib.rs", "begin": [1, 0], "end": [20, 1]},
            "inner": {"module": {"items": ["1", "5"]}},
        },
        "1": {
            "crate_id": 0,
            "name": "crypto",
            "docs": "Cryptographic native helpers.",
            "visibility": "crate",
            "span": {"filename": "rust/miniproto/src/crypto.rs", "begin": [1, 0], "end": [30, 1]},
            "inner": {"module": {"items": ["2", "3", "4"]}},
        },
        "2": {
            "crate_id": 0,
            "name": "seal",
            "docs": crypto_docs if include_docs else None,
            "visibility": "crate",
            "span": {"filename": "rust/miniproto/src/crypto.rs", "begin": [10, 0], "end": [16, 1]},
            "inner": {
                "function": {
                    "sig": {
                        "inputs": [["secret", {"primitive": "slice"}], ["nonce", {"primitive": "u32"}]],
                        "output": {"resolved_path": {"name": "PyResult"}},
                        "is_c_variadic": False,
                    }
                }
            },
        },
        "3": {
            "crate_id": 0,
            "name": "NativeCodec",
            "docs": "Maintain an incremental native codec.",
            "visibility": "crate",
            "span": {"filename": "rust/miniproto/src/crypto.rs", "begin": [20, 0], "end": [30, 1]},
            "inner": {"struct": {"generics": {"params": []}}},
        },
        "4": {
            "crate_id": 0,
            "name": "feed",
            "docs": "Append bytes to the codec.\n\n# Arguments\n\n- `bytes`: Encoded bytes to append.",
            "visibility": "crate",
            "parent": "3",
            "span": {"filename": "rust/miniproto/src/crypto.rs", "begin": [25, 0], "end": [29, 1]},
            "inner": {
                "function": {
                    "sig": {
                        "inputs": [["self", {"generic": "Self"}], ["bytes", {"primitive": "slice"}]],
                        "output": None,
                        "is_c_variadic": False,
                    }
                }
            },
        },
        "5": {
            "crate_id": 0,
            "name": "PublicError",
            "docs": "Report a public native error.",
            "visibility": "public",
            "span": {"filename": "rust/miniproto/src/lib.rs", "begin": [12, 0], "end": [15, 1]},
            "inner": {"enum": {"generics": {"params": []}}},
        },
        "6": {
            "crate_id": 0,
            "name": "generated_codec",
            "docs": None,
            "visibility": "public",
            "span": {"filename": "rust/miniproto/src/generated_tl.rs", "begin": [1, 0], "end": [3, 1]},
            "inner": {
                "function": {
                    "sig": {"inputs": [["value", {"primitive": "u32"}]], "output": None, "is_c_variadic": False}
                }
            },
        },
        "7": {
            "crate_id": 0,
            "name": "private_helper",
            "docs": "Remain an implementation detail.",
            "visibility": "crate",
            "span": {"filename": "rust/miniproto/src/crypto.rs", "begin": [32, 0], "end": [34, 1]},
            "inner": {"function": {"sig": {"inputs": [], "output": None, "is_c_variadic": False}}},
        },
    }
    if reverse_index:
        index = dict(reversed(tuple(index.items())))
    return {
        "format_version": 42,
        "root": "0",
        "index": index,
        "paths": {
            "0": {"path": ["miniproto_native"], "kind": "module"},
            "1": {"path": ["miniproto_native", "crypto"], "kind": "module"},
            "2": {"path": ["miniproto_native", "crypto", "seal"], "kind": "function"},
            "3": {"path": ["miniproto_native", "crypto", "NativeCodec"], "kind": "struct"},
            "4": {"path": ["miniproto_native", "crypto", "NativeCodec", "feed"], "kind": "function"},
            "5": {"path": ["miniproto_native", "PublicError"], "kind": "enum"},
            "6": {"path": ["miniproto_native", "generated_codec"], "kind": "function"},
            "7": {"path": ["miniproto_native", "crypto", "private_helper"], "kind": "function"},
        },
    }


def _format_61_pymethod_fixture() -> dict[str, object]:
    """Return a rustdoc format-61-shaped inherent PyO3 implementation fixture.

    Returns:
        Rustdoc data whose methods are linked only through ``inner.impl``.
    """
    return {
        "format_version": 61,
        "root": "0",
        "index": {
            "0": {
                "crate_id": 0,
                "name": "miniproto_native",
                "docs": "Native acceleration crate.",
                "visibility": "public",
                "span": {"filename": "rust/miniproto/src/lib.rs", "begin": [1, 0], "end": [2, 1]},
                "inner": {"module": {"items": ["1"]}},
            },
            "1": {
                "crate_id": 0,
                "name": "crypto",
                "docs": "Cryptographic native helpers.",
                "visibility": "crate",
                "span": {"filename": "rust/miniproto/src/crypto.rs", "begin": [1, 0], "end": [16, 1]},
                "inner": {"module": {"items": ["3", "8"]}},
            },
            "3": {
                "crate_id": 0,
                "name": "NativeCodec",
                "docs": "Maintain an incremental native codec.",
                "visibility": "crate",
                "span": {"filename": "rust/miniproto/src/crypto.rs", "begin": [2, 0], "end": [3, 19]},
                "inner": {"struct": {"kind": {"unit": None}, "generics": {"params": []}, "impls": ["8"]}},
            },
            "4": {
                "crate_id": 0,
                "name": "new",
                "docs": "Create a codec.\n\n# Arguments\n\n- `limit`: Maximum buffered bytes.",
                "visibility": "crate",
                "span": {"filename": "rust/miniproto/src/crypto.rs", "begin": [8, 4], "end": [8, 48]},
                "inner": {
                    "function": {
                        "sig": {
                            "inputs": [["limit", {"primitive": "usize"}]],
                            "output": {"generic": "Self"},
                            "is_c_variadic": False,
                        },
                        "generics": {"params": [], "where_predicates": []},
                    }
                },
            },
            "5": {
                "crate_id": 0,
                "name": "feed",
                "docs": "Append bytes.\n\n# Arguments\n\n- `bytes`: Encoded bytes to append.",
                "visibility": "crate",
                "span": {"filename": "rust/miniproto/src/crypto.rs", "begin": [11, 4], "end": [11, 48]},
                "inner": {
                    "function": {
                        "sig": {
                            "inputs": [["self", {"generic": "Self"}], ["bytes", {"primitive": "slice"}]],
                            "output": None,
                            "is_c_variadic": False,
                        },
                        "generics": {"params": [], "where_predicates": []},
                    }
                },
            },
            "8": {
                "crate_id": 0,
                "name": None,
                "docs": None,
                "visibility": "crate",
                "span": {"filename": "rust/miniproto/src/crypto.rs", "begin": [5, 0], "end": [13, 1]},
                "inner": {
                    "impl": {
                        "is_unsafe": False,
                        "generics": {"params": [], "where_predicates": []},
                        "provided_trait_methods": [],
                        "trait": None,
                        "for": {"resolved_path": {"name": "NativeCodec", "id": "3", "args": None}},
                        "items": ["4", "5"],
                        "is_negative": False,
                        "is_synthetic": False,
                        "blanket_impl": None,
                    }
                },
            },
        },
        "paths": {
            "0": {"path": ["miniproto_native"], "kind": "module"},
            "1": {"path": ["miniproto_native", "crypto"], "kind": "module"},
            "3": {"path": ["miniproto_native", "crypto", "NativeCodec"], "kind": "struct"},
        },
    }


def _write_format_61_pymethod_sources(root: Path) -> None:
    """Write PyO3 class source matching ``_format_61_pymethod_fixture``.

    Args:
        root: Temporary repository root receiving maintained Rust source.
    """
    source = root / "rust/miniproto/src"
    source.mkdir(parents=True)
    (source / "lib.rs").write_text("//! Native acceleration crate.\n", encoding="utf-8")
    (source / "crypto.rs").write_text(
        "//! Cryptographic native helpers.\n"
        '#[pyclass(module = "miniproto._native")]\n'
        "struct NativeCodec;\n\n"
        "#[pymethods]\n"
        "impl NativeCodec {\n"
        "    #[new]\n"
        "    fn new(limit: usize) -> Self { Self }\n\n"
        '    #[pyo3(name = "push_bytes")]\n'
        "    fn feed(&mut self, bytes: &[u8]) {}\n"
        "}\n",
        encoding="utf-8",
    )


def _write_fixture_sources(root: Path) -> None:
    """Write static Rust source snippets used solely for PyO3 provenance detection.

    Args:
        root: Temporary repository root that receives the minimal Rust source tree.
    """
    source = root / "rust/miniproto/src"
    source.mkdir(parents=True)
    (source / "lib.rs").write_text("pub enum PublicError { Invalid }\n", encoding="utf-8")
    (source / "crypto.rs").write_text(
        '#[pyfunction(name = "seal_packet")]\n'
        "fn seal(secret: &[u8], nonce: u32) {}\n\n"
        '#[pyclass(module = "miniproto._native")]\n'
        "struct NativeCodec;\n\n"
        "#[pymethods]\n"
        "impl NativeCodec {\n"
        "    fn feed(&mut self, bytes: &[u8]) {}\n"
        "}\n\n"
        "fn private_helper() {}\n",
        encoding="utf-8",
    )
    (source / "generated_tl.rs").write_text("fn generated_codec(value: u32) {}\n", encoding="utf-8")


def _write_rustdoc_json(root: Path, payload: dict[str, object]) -> Path:
    """Persist one fixture rustdoc artifact below a temporary repository root.

    Args:
        root: Temporary repository root receiving the JSON artifact.
        payload: Rustdoc JSON content to serialize deterministically for the test.

    Returns:
        Path to the persisted JSON artifact.
    """
    artifact = root / "miniproto_native.json"
    artifact.write_text(json.dumps(payload), encoding="utf-8")
    return artifact


def _write_whole_rust_audit_fixture(root: Path) -> Path:
    """Write maintained source and matching rustdoc JSON for whole-source auditing.

    Args:
        root: Temporary repository root receiving source and rustdoc JSON.

    Returns:
        Path to the format-61 rustdoc JSON fixture.
    """
    source = """//! Maintained crate documentation.

/// Events emitted by the fixture.
enum Event {
    /// A token event. The contained `u32` is the wire token.
    Token(u32),
    /// A bad token event without tuple-field coverage.
    Bad(u64),
    /// An event with one named field.
    Named {
        missing: u8,
    },
}

/// A wrapper containing a `u16` value.
struct Wrapper(u16);

/// Process a value.
///
/// # Arguments
///
/// - `T`: Value type processed by the helper.
/// - `value`: Value supplied to the callback.
fn private_helper<T, const N: usize>(value: T, callback: impl Fn(T)) {}

const UNDOCUMENTED: u8 = 1;

#[cfg(test)]
/// Unit tests for the fixture.
mod tests {
    #[test]
    fn undocumented_test() {}
}
"""
    source_dir = root / "rust/miniproto/src"
    source_dir.mkdir(parents=True)
    (source_dir / "lib.rs").write_text(source, encoding="utf-8")
    (source_dir / "generated_tl.rs").write_text("pub const GENERATED: u8 = 1;\n", encoding="utf-8")

    def line_of(needle: str) -> int:
        """Return the one-based fixture line containing ``needle``.

        Args:
            needle: Unique source text whose line is required.
        """
        return next(index for index, line in enumerate(source.splitlines(), 1) if needle in line)

    event_line = line_of("enum Event")
    token_line = line_of("Token(u32)")
    bad_line = line_of("Bad(u64)")
    named_line = line_of("Named {")
    field_line = line_of("missing: u8")
    wrapper_line = line_of("struct Wrapper")
    helper_line = line_of("fn private_helper")
    constant_line = line_of("const UNDOCUMENTED")
    tests_line = line_of("mod tests")
    source_end_line = len(source.splitlines())
    payload = {
        "format_version": 61,
        "root": "0",
        "index": {
            "0": {
                "crate_id": 0,
                "name": "miniproto_native",
                "docs": "Maintained crate documentation.",
                "span": {"filename": "rust/miniproto/src/lib.rs", "begin": [1, 0], "end": [source_end_line, 1]},
                "inner": {"module": {"items": ["1", "8", "9", "10", "13", "15", "17"]}},
            },
            "1": {
                "crate_id": 0,
                "name": "Event",
                "docs": "Events emitted by the fixture.",
                "span": {"filename": "rust/miniproto/src/lib.rs", "begin": [event_line, 0], "end": [13, 1]},
                "inner": {"enum": {"generics": {"params": []}, "variants": ["2", "4", "6"], "impls": []}},
            },
            "2": {
                "crate_id": 0,
                "name": "Token",
                "docs": "A token event. The contained `u32` is the wire token.",
                "span": {"filename": "rust/miniproto/src/lib.rs", "begin": [token_line, 4], "end": [token_line, 15]},
                "inner": {"variant": {"kind": {"tuple": ["3"]}, "discriminant": None}},
            },
            "3": {
                "crate_id": 0,
                "name": "0",
                "docs": None,
                "span": {"filename": "rust/miniproto/src/lib.rs", "begin": [token_line, 10], "end": [token_line, 13]},
                "inner": {"struct_field": {"primitive": "u32"}},
            },
            "4": {
                "crate_id": 0,
                "name": "Bad",
                "docs": "A bad token event without tuple-field coverage.",
                "span": {"filename": "rust/miniproto/src/lib.rs", "begin": [bad_line, 4], "end": [bad_line, 13]},
                "inner": {"variant": {"kind": {"tuple": ["5"]}, "discriminant": None}},
            },
            "5": {
                "crate_id": 0,
                "name": "0",
                "docs": None,
                "span": {"filename": "rust/miniproto/src/lib.rs", "begin": [bad_line, 8], "end": [bad_line, 11]},
                "inner": {"struct_field": {"primitive": "u64"}},
            },
            "6": {
                "crate_id": 0,
                "name": "Named",
                "docs": "An event with one named field.",
                "span": {"filename": "rust/miniproto/src/lib.rs", "begin": [named_line, 4], "end": [12, 5]},
                "inner": {"variant": {"kind": {"struct": ["7"]}, "discriminant": None}},
            },
            "7": {
                "crate_id": 0,
                "name": "missing",
                "docs": None,
                "span": {"filename": "rust/miniproto/src/lib.rs", "begin": [field_line, 8], "end": [field_line, 19]},
                "inner": {"struct_field": {"primitive": "u8"}},
            },
            "8": {
                "crate_id": 0,
                "name": "private_helper",
                "docs": "Process a value.\n\n# Arguments\n\n- `T`: Value type processed by the helper.\n- `value`: Value supplied to the callback.",
                "span": {"filename": "rust/miniproto/src/lib.rs", "begin": [helper_line, 0], "end": [helper_line, 80]},
                "inner": {
                    "function": {
                        "sig": {
                            "inputs": [["value", {"generic": "T"}], ["callback", {"impl_trait": []}]],
                            "output": None,
                            "is_c_variadic": False,
                        },
                        "generics": {
                            "params": [
                                {"name": "T", "kind": {"type": {"bounds": [], "default": None}}},
                                {"name": "N", "kind": {"const": {"type": {"primitive": "usize"}, "default": None}}},
                                {
                                    "name": "impl Fn(T)",
                                    "kind": {"type": {"bounds": [], "default": None, "is_synthetic": True}},
                                },
                            ],
                            "where_predicates": [],
                        },
                    }
                },
            },
            "9": {
                "crate_id": 0,
                "name": "UNDOCUMENTED",
                "docs": None,
                "span": {
                    "filename": "rust/miniproto/src/lib.rs",
                    "begin": [constant_line, 0],
                    "end": [constant_line, 28],
                },
                "inner": {"constant": {"type": {"primitive": "u8"}, "const": "1"}},
            },
            "10": {
                "crate_id": 0,
                "name": "tests",
                "docs": "Unit tests for the fixture.",
                "span": {
                    "filename": "rust/miniproto/src/lib.rs",
                    "begin": [tests_line, 0],
                    "end": [source_end_line, 1],
                },
                "inner": {"module": {"items": []}},
            },
            "11": {
                "crate_id": 0,
                "name": "__pyfunction_private_helper",
                "docs": None,
                "span": {"filename": "rust/miniproto/src/lib.rs", "begin": [helper_line, 0], "end": [helper_line, 80]},
                "inner": {"function": {"sig": {"inputs": [], "output": None}, "generics": {"params": []}}},
            },
            "12": {
                "crate_id": 0,
                "name": "GENERATED",
                "docs": None,
                "span": {"filename": "rust/miniproto/src/generated_tl.rs", "begin": [1, 0], "end": [1, 28]},
                "inner": {"constant": {"type": {"primitive": "u8"}, "const": "1"}},
            },
            "13": {
                "crate_id": 0,
                "name": "Wrapper",
                "docs": "A wrapper containing a `u16` value.",
                "span": {
                    "filename": "rust/miniproto/src/lib.rs",
                    "begin": [wrapper_line, 0],
                    "end": [wrapper_line, 20],
                },
                "inner": {
                    "struct": {
                        "kind": {"tuple": ["14"]},
                        "generics": {"params": [], "where_predicates": []},
                        "impls": [],
                    }
                },
            },
            "14": {
                "crate_id": 0,
                "name": "0",
                "docs": None,
                "span": {
                    "filename": "rust/miniproto/src/lib.rs",
                    "begin": [wrapper_line, 15],
                    "end": [wrapper_line, 18],
                },
                "inner": {"struct_field": {"primitive": "u16"}},
            },
            "15": {
                "crate_id": 0,
                "name": "__MacroTuple",
                "docs": None,
                "span": {
                    "filename": "rust/miniproto/src/lib.rs",
                    "begin": [wrapper_line, 0],
                    "end": [wrapper_line, 20],
                },
                "inner": {
                    "struct": {
                        "kind": {"tuple": ["16"]},
                        "generics": {"params": [], "where_predicates": []},
                        "impls": [],
                    }
                },
            },
            "16": {
                "crate_id": 0,
                "name": "0",
                "docs": None,
                "span": {
                    "filename": "rust/miniproto/src/lib.rs",
                    "begin": [wrapper_line, 15],
                    "end": [wrapper_line, 18],
                },
                "inner": {"struct_field": {"primitive": "u16"}},
            },
            "17": {
                "crate_id": 0,
                "name": "__macro_module",
                "docs": None,
                "span": {
                    "filename": "rust/miniproto/src/lib.rs",
                    "begin": [wrapper_line, 0],
                    "end": [wrapper_line, 20],
                },
                "inner": {"module": {"items": []}},
            },
        },
        "paths": {
            "0": {"path": ["miniproto_native"], "kind": "module"},
            "1": {"path": ["miniproto_native", "Event"], "kind": "enum"},
            "8": {"path": ["miniproto_native", "private_helper"], "kind": "function"},
            "9": {"path": ["miniproto_native", "UNDOCUMENTED"], "kind": "constant"},
            "10": {"path": ["miniproto_native", "tests"], "kind": "module"},
            "13": {"path": ["miniproto_native", "Wrapper"], "kind": "struct"},
        },
    }
    return _write_rustdoc_json(root, payload)


def _rendered_markdown() -> dict[str, str]:
    """Return fixture Markdown standing in for pinned cargo-docs-md output.

    Returns:
        Complete item bodies keyed by rustdoc item id.
    """
    return {
        "0": (
            "# miniproto_native\n\nNative acceleration crate.\n\n"
            "## Modules\n\n"
            "- [`crypto`](crypto/index.md) — Maintained helpers.\n"
            "- [`generated_tl`](generated_tl/index.md) — Generated constructor metadata."
        ),
        "1": "# crypto\n\nCryptographic native helpers.",
        "2": "# seal\n\nSeal packets for the native extension.",
        "3": "# NativeCodec\n\nMaintain an incremental native codec.",
        "4": "# feed\n\nAppend bytes to the codec.",
        "5": "# PublicError\n\nReport a public native error.",
    }


def test_rust_documentation_toolchain_is_exact_and_runtime_import_free() -> None:
    """Keep the docs-only nightly/renderer pin explicit without importing miniproto runtime code."""
    toolchain = load_documentation_toolchain()
    rustdoc = pinned_rustdoc_command(
        toolchain=toolchain, manifest_path=Path("rust/miniproto/Cargo.toml"), target_dir=Path("target/rustdoc-json")
    )
    renderer = cargo_docs_md_command(
        json_directory=Path("target/rustdoc-json/doc"),
        output_directory=Path("target/cargo-docs-md"),
        crate="miniproto_native",
    )
    imports = [
        alias.name
        for statement in ast.walk(ast.parse(Path(generate_rust.__file__).read_text(encoding="utf-8")))
        if isinstance(statement, (ast.Import, ast.ImportFrom))
        for alias in statement.names
    ]

    assert toolchain.nightly == "nightly-2026-08-12"
    assert cargo_docs_md_install_command(toolchain) == (
        "cargo",
        "install",
        "--locked",
        "cargo-docs-md",
        "--version",
        "0.2.4",
    )
    assert rustdoc[0:3] == ("cargo", "+nightly-2026-08-12", "rustdoc")
    assert rustdoc[-6:] == ("--", "-Z", "unstable-options", "--output-format", "json", "--document-private-items")
    assert "RUSTC_BOOTSTRAP" not in rustdoc
    assert {"--source-locations", "--full-method-docs", "--no-mdbook", "--no-search-index"}.issubset(renderer)
    assert all(not imported_name.startswith("miniproto") for imported_name in imports)


def test_pinned_nightly_detection_accepts_rustup_target_suffix() -> None:
    """Treat rustup's normal host-qualified toolchain name as the exact pin."""
    toolchain = load_documentation_toolchain()

    ensure_pinned_nightly_available(
        toolchain,
        runner=lambda *args, **kwargs: CompletedProcess(
            args=args[0], returncode=0, stdout=f"{toolchain.nightly}-x86_64-pc-windows-msvc\n", stderr=""
        ),
    )


def test_cargo_docs_md_fragments_preserve_real_module_and_item_sections(tmp_path: Path) -> None:
    """Split cargo-docs-md's per-module output without reconstructing its Markdown.

    Args:
        tmp_path: Pytest-provided staging root.
    """
    payload = _rustdoc_fixture()
    rustdoc_json = tmp_path / "miniproto_native.json"
    rustdoc_json.write_text(json.dumps(payload), encoding="utf-8")
    output = tmp_path / "rendered" / "miniproto_native"
    (output / "crypto").mkdir(parents=True)
    (output / "index.md").write_text("# Crate `miniproto_native`\n\nNative crate body.\n", encoding="utf-8")
    (output / "crypto" / "index.md").write_text(
        "# Module `crypto`\n\nModule body.\n\n"
        "## Functions\n\n"
        "### `seal`\n\n```rust\nfn seal(secret: &[u8], nonce: u32)\n```\n\nSeal body.\n\n"
        "## Structs\n\n"
        "### `NativeCodec`\n\n```rust\nstruct NativeCodec;\n```\n\nCodec body.\n\n"
        "#### Implementations\n\n"
        '- <span id="nativecodec-feed"></span>`fn feed(&mut self, bytes: &[u8])`\n\n'
        "  Append rendered bytes.\n\n"
        '- <span id="nativecodec-other"></span>`fn other(&self)`\n\n  Other body.\n',
        encoding="utf-8",
    )

    fragments = load_cargo_docs_md_fragments(
        rustdoc_json=rustdoc_json, output_directory=tmp_path / "rendered", crate="miniproto_native"
    )

    assert fragments["0"].startswith("# Crate `miniproto_native`")
    assert fragments["1"].startswith("# Module `crypto`")
    assert fragments["2"].startswith("### `seal`")
    assert "NativeCodec" not in fragments["2"]
    assert fragments["3"].startswith("### `NativeCodec`")
    assert fragments["4"].startswith('- <span id="nativecodec-feed"')
    assert "Append rendered bytes." in fragments["4"]
    assert "nativecodec-other" not in fragments["4"]


def test_live_rustdoc_generation_resolves_relative_paths_once(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Avoid duplicating a relative manifest below the Cargo working directory.

    Args:
        tmp_path: Pytest-provided repository root.
        monkeypatch: Pytest helper used to make the manifest path relative.
    """
    crate_root = tmp_path / "crate"
    crate_root.mkdir()
    manifest = crate_root / "Cargo.toml"
    manifest.write_text("[package]\nname='fixture'\nversion='0.1.0'\n", encoding="utf-8")
    target = tmp_path / "target"
    toolchain = load_documentation_toolchain()

    def runner(argv: tuple[str, ...], **kwargs: object) -> CompletedProcess[str]:
        """Return deterministic rustup/Cargo results and materialize the fixture artifact.

        Args:
            argv: Process argument vector requested by the generator.
            **kwargs: Subprocess options whose working directory is verified.
        """
        if argv[:3] == ("rustup", "toolchain", "list"):
            return CompletedProcess(argv, 0, stdout=f"{toolchain.nightly}-x86_64-pc-windows-msvc\n", stderr="")
        manifest_argument = Path(argv[argv.index("--manifest-path") + 1])
        assert manifest_argument == manifest.resolve()
        assert kwargs["cwd"] == crate_root.resolve()
        artifact = target.resolve() / "doc" / "fixture.json"
        artifact.parent.mkdir(parents=True)
        artifact.write_text("{}", encoding="utf-8")
        return CompletedProcess(argv, 0, stdout="", stderr="")

    monkeypatch.chdir(tmp_path)

    artifact = generate_pinned_rustdoc_json(
        toolchain=toolchain,
        manifest_path=Path("crate/Cargo.toml"),
        target_dir=Path("target"),
        artifact_stem="fixture",
        runner=runner,
    )

    assert artifact == target.resolve() / "doc" / "fixture.json"


def test_rust_reference_pages_are_deterministic_and_keep_provenance(tmp_path: Path) -> None:
    """Normalize equivalent artifacts to identical, split pages with source/PyO3 provenance.

    Args:
        tmp_path: Pytest-provided temporary repository root.
    """
    _write_fixture_sources(tmp_path)
    forward = generate_rust_pages(
        rustdoc_json=_write_rustdoc_json(tmp_path, _rustdoc_fixture()),
        source_root=tmp_path,
        rendered_markdown=_rendered_markdown(),
        repository_url="https://example.invalid/miniproto",
        crate="miniproto-native",
        reviewed_modules=("crypto",),
    )
    reverse = generate_rust_pages(
        rustdoc_json=_write_rustdoc_json(tmp_path, _rustdoc_fixture(reverse_index=True)),
        source_root=tmp_path,
        rendered_markdown=_rendered_markdown(),
        repository_url="https://example.invalid/miniproto",
        crate="miniproto-native",
        reviewed_modules=("crypto",),
    )

    assert forward == reverse
    pages = {page.qualified_name: page for page in forward}
    assert set(pages) == {
        "miniproto_native",
        "file:rust/miniproto/src/lib.rs",
        "file:rust/miniproto/src/crypto.rs",
        "miniproto_native::crypto",
        "miniproto_native::crypto::seal",
        "miniproto_native::crypto::NativeCodec",
        "miniproto_native::crypto::NativeCodec::feed",
        "miniproto_native::PublicError",
    }
    assert pages["miniproto_native::crypto"].path == "rust/miniproto-native/crypto/index.md"
    assert pages["miniproto_native::crypto::seal"].source_path == "rust/miniproto/src/crypto.rs"
    assert pages["miniproto_native::crypto::seal"].python_visible is True
    assert "miniproto._native.seal_packet" in pages["miniproto_native::crypto::seal"].body
    assert pages["miniproto_native::crypto::NativeCodec::feed"].python_visible is True


def test_format_61_pymethods_keep_constructor_and_renamed_method_provenance(tmp_path: Path) -> None:
    """Map a PyO3 constructor and renamed method to names Python actually exposes.

    Args:
        tmp_path: Pytest-provided temporary repository root.
    """
    _write_format_61_pymethod_sources(tmp_path)
    payload = _format_61_pymethod_fixture()
    pages = generate_rust_pages(
        rustdoc_json=_write_rustdoc_json(tmp_path, payload),
        source_root=tmp_path,
        rendered_markdown={item_id: f"# rendered {item_id}" for item_id in ("0", "1", "3", "4", "5")},
        repository_url="https://example.invalid/miniproto",
        crate="miniproto-native",
        reviewed_modules=("crypto",),
    )

    pages_by_name = {page.qualified_name: page for page in pages}
    constructor = pages_by_name["miniproto_native::crypto::NativeCodec::new"]
    renamed = pages_by_name["miniproto_native::crypto::NativeCodec::feed"]
    assert constructor.aliases == ("miniproto._native.NativeCodec",)
    assert "miniproto._native.NativeCodec.new" not in constructor.body
    assert renamed.aliases == ("miniproto._native.NativeCodec.push_bytes",)


def test_rust_reference_pages_preserve_every_function_argument(tmp_path: Path) -> None:
    """Expose every rustdoc function argument in the structural declaration summary.

    Args:
        tmp_path: Pytest-provided temporary repository root.
    """
    _write_fixture_sources(tmp_path)

    pages = generate_rust_pages(
        rustdoc_json=_write_rustdoc_json(tmp_path, _rustdoc_fixture()),
        source_root=tmp_path,
        rendered_markdown=_rendered_markdown(),
        repository_url="https://example.invalid/miniproto",
        crate="miniproto-native",
        reviewed_modules=("crypto",),
    )

    body = {page.qualified_name: page.body for page in pages}["miniproto_native::crypto::seal"]
    assert "fn seal(secret: slice, nonce: u32) -> PyResult" in body
    assert "- `secret`: Bytes authenticated by the operation." in body
    assert "- `nonce`: Sequence value used once per packet." in body


def test_rust_reference_pages_exclude_generator_owned_rust(tmp_path: Path) -> None:
    """Leave generated TL declarations outside committed Rust reference pages.

    Args:
        tmp_path: Pytest-provided temporary repository root.
    """
    _write_fixture_sources(tmp_path)

    pages = generate_rust_pages(
        rustdoc_json=_write_rustdoc_json(tmp_path, _rustdoc_fixture()),
        source_root=tmp_path,
        rendered_markdown=_rendered_markdown(),
        repository_url="https://example.invalid/miniproto",
        crate="miniproto-native",
        reviewed_modules=("crypto",),
    )

    assert all("generated_codec" not in page.qualified_name for page in pages)
    assert all("generated_tl.rs" not in page.source_path for page in pages)
    crate_body = next(page.body for page in pages if page.qualified_name == "miniproto_native")
    assert "[`crypto`](crypto/index.md)" in crate_body
    assert "[`generated_tl`](generated_tl/index.md)" not in crate_body
    assert "`generated_tl` — Generated constructor metadata." in crate_body


def test_rust_reference_pages_fail_honestly_for_missing_selected_docs(tmp_path: Path) -> None:
    """Reject an undocumented Python-visible item instead of manufacturing prose.

    Args:
        tmp_path: Pytest-provided temporary repository root.
    """
    _write_fixture_sources(tmp_path)

    with pytest.raises(RustDocumentationError, match=r"miniproto_native::crypto::seal.*crypto\.rs:10"):
        generate_rust_pages(
            rustdoc_json=_write_rustdoc_json(tmp_path, _rustdoc_fixture(include_docs=False)),
            source_root=tmp_path,
            rendered_markdown=_rendered_markdown(),
            repository_url="https://example.invalid/miniproto",
            crate="miniproto-native",
            reviewed_modules=("crypto",),
        )


def test_rust_reference_pages_require_non_lifetime_generic_descriptions(tmp_path: Path) -> None:
    """Treat type and const generics as explicit documented parameters.

    Args:
        tmp_path: Pytest-provided temporary repository root.
    """
    _write_fixture_sources(tmp_path)
    payload = _rustdoc_fixture()
    function = payload["index"]["2"]["inner"]["function"]
    function["generics"] = {
        "params": [
            {"name": "'py", "kind": {"lifetime": {"outlives": []}}},
            {"name": "T", "kind": {"type": {"bounds": [], "default": None, "is_synthetic": False}}},
        ],
        "where_predicates": [],
    }

    with pytest.raises(RustDocumentationError, match=r"miniproto_native::crypto::seal.*`T`"):
        generate_rust_pages(
            rustdoc_json=_write_rustdoc_json(tmp_path, payload),
            source_root=tmp_path,
            rendered_markdown=_rendered_markdown(),
            repository_url="https://example.invalid/miniproto",
            crate="miniproto-native",
            reviewed_modules=("crypto",),
        )


def test_whole_rust_audit_is_source_span_aware_and_covers_private_declarations(tmp_path: Path) -> None:
    """Audit maintained modules, fields, tuple fields, and tests without macro noise.

    Args:
        tmp_path: Pytest-provided temporary repository root.
    """
    report = audit_maintained_rust_docs(
        _write_whole_rust_audit_fixture(tmp_path),
        source_root=tmp_path,
        maintained_paths=("rust/miniproto/src/lib.rs",),
        excluded_paths=("rust/miniproto/src/generated_tl.rs",),
    )

    assert report.documentation_unit_count == 14
    assert report.named_declaration_count == 8
    assert report.module_count == 2
    assert report.test_function_count == 1
    assert report.tuple_field_count == 3
    assert {(issue.qualified_name, issue.kind) for issue in report.missing_docs} == {
        ("miniproto_native::Event::Bad::0", "tuple_field"),
        ("miniproto_native::Event::Named::missing", "struct_field"),
        ("miniproto_native::UNDOCUMENTED", "constant"),
        ("miniproto_native::tests::undocumented_test", "test_function"),
    }
    assert all("__pyfunction" not in issue.qualified_name for issue in report.missing_docs)
    assert all("generated_tl.rs" not in issue.path for issue in report.missing_docs)


def test_whole_rust_audit_requires_value_type_and_const_parameter_descriptions(tmp_path: Path) -> None:
    """Require descriptions for every non-receiver value, type, and const parameter.

    Args:
        tmp_path: Pytest-provided temporary repository root.
    """
    report = audit_maintained_rust_docs(
        _write_whole_rust_audit_fixture(tmp_path),
        source_root=tmp_path,
        maintained_paths=("rust/miniproto/src/lib.rs",),
        excluded_paths=("rust/miniproto/src/generated_tl.rs",),
    )

    assert report.function_count == 1
    assert report.value_parameter_count == 2
    assert report.generic_parameter_count == 2
    assert [(issue.qualified_name, issue.arguments) for issue in report.missing_parameter_docs] == [
        ("miniproto_native::private_helper", ("N", "callback"))
    ]
