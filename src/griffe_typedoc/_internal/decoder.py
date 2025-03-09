# This module contains a data decoder to convert TypeDoc's JSON to Python objects.

from __future__ import annotations

import json
import re
from contextlib import suppress
from functools import wraps
from typing import Any, Callable

from griffe_typedoc._internal.models import (
    Accessor,
    BlockTag,
    BlockTagContent,
    BlockTagContentKind,
    BlockTagKind,
    CallSignature,
    Class,
    Comment,
    Constructor,
    ConstructorSignature,
    Enum,
    EnumMember,
    FileRegistry,
    Function,
    GetSignature,
    Group,
    IndexSignature,
    Interface,
    Method,
    Module,
    Namespace,
    Parameter,
    Project,
    Property,
    Reference,
    ReflectionKind,
    SetSignature,
    Source,
    Target,
    Type,
    TypeAlias,
    TypeKind,
    TypeLiteral,
    TypeParameter,
    Variable,
)

_re_word_end = re.compile("(.)([A-Z][a-z]+)")
_re_word_start = re.compile("([a-z0-9])([A-Z])")


def _camel_to_snake(key: str) -> str:
    return _re_word_start.sub(r"\1_\2", _re_word_end.sub(r"\1_\2", key)).lower()


def _loader(func: Callable[[dict], Any]) -> Callable[[dict[str, Any], dict[int, Any]], Any]:
    @wraps(func)
    def wrapper(obj_dict: dict[str, Any], symbol_id_map: dict[int, Any]) -> Any:
        # Transform keys from camelCase to snake_case.
        for key in list(obj_dict.keys()):
            if (_snake := _camel_to_snake(key)) != key:
                obj_dict[_snake] = obj_dict.pop(key)

        # Replace root symbol id map with our own.
        if "symbol_id_map" in obj_dict:
            obj_dict["symbol_id_map"] = symbol_id_map

        # Load object and register it in symbol map.
        obj = func(obj_dict)
        if "id" in obj_dict:
            symbol_id_map[obj.id] = obj

        # Assign object as parent on children.
        if "children" in obj_dict:
            for child in obj.children:
                with suppress(AttributeError):  # ints in groups
                    child.parent = obj

        if "signatures" in obj_dict:
            for signature in obj.signatures:
                signature.parent = obj

        if "parameters" in obj_dict:
            for parameter in obj.parameters:
                parameter.parent = obj

        if "set_signature" in obj_dict:
            obj.set_signature.parent = obj

        if "get_signature" in obj_dict:
            obj.get_signature.parent = obj

        if "sources" in obj_dict:
            for source in obj.sources:
                source.parent = obj

        return obj

    return wrapper


@_loader
def _load_project(obj_dict: dict) -> Project:
    return Project(**obj_dict)


@_loader
def _load_file_registry(obj_dict: dict) -> FileRegistry:
    return FileRegistry(**obj_dict)


@_loader
def _load_module(obj_dict: dict) -> Module:
    return Module(**obj_dict)


@_loader
def _load_namespace(obj_dict: dict) -> Namespace:
    return Namespace(**obj_dict)


@_loader
def _load_enum(obj_dict: dict) -> Enum:
    return Enum(**obj_dict)


@_loader
def _load_enum_member(obj_dict: dict) -> EnumMember:
    return EnumMember(**obj_dict)


@_loader
def _load_variable(obj_dict: dict) -> Variable:
    return Variable(**obj_dict)


@_loader
def _load_function(obj_dict: dict) -> Function:
    return Function(**obj_dict)


@_loader
def _load_class(obj_dict: dict) -> Class:
    return Class(**obj_dict)


@_loader
def _load_interface(obj_dict: dict) -> Interface:
    return Interface(**obj_dict)


@_loader
def _load_constructor(obj_dict: dict) -> Constructor:
    return Constructor(**obj_dict)


@_loader
def _load_property(obj_dict: dict) -> Property:
    return Property(**obj_dict)


@_loader
def _load_method(obj_dict: dict) -> Method:
    return Method(**obj_dict)


@_loader
def _load_call_signature(obj_dict: dict) -> CallSignature:
    return CallSignature(**obj_dict)


@_loader
def _load_index_signature(obj_dict: dict) -> IndexSignature:
    return IndexSignature(**obj_dict)


@_loader
def _load_constructor_signature(obj_dict: dict) -> ConstructorSignature:
    return ConstructorSignature(**obj_dict)


@_loader
def _load_parameter(obj_dict: dict) -> Parameter:
    return Parameter(**obj_dict)


@_loader
def _load_type_literal(obj_dict: dict) -> TypeLiteral:
    return TypeLiteral(**obj_dict)


@_loader
def _load_type_parameter(obj_dict: dict) -> TypeParameter:
    return TypeParameter(**obj_dict)


@_loader
def _load_accessor(obj_dict: dict) -> Accessor:
    return Accessor(**obj_dict)


@_loader
def _load_get_signature(obj_dict: dict) -> GetSignature:
    return GetSignature(**obj_dict)


@_loader
def _load_set_signature(obj_dict: dict) -> SetSignature:
    return SetSignature(**obj_dict)


@_loader
def _load_type_alias(obj_dict: dict) -> TypeAlias:
    return TypeAlias(**obj_dict)


@_loader
def _load_reference(obj_dict: dict) -> Reference:
    return Reference(**obj_dict)


@_loader
def _load_block_tag_alpha(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.ALPHA, content=obj_dict["content"])


@_loader
def _load_block_tag_beta(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.BETA, content=obj_dict["content"])


@_loader
def _load_block_tag_category(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.CATEGORY, content=obj_dict["content"])


@_loader
def _load_block_tag_default_value(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.DEFAULT_VALUE, content=obj_dict["content"])


@_loader
def _load_block_tag_deprecated(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.DEPRECATED, content=obj_dict["content"])


@_loader
def _load_block_tag_enum(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.ENUM, content=obj_dict["content"])


@_loader
def _load_block_tag_event(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.EVENT, content=obj_dict["content"])


@_loader
def _load_block_tag_event_property(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.EVENT_PROPERTY, content=obj_dict["content"])


@_loader
def _load_block_tag_example(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.EXAMPLE, content=obj_dict["content"])


@_loader
def _load_block_tag_experimental(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.EXPERIMENTAL, content=obj_dict["content"])


@_loader
def _load_block_tag_group(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.GROUP, content=obj_dict["content"])


@_loader
def _load_block_tag_hidden(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.HIDDEN, content=obj_dict["content"])


@_loader
def _load_block_tag_ignore(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.IGNORE, content=obj_dict["content"])


@_loader
def _load_block_tag_inherit_doc(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.INHERIT_DOC, content=obj_dict["content"])


@_loader
def _load_block_tag_interface(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.INTERFACE, content=obj_dict["content"])


@_loader
def _load_block_tag_internal(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.INTERNAL, content=obj_dict["content"])


@_loader
def _load_block_tag_label(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.LABEL, content=obj_dict["content"])


@_loader
def _load_block_tag_link(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.LINK, content=obj_dict["content"])


@_loader
def _load_block_tag_module(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.MODULE, content=obj_dict["content"])


@_loader
def _load_block_tag_namespace(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.NAMESPACE, content=obj_dict["content"])


@_loader
def _load_block_tag_overload(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.OVERLOAD, content=obj_dict["content"])


@_loader
def _load_block_tag_override(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.OVERRIDE, content=obj_dict["content"])


@_loader
def _load_block_tag_package_documentation(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.PACKAGE_DOCUMENTATION, content=obj_dict["content"])


@_loader
def _load_block_tag_param(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.PARAM, content=obj_dict["content"])


@_loader
def _load_block_tag_private(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.PRIVATE, content=obj_dict["content"])


@_loader
def _load_block_tag_private_remarks(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.PRIVATE_REMARKS, content=obj_dict["content"])


@_loader
def _load_block_tag_property(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.PROPERTY, content=obj_dict["content"])


@_loader
def _load_block_tag_protected(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.PROTECTED, content=obj_dict["content"])


@_loader
def _load_block_tag_public(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.PUBLIC, content=obj_dict["content"])


@_loader
def _load_block_tag_readonly(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.READONLY, content=obj_dict["content"])


@_loader
def _load_block_tag_remarks(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.REMARKS, content=obj_dict["content"])


@_loader
def _load_block_tag_returns(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.RETURNS, content=obj_dict["content"])


@_loader
def _load_block_tag_satisfies(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.SATISFIES, content=obj_dict["content"])


@_loader
def _load_block_tag_sealed(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.SEALED, content=obj_dict["content"])


@_loader
def _load_block_tag_see(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.SEE, content=obj_dict["content"])


@_loader
def _load_block_tag_template(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.TEMPLATE, content=obj_dict["content"])


@_loader
def _load_block_tag_throws(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.THROWS, content=obj_dict["content"])


@_loader
def _load_block_tag_type_param(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.TYPE_PARAM, content=obj_dict["content"])


@_loader
def _load_block_tag_virtual(obj_dict: dict) -> BlockTag:
    return BlockTag(kind=BlockTagKind.VIRTUAL, content=obj_dict["content"])


@_loader
def _load_block_tag_content_text(obj_dict: dict) -> BlockTagContent:
    return BlockTagContent(kind=BlockTagContentKind.TEXT, text=obj_dict["text"])


@_loader
def _load_block_tag_content_code(obj_dict: dict) -> BlockTagContent:
    return BlockTagContent(kind=BlockTagContentKind.CODE, text=obj_dict["text"])


@_loader
def _load_block_tag_content_inline_tag(obj_dict: dict) -> BlockTagContent:
    obj_dict.pop("tag")
    return BlockTagContent(kind=BlockTagContentKind.INLINE_TAG, **obj_dict)


@_loader
def _load_comment(obj_dict: dict) -> Comment:
    return Comment(**obj_dict)


@_loader
def _load_source(obj_dict: dict) -> Source:
    return Source(**obj_dict)


@_loader
def _load_type(obj_dict: dict) -> Type:
    type = obj_dict.pop("type")
    if isinstance(type, str):
        type = TypeKind(type)
    return Type(type=type, **obj_dict)


@_loader
def _load_target(obj_dict: dict) -> Target:
    return Target(**obj_dict)


@_loader
def _load_group(obj_dict: dict) -> Group:
    return Group(**obj_dict)


_loader_map: dict[
    ReflectionKind | BlockTagKind | BlockTagContentKind,
    Callable[[dict[str, Any], dict[int, Any]], Any],
] = {
    ReflectionKind.PROJECT: _load_project,
    ReflectionKind.MODULE: _load_module,
    ReflectionKind.NAMESPACE: _load_namespace,
    ReflectionKind.ENUM: _load_enum,
    ReflectionKind.ENUM_MEMBER: _load_enum_member,
    ReflectionKind.VARIABLE: _load_variable,
    ReflectionKind.FUNCTION: _load_function,
    ReflectionKind.CLASS: _load_class,
    ReflectionKind.INTERFACE: _load_interface,
    ReflectionKind.CONSTRUCTOR: _load_constructor,
    ReflectionKind.PROPERTY: _load_property,
    ReflectionKind.METHOD: _load_method,
    ReflectionKind.CALL_SIGNATURE: _load_call_signature,
    ReflectionKind.INDEX_SIGNATURE: _load_index_signature,
    ReflectionKind.CONSTRUCTOR_SIGNATURE: _load_constructor_signature,
    ReflectionKind.PARAMETER: _load_parameter,
    ReflectionKind.TYPE_LITERAL: _load_type_literal,
    ReflectionKind.TYPE_PARAMETER: _load_type_parameter,
    ReflectionKind.ACCESSOR: _load_accessor,
    ReflectionKind.GET_SIGNATURE: _load_get_signature,
    ReflectionKind.SET_SIGNATURE: _load_set_signature,
    ReflectionKind.TYPE_ALIAS: _load_type_alias,
    ReflectionKind.REFERENCE: _load_reference,
    BlockTagKind.ALPHA: _load_block_tag_alpha,
    BlockTagKind.BETA: _load_block_tag_beta,
    BlockTagKind.CATEGORY: _load_block_tag_category,
    BlockTagKind.DEFAULT_VALUE: _load_block_tag_default_value,
    BlockTagKind.DEPRECATED: _load_block_tag_deprecated,
    BlockTagKind.ENUM: _load_block_tag_enum,
    BlockTagKind.EVENT: _load_block_tag_event,
    BlockTagKind.EVENT_PROPERTY: _load_block_tag_event_property,
    BlockTagKind.EXAMPLE: _load_block_tag_example,
    BlockTagKind.EXPERIMENTAL: _load_block_tag_experimental,
    BlockTagKind.GROUP: _load_block_tag_group,
    BlockTagKind.HIDDEN: _load_block_tag_hidden,
    BlockTagKind.IGNORE: _load_block_tag_ignore,
    BlockTagKind.INTERFACE: _load_block_tag_interface,
    BlockTagKind.INTERNAL: _load_block_tag_internal,
    BlockTagKind.MODULE: _load_block_tag_module,
    BlockTagKind.NAMESPACE: _load_block_tag_namespace,
    BlockTagKind.OVERLOAD: _load_block_tag_overload,
    BlockTagKind.OVERRIDE: _load_block_tag_override,
    BlockTagKind.PACKAGE_DOCUMENTATION: _load_block_tag_package_documentation,
    BlockTagKind.PARAM: _load_block_tag_param,
    BlockTagKind.PRIVATE: _load_block_tag_private,
    BlockTagKind.PRIVATE_REMARKS: _load_block_tag_private_remarks,
    BlockTagKind.PROPERTY: _load_block_tag_property,
    BlockTagKind.PROTECTED: _load_block_tag_protected,
    BlockTagKind.PUBLIC: _load_block_tag_public,
    BlockTagKind.READONLY: _load_block_tag_readonly,
    BlockTagKind.REMARKS: _load_block_tag_remarks,
    BlockTagKind.RETURNS: _load_block_tag_returns,
    BlockTagKind.SATISFIES: _load_block_tag_satisfies,
    BlockTagKind.SEALED: _load_block_tag_sealed,
    BlockTagKind.SEE: _load_block_tag_see,
    BlockTagKind.TEMPLATE: _load_block_tag_template,
    BlockTagKind.THROWS: _load_block_tag_throws,
    BlockTagKind.TYPE_PARAM: _load_block_tag_type_param,
    BlockTagKind.VIRTUAL: _load_block_tag_virtual,
    BlockTagContentKind.TEXT: _load_block_tag_content_text,
    BlockTagContentKind.CODE: _load_block_tag_content_code,
    BlockTagContentKind.INLINE_TAG: _load_block_tag_content_inline_tag,
}


class TypedocDecoder(json.JSONDecoder):
    """JSON decoder."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the decoder.

        Parameters:
            *args: Arguments passed to parent init method.
            *kwargs: Keyword arguments passed to parent init method.
        """
        kwargs["object_hook"] = self._object_hook
        super().__init__(*args, **kwargs)
        self._symbol_map: dict[int, Any] = {}

    def _object_hook(self, obj_dict: dict[str, Any]) -> dict[str, Any] | str:
        """Decode dictionaries as data classes.

        The [`json.loads`][] method walks the tree from bottom to top.

        Parameters:
            obj_dict: The dictionary to decode.

        Returns:
            An instance of a data class.
        """
        # Load reflections or block tag contents.
        if "kind" in obj_dict:
            try:
                kind = BlockTagContentKind(obj_dict["kind"])
            except ValueError:
                kind = ReflectionKind.from_int(obj_dict["kind"])  # type: ignore[assignment]
            obj_dict.pop("kind")
            return _loader_map[kind](obj_dict, self._symbol_map)

        # Load block tags.
        if "tag" in obj_dict:
            return _loader_map[BlockTagKind(obj_dict["tag"])](obj_dict, self._symbol_map)

        # Load comments.
        if "summary" in obj_dict:
            return _load_comment(obj_dict, self._symbol_map)

        # Load sources.
        if "fileName" in obj_dict:
            return _load_source(obj_dict, self._symbol_map)

        # Load targets.
        if "sourceFileName" in obj_dict:
            return _load_target(obj_dict, self._symbol_map)

        # Load types.
        if "type" in obj_dict:
            return _load_type(obj_dict, self._symbol_map)

        # Load groups.
        if set(obj_dict.keys()) == {"title", "children"}:
            return _load_group(obj_dict, self._symbol_map)

        # Load file registry.
        if set(obj_dict.keys()) == {"entries", "reflections"}:
            return _load_file_registry(obj_dict, self._symbol_map)

        # Return dict as is.
        return obj_dict
