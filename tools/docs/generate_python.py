"""Generate split Python reference pages through static Griffe and griffe2md."""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from pathlib import Path, PurePosixPath
from posixpath import relpath

from griffe import (
    Alias,
    Attribute,
    Class,
    ExprList,
    ExprTuple,
    Function,
    GriffeLoader,
    Module,
    Object,
    Parser,
    TypeAlias,
)
from griffe2md import ConfigDict, render_object_docs

from tools.docs.model import ReferencePage

_RENDER_CONFIG: ConfigDict = {
    "allow_inspection": False,
    "filters": ["!^_"],
    "heading_level": 2,
    "inherited_members": False,
    "members": [],
    "show_root_full_path": True,
    "show_root_heading": True,
    "show_root_members_full_path": True,
    "show_signature_annotations": True,
    "signature_crossrefs": False,
}


def generate_python_pages(
    *, source_root: Path, module_names: Sequence[str], repository_url: str, dynamic_all_modules: Sequence[str] = ()
) -> tuple[ReferencePage, ...]:
    """Generate deterministic Markdown pages for reviewed public Python modules.

    Args:
        source_root: Static import-search root containing the documented packages.
        module_names: Explicit reviewed modules to render.
        repository_url: Repository base URL used for source provenance links.
        dynamic_all_modules: Explicit module paths allowed to fall back to directly source-defined public declarations
            when Griffe cannot expand ``__all__``. Schema-created members omitted by this fallback must be covered by the
            Telegram reference generator.

    Returns:
        Module, class, function, attribute, type-alias, and public method pages sorted by path.

    Raises:
        ValueError: A selected public object cannot be represented statically or lacks required documentation.

    Notes:
        Griffe inspection is disabled, so module top-level code is never executed.
    """
    loader = GriffeLoader(search_paths=[source_root], docstring_parser=Parser.google, allow_inspection=False)
    roots = {
        top_level: loader.load(top_level, submodules=True)
        for top_level in sorted({module_name.partition(".")[0] for module_name in module_names})
    }
    loader.resolve_aliases(implicit=False, external=False)
    pages: dict[str, ReferencePage] = {}
    dynamic_all_allowlist = frozenset(dynamic_all_modules)
    for module_name in sorted(set(module_names)):
        module = _resolve_module(roots[module_name.partition(".")[0]], module_name)
        _collect_module_pages(
            module,
            pages=pages,
            source_root=source_root,
            repository_url=repository_url,
            dynamic_all_modules=dynamic_all_allowlist,
        )
    return tuple(sorted(pages.values(), key=lambda page: page.path))


def _collect_module_pages(
    module: Module,
    *,
    pages: dict[str, ReferencePage],
    source_root: Path,
    repository_url: str,
    dynamic_all_modules: frozenset[str],
) -> None:
    """Collect one canonical module page and every split public member page.

    Args:
        module: Canonical module whose public surface is collected.
        pages: Canonical output-path map used for recursive deduplication.
        source_root: Static import-search root used for provenance.
        repository_url: Repository browser base URL.
        dynamic_all_modules: Canonical module paths approved for direct-declaration fallback.
    """
    module_path = _module_page_path(module)
    if module_path in pages:
        return
    members = tuple(_public_members(module, allow_dynamic_all=module.path in dynamic_all_modules))
    module_page = _module_page(module, members, source_root=source_root, repository_url=repository_url)
    pages[module_page.path] = module_page
    for _, member in members:
        if isinstance(member, Module):
            _collect_module_pages(
                member,
                pages=pages,
                source_root=source_root,
                repository_url=repository_url,
                dynamic_all_modules=dynamic_all_modules,
            )
            continue
        for page in _object_pages(member, source_root=source_root, repository_url=repository_url):
            pages.setdefault(page.path, page)


def _resolve_module(root: Object | Alias, module_name: str) -> Module:
    """Resolve a reviewed dotted module below an already loaded package root.

    Args:
        root: Statically loaded top-level package object.
        module_name: Reviewed dotted module name to resolve.

    Returns:
        Selected Griffe module.

    Raises:
        TypeError: The selected object is not a module or its root alias is unresolved.
    """
    if isinstance(root, Alias):
        if not root.resolved:
            raise TypeError(f"selected Python root alias is unresolved: {root.path}")
        root = root.final_target
    if root.path == module_name:
        if not isinstance(root, Module):
            raise TypeError(f"selected Python root is not a module: {module_name}")
        return root
    relative = module_name.split(".")[1:]
    selected = root.get_member(relative)
    if not isinstance(selected, Module):
        raise TypeError(f"selected Python object is not a module: {module_name}")
    return selected


def _public_members(parent: Module | Class, *, allow_dynamic_all: bool = False) -> Iterable[tuple[str, Object]]:
    """Yield public names and their statically representable canonical targets.

    Args:
        parent: Module or class whose direct members are filtered.
        allow_dynamic_all: Whether an unexpandable module ``__all__`` may fall back to direct declarations.

    Yields:
        Display name and resolved canonical statically representable target.

    Raises:
        ValueError: A selected public export cannot be represented statically.
    """
    dynamic_fallback = False
    if isinstance(parent, Module):
        dynamic_fallback = _validate_static_exports(parent, allow_dynamic=allow_dynamic_all)
    for name, member in sorted(parent.members.items(), key=_member_source_order):
        if name.startswith("_"):
            continue
        if isinstance(member, Module):
            if not member.is_exported:
                continue
        elif not member.is_public:
            continue
        if isinstance(member, Alias):
            if not member.resolved:
                raise ValueError(f"selected Python alias could not be resolved statically: {member.path}")
            member = member.final_target
        if isinstance(parent, Class):
            if isinstance(member, Class | Function):
                yield name, member
            continue
        if dynamic_fallback and not (
            isinstance(member, Class | Function | TypeAlias)
            or (isinstance(member, Attribute) and isinstance(member.value, str))
        ):
            continue
        if isinstance(member, Module | Class | Function | Attribute | TypeAlias):
            yield name, member
            continue
        raise ValueError(f"selected Python public object has an unsupported static kind: {member.path}")


def _validate_static_exports(module: Module, *, allow_dynamic: bool) -> bool:
    """Reject a selected module whose ``__all__`` cannot be expanded statically.

    Args:
        module: Selected or publicly exported module to validate.
        allow_dynamic: Whether a dynamic ``__all__`` may use direct source declarations only.

    Returns:
        Whether generation must use the conservative direct-declaration fallback.

    Raises:
        ValueError: ``__all__`` is dynamic or names members absent from the static model.
    """
    all_member = module.members.get("__all__")
    if all_member is None:
        return False
    exports = module.exports or []
    if not exports:
        value = getattr(all_member, "value", None)
        if isinstance(value, ExprList | ExprTuple) and not value.elements:
            return False
        if allow_dynamic:
            return True
        raise ValueError(f"selected Python module {module.path} has a dynamically computed __all__")
    export_names: list[str] = []
    for export in exports:
        if not isinstance(export, str):
            if allow_dynamic:
                return True
            raise ValueError(f"selected Python module {module.path} has a dynamically computed __all__")
        export_names.append(export)
    missing = sorted(name for name in export_names if name not in module.members)
    if missing:
        raise ValueError(
            f"selected Python module {module.path} has static exports missing from the Griffe model: {', '.join(missing)}"
        )
    return False


def _member_source_order(item: tuple[str, Object | Alias]) -> tuple[int, str]:
    """Return declaration order without resolving a possible alias target.

    Args:
        item: Member name and statically loaded Griffe member.

    Returns:
        Source line and name suitable for deterministic sorting.
    """
    name, member = item
    lineno = member.alias_lineno if isinstance(member, Alias) else member.lineno
    return lineno or 0, name


def _module_page(
    module: Module, members: Sequence[tuple[str, Object]], *, source_root: Path, repository_url: str
) -> ReferencePage:
    """Create one module index with griffe2md prose and links to split members.

    Args:
        module: Statically loaded module being rendered.
        members: Reviewed direct public objects linked from the index.
        source_root: Static import-search root used for source provenance.
        repository_url: Repository browser base URL.

    Returns:
        Generated module index page.
    """
    source_path, source_url = _source_provenance(module, source_root=source_root, repository_url=repository_url)
    links = ["## Public objects", ""]
    if members:
        for display_name, member in members:
            links.append(f"- [`{display_name}`]({_module_member_link(module, member)}) — {_summary(member)}")
    else:
        links.append("This module does not define a separate public object.")
    body = f"{_render(module)}\n\n" + "\n".join(links)
    return ReferencePage(
        path=_module_page_path(module),
        title=module.path,
        description=_summary(module),
        language="python",
        kind="module",
        qualified_name=module.path,
        source_path=source_path,
        source_url=source_url,
        body=body,
        module=module.path,
        aliases=_public_alias_paths(module),
    )


def _object_pages(obj: Object, *, source_root: Path, repository_url: str) -> list[ReferencePage]:
    """Create a public object page and recursively split public class members.

    Args:
        obj: Public Griffe object being rendered.
        source_root: Static import-search root used for provenance.
        repository_url: Repository browser base URL.

    Returns:
        The object page followed by any public class-member pages.
    """
    module = obj.module
    source_path, source_url = _source_provenance(obj, source_root=source_root, repository_url=repository_url)
    page = ReferencePage(
        path=_object_page_path(obj),
        title=obj.path,
        description=_summary(obj),
        language="python",
        kind="type" if isinstance(obj, TypeAlias) else str(obj.kind.value),
        qualified_name=obj.path,
        source_path=source_path,
        source_url=source_url,
        body=_render(obj),
        module=module.path,
        aliases=_public_alias_paths(obj),
    )
    pages = [page]
    if isinstance(obj, Class):
        for _, member in _public_members(obj):
            pages.extend(_object_pages(member, source_root=source_root, repository_url=repository_url))
    return pages


def _object_page_path(obj: Object) -> str:
    """Return the canonical split-page path for a Python object.

    Args:
        obj: Canonical object whose defining module owns the route.

    Returns:
        Markdown path below the Python reference root.
    """
    module = obj.module
    relative_parts = obj.path.split(".")[len(module.path.split(".")) :]
    object_path = "/".join(_slug(part) for part in relative_parts)
    return f"python/{module.path.replace('.', '/')}/{object_path}.md"


def _module_page_path(module: Module) -> str:
    """Return the canonical split-page path for a Python module.

    Args:
        module: Canonical module that owns the index route.

    Returns:
        Markdown index path below the Python reference root.
    """
    return f"python/{module.path.replace('.', '/')}/index.md"


def _module_member_link(module: Module, member: Object) -> str:
    """Return a relative module-index link to a canonical object page.

    Args:
        module: Selected module whose index owns the link.
        member: Canonical object targeted by the displayed public name.

    Returns:
        Directory-style relative URL to the canonical page.
    """
    module_directory = PurePosixPath(f"python/{module.path.replace('.', '/')}")
    target = (
        PurePosixPath(_module_page_path(member)).parent
        if isinstance(member, Module)
        else PurePosixPath(_object_page_path(member)).with_suffix("")
    )
    link = relpath(target.as_posix(), start=module_directory.as_posix())
    if not link.startswith("."):
        link = f"./{link}"
    return f"{link}/"


def _public_alias_paths(obj: Object) -> tuple[str, ...]:
    """Return every public alias path that resolves to a canonical object.

    Args:
        obj: Canonical object whose aliases are collected.

    Returns:
        Sorted direct and containing-class-derived public alias paths.
    """
    aliases = {
        alias.path
        for alias in obj.aliases.values()
        if alias.resolved and alias.is_public and not alias.name.startswith("_")
    }
    if isinstance(obj.parent, Class):
        aliases.update(f"{parent_alias}.{obj.name}" for parent_alias in _public_alias_paths(obj.parent))
    aliases.discard(obj.path)
    return tuple(sorted(aliases))


def _source_provenance(obj: Object, *, source_root: Path, repository_url: str) -> tuple[str, str]:
    """Return a repository-relative source path and optional line-anchored URL.

    Args:
        obj: Griffe object that owns the source location.
        source_root: Static import-search root below the repository.
        repository_url: Repository browser base URL.

    Returns:
        Repository-relative path and source browser URL.
    """
    object_filepath = obj.filepath
    if isinstance(object_filepath, list):
        if not object_filepath:
            raise ValueError(f"selected Python object has no source path: {obj.path}")
        filepath = min(object_filepath, key=lambda path: path.as_posix())
    else:
        filepath = object_filepath
    try:
        source_path = filepath.resolve().relative_to(source_root.resolve().parent).as_posix()
    except ValueError:
        source_path = filepath.name
    source_url = f"{repository_url.rstrip('/')}/blob/master/{source_path}"
    if obj.lineno:
        source_url += f"#L{obj.lineno}"
    return source_path, source_url


def _summary(obj: Object) -> str:
    """Return the first descriptive docstring line for frontmatter and indexes.

    Args:
        obj: Griffe object whose docstring supplies the summary.

    Returns:
        First non-empty docstring line.

    Raises:
        ValueError: The selected object lacks descriptive documentation.
    """
    if obj.docstring is None or not obj.docstring.value.strip():
        if isinstance(obj, Attribute | TypeAlias):
            return f"Public {obj.kind.value} `{obj.path}`."
        raise ValueError(f"selected Python object lacks a docstring: {obj.path}")
    return next(line.strip() for line in obj.docstring.value.splitlines() if line.strip())


def _render(obj: Object) -> str:
    """Render one object through the pinned griffe2md implementation.

    Args:
        obj: Griffe object to render without runtime inspection.

    Returns:
        Generated Markdown without surrounding frontmatter.

    Raises:
        ValueError: A type alias has no static source representation.
    """
    if isinstance(obj, TypeAlias):
        source = obj.source.strip()
        if not source:
            raise ValueError(f"selected Python type alias lacks static source: {obj.path}")
        return f"## `{obj.path}`\n\n```python\n{source}\n```"
    return render_object_docs(obj, config=_RENDER_CONFIG, format_md=False).strip()


def _slug(value: str) -> str:
    """Convert a Python symbol segment to a stable collision-readable route slug.

    Args:
        value: Source identifier segment.

    Returns:
        Lowercase route-safe slug, or ``symbol`` when no characters remain.
    """
    slug = re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")
    return slug or "symbol"


__all__ = ["generate_python_pages"]
