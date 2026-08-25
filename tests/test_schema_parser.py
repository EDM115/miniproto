from __future__ import annotations

from pathlib import Path

import pytest
from tools.schema.parser import TLSchemaParseError, parse_schema, parse_schema_file

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "tools" / "schema" / "schema.tl"
FIXTURE = ROOT / "tests" / "fixtures" / "schema" / "layer223-slice.tl"
TDLIB_FIXTURE = ROOT / "tests" / "fixtures" / "schema" / "tdlib-layer228-slice.tl"


def test_parser_reads_full_official_schema_mirror() -> None:
    schema = parse_schema_file(SCHEMA)
    assert len(schema.constructors) == 1663
    assert len(schema.functions) == 817
    assert len(schema.ignored_declarations) == 8
    help_config = next(entry for entry in schema.functions if entry.name == "help.getConfig")
    assert help_config.constructor_id_hex == "c4f9186b"
    assert help_config.namespace == "help"
    assert help_config.result_type == "Config"
    assert any(entry.name == "ephemeral.editMessage" for entry in schema.functions)
    assert any(entry.name == "inputPeerPhotoFileLocationLegacy" for entry in schema.constructors)
    assert not any(entry.name == "null" for entry in schema.constructors)
    join_channel = next(entry for entry in schema.functions if entry.name == "channels.joinChannel")
    assert join_channel.constructor_id_hex == "7f6a1e22"
    assert join_channel.result_type == "messages.ChatInviteJoinResult"
    contacts_search = next(entry for entry in schema.functions if entry.name == "contacts.search")
    assert contacts_search.constructor_id_hex == "5f58d0f"
    assert any(param.name == "broadcasts" and param.flag == "flags" for param in contacts_search.params)


def test_parser_handles_real_flags_vectors_generics_and_reserved_names() -> None:
    schema = parse_schema_file(SCHEMA)
    user = next(entry for entry in schema.constructors if entry.name == "user")
    assert any(param.name == "flags2" and param.is_flags_marker for param in user.params)
    assert any(param.name == "usernames" and param.flag == "flags2" and param.is_vector for param in user.params)
    send_message = next(entry for entry in schema.functions if entry.name == "messages.sendMessage")
    assert send_message.namespace == "messages"
    assert any(param.name == "no_webpage" and param.is_true_flag for param in send_message.params)
    assert any(param.name == "entities" and param.vector_item_type == "MessageEntity" for param in send_message.params)
    invoke_with_layer = next(entry for entry in schema.functions if entry.name == "invokeWithLayer")
    assert any(param.name == "X" and param.is_template for param in invoke_with_layer.params)
    assert any(param.name == "query" and param.type == "!X" for param in invoke_with_layer.params)
    story_header = next(entry for entry in schema.constructors if entry.name == "storyFwdHeader")
    from_param = next(param for param in story_header.params if param.name == "from")
    assert from_param.python_name == "from_"


def test_tdlib_parser_fixture_is_copied_from_pinned_canonical_schema_lines() -> None:
    official_lines = set(SCHEMA.read_text(encoding="utf-8").splitlines())
    fixture_lines = [
        line for line in TDLIB_FIXTURE.read_text(encoding="utf-8").splitlines() if line != "---functions---"
    ]
    assert fixture_lines
    assert all(line in official_lines for line in fixture_lines)


def test_parser_reads_json_schema_slice(tmp_path: Path) -> None:
    schema_path = tmp_path / "schema.json"
    schema_path.write_text(
        """{
  "constructors": [
    {"id": "-1720552011", "predicate": "boolTrue", "params": [], "type": "Bool"},
    {
      "id": "3089555792",
      "predicate": "storyFwdHeader",
      "params": [
        {"name": "flags", "type": "#"},
        {"name": "modified", "type": "flags.3?true"},
        {"name": "from", "type": "flags.0?Peer"},
        {"name": "story_id", "type": "flags.2?int"}
      ],
      "type": "StoryFwdHeader"
    }
  ],
  "methods": [
    {
      "id": "3667590413",
      "method": "invokeWithLayer",
      "params": [
        {"name": "layer", "type": "int"},
        {"name": "query", "type": "!X"}
      ],
      "type": "X"
    },
    {
      "id": "4261792922",
      "method": "messages.sendMessage",
      "params": [
        {"name": "flags", "type": "#"},
        {"name": "no_webpage", "type": "flags.1?true"},
        {"name": "peer", "type": "InputPeer"},
        {"name": "message", "type": "string"},
        {"name": "entities", "type": "flags.3?Vector<MessageEntity>"}
      ],
      "type": "Updates"
    }
  ]
}
""",
        encoding="utf-8",
    )

    schema = parse_schema_file(schema_path)

    assert len(schema.constructors) == 2
    assert len(schema.functions) == 2
    bool_true = next(entry for entry in schema.constructors if entry.name == "boolTrue")
    assert bool_true.constructor_id_hex == "997275b5"
    story_header = next(entry for entry in schema.constructors if entry.name == "storyFwdHeader")
    from_param = next(param for param in story_header.params if param.name == "from")
    assert from_param.python_name == "from_"
    invoke_with_layer = next(entry for entry in schema.functions if entry.name == "invokeWithLayer")
    assert any(param.name == "query" and param.type == "!X" and param.is_generic for param in invoke_with_layer.params)
    send_message = next(entry for entry in schema.functions if entry.name == "messages.sendMessage")
    assert send_message.namespace == "messages"
    assert any(param.name == "no_webpage" and param.is_true_flag for param in send_message.params)
    assert any(param.name == "entities" and param.vector_item_type == "MessageEntity" for param in send_message.params)


def test_parser_classifies_only_known_tdlib_non_id_declarations() -> None:
    schema = parse_schema_file(TDLIB_FIXTURE)

    assert len(schema.constructors) == 3
    assert len(schema.functions) == 6
    assert [(item.name, item.classification) for item in schema.ignored_declarations] == [
        ("int", "primitive"),
        ("long", "primitive"),
        ("double", "primitive"),
        ("string", "primitive"),
        ("bytes", "alias"),
        ("int256", "alias"),
        ("test.useConfigSimple", "test_combinator"),
        ("test.parseInputAppEvent", "test_combinator"),
    ]
    assert next(entry for entry in schema.functions if entry.name == "invokeWithReCaptchaPrefix")
    assert next(entry for entry in schema.functions if entry.name == "invokeWithReCaptcha")
    assert next(entry for entry in schema.constructors if entry.name == "inputPeerPhotoFileLocationLegacy")


def test_parser_rejects_unknown_non_id_declaration() -> None:
    with pytest.raises(TLSchemaParseError, match="unknown constructor-id-free TL declaration"):
        parse_schema("surprise value = Mystery;\n")


def test_parser_rejects_duplicate_constructor_ids() -> None:
    with pytest.raises(TLSchemaParseError, match="duplicate constructor id 997275b5"):
        parse_schema("boolTrue#997275b5 = Bool;\notherTrue#997275b5 = Bool;\n")


def test_parser_accepts_only_known_tdlib_prefix_constructor_id_aliases() -> None:
    schema = parse_schema(
        "---functions---\n"
        "invokeWithReCaptchaPrefix#adbb0f94 token:string = Error;\n"
        "invokeWithReCaptcha#adbb0f94 {X:Type} token:string query:!X = X;\n"
    )

    assert [entry.name for entry in schema.functions] == ["invokeWithReCaptchaPrefix", "invokeWithReCaptcha"]


def test_parser_rejects_structured_parameter_comment_for_missing_parameter() -> None:
    with pytest.raises(TLSchemaParseError, match="documents unknown parameter 'missing'"):
        parse_schema("// @param missing This field does not exist.\nboolTrue#997275b5 = Bool;\n")
