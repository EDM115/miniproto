from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from tools.schema import rust_fast
from tools.schema.parser import (
    TLParameter,
    TLSchema,
    TLSchemaParseError,
    parse_schema,
    parse_schema_file,
    parse_schema_json,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "schema" / "layer223-slice.tl"
TDLIB_FIXTURE = ROOT / "tests" / "fixtures" / "schema" / "tdlib-layer228-slice.tl"


def test_parser_handles_real_flags_vectors_generics_and_reserved_names() -> None:
    schema = parse_schema_file(FIXTURE)
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


def _named_schema_data(name: str, *, method: bool = False) -> dict[str, object]:
    return {
        "methods" if method else "constructors": [
            {"id": "1", "method" if method else "predicate": name, "params": [], "type": "Object"}
        ]
    }


@pytest.mark.parametrize("method", [False, True])
@pytest.mark.parametrize(
    "name",
    [
        "Payload[T:Any(0)]",
        "Payload[0:Any(0)]",
        "Payload()",
        "Payload'",
        'Payload"',
        "scope;print(0);alias.item",
        "scope\nprint(0)\nalias.item",
        "scope\ralias.item",
        "scope.item\x00",
        "scope.item # comment",
    ],
)
def test_json_rejects_expression_and_statement_names(name: str, method: bool) -> None:
    with pytest.raises(TLSchemaParseError, match="invalid declaration name"):
        parse_schema_json(_named_schema_data(name, method=method))


@pytest.mark.parametrize(
    "name",
    [".item", "item.", "outer..item", "1item", "outer.2item", "outer._1", "class.item", "True.item", "caf\u00e9"],
)
@pytest.mark.parametrize("method", [False, True])
def test_text_and_json_reject_unusable_qualified_identifiers(name: str, method: bool) -> None:
    with pytest.raises(TLSchemaParseError):
        parse_schema_json(_named_schema_data(name, method=method))
    with pytest.raises(TLSchemaParseError):
        parse_schema(("---functions---\n" if method else "") + f"{name}#00000001 = Object;\n")


@pytest.mark.parametrize(
    "names", [("outer.inner.item", "outer_inner.other"), ("Box.item", "box"), ("outer.true", "outer.trueValue")]
)
@pytest.mark.parametrize("method", [False, True])
def test_parser_rejects_namespace_and_short_alias_collisions(names: tuple[str, str], method: bool) -> None:
    entries = [
        {"id": str(index), "method" if method else "predicate": name, "params": [], "type": "Object"}
        for index, name in enumerate(names, start=1)
    ]
    with pytest.raises(TLSchemaParseError, match=r"generated (namespace|alias)"):
        parse_schema_json({"methods" if method else "constructors": entries})
    with pytest.raises(TLSchemaParseError, match=r"generated (namespace|alias)"):
        parse_schema(
            ("---functions---\n" if method else "")
            + "\n".join(f"{name}#{index:08x} = Object;" for index, name in enumerate(names, start=1))
        )


@pytest.mark.parametrize(
    "filename", ["schema.json", "schema.tl", "schema-core.json", "schema-core.tl", "schema-tdesktop.tl"]
)
def test_pinned_schemas_remain_accepted(filename: str) -> None:
    schema = parse_schema_file(ROOT / "tools/schema" / filename)
    assert schema.constructors
    assert schema.functions


def _flag_schema_data(params: list[tuple[str, str]], *, method: bool = False) -> dict[str, object]:
    return {
        "methods" if method else "constructors": [
            {
                "id": str(0x10203040),
                "method" if method else "predicate": "sample",
                "params": [{"name": name, "type": type_name} for name, type_name in params],
                "type": "Sample",
            }
        ]
    }


def _parse_flag_schema(params: list[tuple[str, str]], *, json_input: bool, method: bool = False) -> TLSchema:
    if json_input:
        return parse_schema_json(_flag_schema_data(params, method=method))
    declaration = "sample#10203040 " + " ".join(f"{name}:{type_name}" for name, type_name in params) + " = Sample;\n"
    return parse_schema(("---functions---\n" if method else "") + declaration)


@pytest.mark.parametrize("json_input", [False, True])
@pytest.mark.parametrize("method", [False, True])
@pytest.mark.parametrize(
    "index",
    [
        pytest.param("32", id="first-invalid"),
        pytest.param("00032", id="leading-zero-invalid"),
        pytest.param("1000000000", id="short-large-index"),
        pytest.param("9" * 5000, id="beyond-int-conversion-limit"),
    ],
)
@pytest.mark.parametrize("inner", ["true", "int"])
def test_parsers_reject_out_of_word_indexes(json_input: bool, method: bool, index: str, inner: str) -> None:
    with pytest.raises(TLSchemaParseError, match=r"flag index.*0 through 31"):
        _parse_flag_schema([("flags", "#"), ("value", f"flags.{index}?{inner}")], json_input=json_input, method=method)


@pytest.mark.parametrize("json_input", [False, True])
@pytest.mark.parametrize(
    "type_name",
    [
        "flags.-1?int",
        "flags.+1?int",
        "flags.0x1?int",
        "flags.1_0?int",
        "flags.\u0663\u0661?int",
        "flags.?int",
        "flags.1?flags.2?int",
    ],
)
def test_malformed_optional_types_cannot_become_unconditional_fields(json_input: bool, type_name: str) -> None:
    with pytest.raises(TLSchemaParseError, match="malformed optional field"):
        _parse_flag_schema([("flags", "#"), ("value", type_name)], json_input=json_input)


@pytest.mark.parametrize("json_input", [False, True])
@pytest.mark.parametrize(
    "params",
    [
        [("value", "missing.0?int")],
        [("value", "flags.0?true"), ("flags", "#")],
        [("flags", "int"), ("value", "flags.0?int")],
        [("flags", "#"), ("flags", "#"), ("value", "flags.0?true")],
    ],
)
def test_optional_fields_require_one_preceding_flags_marker(json_input: bool, params: list[tuple[str, str]]) -> None:
    with pytest.raises(TLSchemaParseError, match="flags marker"):
        _parse_flag_schema(params, json_input=json_input)


@pytest.mark.parametrize("json_input", [False, True])
@pytest.mark.parametrize("token,index", [("0", 0), ("30", 30), ("31", 31), ("00031", 31), ("0" * 5000 + "31", 31)])
def test_valid_indexes_and_leading_zeroes_remain_supported(json_input: bool, token: str, index: int) -> None:
    schema = _parse_flag_schema([("flags", "#"), ("value", f"flags.{token}?true")], json_input=json_input)
    field = schema.entries[0].params[1]
    assert field.flag_index == index
    assert field.flag == "flags"
    assert field.is_optional and field.is_true_flag


@pytest.mark.parametrize("index", [-1, 32, 1000000000, True, 1.0, None])
def test_programmatic_parameter_and_native_models_reject_invalid_indexes(index: Any) -> None:
    with pytest.raises(TLSchemaParseError, match=r"flag index.*0 through 31"):
        TLParameter("value", "value", "true", flag="flags", flag_index=index, is_optional=True, is_true_flag=True)
    with pytest.raises(TLSchemaParseError, match=r"flag index.*0 through 31"):
        rust_fast.FastField("value", "value", "true", "true", 0, flag_group=0, flag_index=index)


@pytest.mark.parametrize(
    "filename", ["schema.json", "schema.tl", "schema-core.json", "schema-core.tl", "schema-tdesktop.tl"]
)
def test_pinned_schema_flags_remain_accepted(filename: str) -> None:
    schema = parse_schema_file(ROOT / "tools/schema" / filename)
    assert schema.constructors
    assert schema.functions
