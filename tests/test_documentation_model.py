"""Focused contracts for generated reference-page metadata."""

import json
from pathlib import Path

from tools.docs.manifest import build_reference_manifest, write_reference_tree
from tools.docs.model import ReferencePage


def test_generated_reference_pages_disable_source_edit_links() -> None:
    """Generated pages must point readers at provenance instead of an editor."""
    page = ReferencePage(
        path="python/miniproto/client.md",
        title="miniproto.client.Client",
        description="High-level Telegram client.",
        language="python",
        kind="class",
        qualified_name="miniproto.client.Client",
        source_path="src/miniproto/client.py",
        source_url="https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L250",
        body="Generated body.",
        module="miniproto.client",
    )

    assert "\neditUrl: false\n" in page.render()


def test_generated_reference_page_paths_are_posix_on_every_host() -> None:
    """Canonicalize structural Markdown and provenance paths instead of leaking host separators."""
    page = ReferencePage(
        path=r"python\miniproto\client.md",
        title="miniproto.client.Client",
        description="High-level Telegram client.",
        language="python",
        kind="class",
        qualified_name="miniproto.client.Client",
        source_path=r"src\miniproto\client.py",
        source_url="https://github.com/EDM115/miniproto/blob/master/src/miniproto/client.py#L250",
        body=r"A literal Windows example remains `C:\Users\developer\session`.",
        module="miniproto.client",
    )

    assert page.path == "python/miniproto/client.md"
    assert page.source_path == "src/miniproto/client.py"
    assert 'source_path: "src/miniproto/client.py"' in page.render()
    assert r"`C:\Users\developer\session`" in page.render()


def test_reference_manifest_tracks_machine_readable_relationship_artifacts(tmp_path: Path) -> None:
    """Non-Markdown relationship data must be committed and hashed beside page records."""
    page = ReferencePage(
        path="telegram/index.md",
        title="Telegram API",
        description="Telegram raw API index.",
        language="telegram",
        kind="index",
        qualified_name="telegram",
        source_path="tools/schema/schema.json",
        source_url="https://example.invalid/schema.json",
        body="Generated body.",
        namespace="global",
        layer=228,
        schema_source="tdlib",
    )
    relationships = '{"schema_version":1}\n'

    manifest = json.loads(
        build_reference_manifest(
            (page,),
            tool_versions={"generator": "1"},
            source_hashes={"schema": "abc"},
            artifacts={"telegram/relationships.json": relationships},
        )
    )
    write_reference_tree(
        tmp_path,
        (page,),
        tool_versions={"generator": "1"},
        source_hashes={"schema": "abc"},
        artifacts={"telegram/relationships.json": relationships},
    )

    assert manifest["artifacts"] == [
        {
            "path": "telegram/relationships.json",
            "sha256": "c5d130e87e377f65c0f77eda3629f01de137de88cd3b0a181aa1b6fda001afdc",
        }
    ]
    assert (tmp_path / "telegram/relationships.json").read_text(encoding="utf-8") == relationships
