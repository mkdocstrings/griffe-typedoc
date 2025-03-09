from __future__ import annotations

import enum
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Any

# from pydantic.dataclasses import dataclass, Field as field

# TODO: Use info from https://typedoc.org/api/modules/JSONOutput.html to rebuild models!
# We could also use https://github.com/koxudaxi/datamodel-code-generator to generate the models, after generating a JSON Schema with
# `npx ts-json-schema-generator --path src/**/*.ts --type ProjectReflection --no-type-check`.
# Initially discussed in https://github.com/TypeStrong/typedoc/issues/2705.
# See issue generating schema: https://github.com/vega/ts-json-schema-generator/issues/2197.

# TODO: I have aggressively added type-ignore comments to this file,
# they should all be removed and fixed (unless we rewrite the whole thing as per previous comment).


# https://github.com/TypeStrong/typedoc/blob/master/src/lib/models/reflections/kind.ts
class ReflectionKind(enum.Enum):
    PROJECT = "project"
    MODULE = "module"
    NAMESPACE = "namespace"
    ENUM = "enum"
    ENUM_MEMBER = "enum_member"
    VARIABLE = "variable"
    FUNCTION = "function"
    CLASS = "class"
    INTERFACE = "interface"
    CONSTRUCTOR = "constructor"
    PROPERTY = "property"
    METHOD = "method"
    CALL_SIGNATURE = "call_signature"
    INDEX_SIGNATURE = "index_signature"
    CONSTRUCTOR_SIGNATURE = "constructor_signature"
    PARAMETER = "parameter"
    TYPE_LITERAL = "type_literal"
    TYPE_PARAMETER = "type_parameter"
    ACCESSOR = "accessor"
    GET_SIGNATURE = "get_signature"
    SET_SIGNATURE = "set_signature"
    TYPE_ALIAS = "type_alias"
    REFERENCE = "reference"

    @classmethod
    def from_int(cls, value: int) -> ReflectionKind:
        return {
            0x1: cls.PROJECT,
            0x2: cls.MODULE,
            0x4: cls.NAMESPACE,
            0x8: cls.ENUM,
            0x10: cls.ENUM_MEMBER,
            0x20: cls.VARIABLE,
            0x40: cls.FUNCTION,
            0x80: cls.CLASS,
            0x100: cls.INTERFACE,
            0x200: cls.CONSTRUCTOR,
            0x400: cls.PROPERTY,
            0x800: cls.METHOD,
            0x1000: cls.CALL_SIGNATURE,
            0x2000: cls.INDEX_SIGNATURE,
            0x4000: cls.CONSTRUCTOR_SIGNATURE,
            0x8000: cls.PARAMETER,
            0x10000: cls.TYPE_LITERAL,
            0x20000: cls.TYPE_PARAMETER,
            0x40000: cls.ACCESSOR,
            0x80000: cls.GET_SIGNATURE,
            0x100000: cls.SET_SIGNATURE,
            0x200000: cls.TYPE_ALIAS,
            0x400000: cls.REFERENCE,
        }[value]

    def to_int(self) -> int:
        return {
            self.PROJECT: 0x1,
            self.MODULE: 0x2,
            self.NAMESPACE: 0x4,
            self.ENUM: 0x8,
            self.ENUM_MEMBER: 0x10,
            self.VARIABLE: 0x20,
            self.FUNCTION: 0x40,
            self.CLASS: 0x80,
            self.INTERFACE: 0x100,
            self.CONSTRUCTOR: 0x200,
            self.PROPERTY: 0x400,
            self.METHOD: 0x800,
            self.CALL_SIGNATURE: 0x1000,
            self.INDEX_SIGNATURE: 0x2000,
            self.CONSTRUCTOR_SIGNATURE: 0x4000,
            self.PARAMETER: 0x8000,
            self.TYPE_LITERAL: 0x10000,
            self.TYPE_PARAMETER: 0x20000,
            self.ACCESSOR: 0x40000,
            self.GET_SIGNATURE: 0x80000,
            self.SET_SIGNATURE: 0x100000,
            self.TYPE_ALIAS: 0x200000,
            self.REFERENCE: 0x400000,
        }[self]  # type: ignore[index]


# https://typedoc.org/guides/tags/
class BlockTagKind(enum.Enum):
    ALPHA = "@alpha"
    BETA = "@beta"
    CATEGORY = "@category"
    DEFAULT_VALUE = "@defaultValue"
    DEPRECATED = "@deprecated"
    ENUM = "@enum"
    EVENT = "@event"
    EVENT_PROPERTY = "@eventProperty"
    EXAMPLE = "@example"
    EXPERIMENTAL = "@experimental"
    GROUP = "@group"
    HIDDEN = "@hidden"
    IGNORE = "@ignore"
    INHERIT_DOC = "@inheritDoc"
    INTERFACE = "@interface"
    INTERNAL = "@internal"
    LABEL = "@label"
    LINK = "@link"
    MODULE = "@module"
    NAMESPACE = "@namespace"
    OVERLOAD = "@overload"
    OVERRIDE = "@override"
    PACKAGE_DOCUMENTATION = "@packageDocumentation"
    PARAM = "@param"
    PRIVATE = "@private"
    PRIVATE_REMARKS = "@privateRemarks"
    PROPERTY = "@property"
    PROTECTED = "@protected"
    PUBLIC = "@public"
    READONLY = "@readonly"
    REMARKS = "@remarks"
    RETURNS = "@returns"
    SATISFIES = "@satisfies"
    SEALED = "@sealed"
    SEE = "@see"
    TEMPLATE = "@template"
    THROWS = "@throws"
    TYPE_PARAM = "@typeParam"
    VIRTUAL = "@virtual"


class BlockTagContentKind(enum.Enum):
    TEXT = "text"
    CODE = "code"
    INLINE_TAG = "inline-tag"


@dataclass(kw_only=True)
class FileRegistry:
    entries: dict[int, str]
    reflections: dict[int, int]

    @cached_property
    def reverse_reflections(self) -> dict[int, int]:
        return {value: key for key, value in self.reflections.items()}

    def filepath(self, reflection_id: int) -> str:
        return self.entries[self.reverse_reflections[reflection_id]]


@dataclass(kw_only=True)
class BlockTagContent:
    kind: BlockTagContentKind
    text: str
    target: int | str | None = None
    ts_link_text: str | None = None

    def __str__(self) -> str:
        return self.markdown()

    def markdown(self, symbol_map: dict[int, Reflection] | None = None) -> str:
        if self.target:
            if isinstance(self.target, int) and symbol_map:
                return f'<autoref identifier="{symbol_map[self.target].path}">{self.text}</autoref>'
            return f"[{self.text}]({self.target})"
        return self.text


@dataclass(kw_only=True)
class BlockTag:
    kind: BlockTagKind
    content: list[BlockTagContent]

    def __str__(self) -> str:
        return "".join(str(block) for block in self.content)

    def markdown(self, **kwargs: Any) -> str:
        return "".join(block.markdown(**kwargs) for block in self.summary)  # type: ignore[attr-defined]


@dataclass(kw_only=True)
class Comment:
    summary: list[BlockTagContent]
    tags: list[BlockTag] | None = None
    block_tags: list[BlockTag] | None = None

    def __str__(self) -> str:
        return "".join(str(block) for block in self.summary)

    def markdown(self, **kwargs: Any) -> str:
        return "".join(block.markdown(**kwargs) for block in self.summary)


@dataclass(kw_only=True)
class Group:
    title: str
    children: list[int | Reflection]


@dataclass(kw_only=True)
class Source:
    file_name: str
    line: int
    character: int
    url: str | None = None

    @property
    def filepath(self) -> str:
        root = self.parent.root  # type: ignore[attr-defined]
        try:
            return root.files.filepath(self.parent.root_module.id)  # type: ignore[attr-defined]
        except IndexError:
            return root.files.filepath(root.id)

    @property
    def contents(self) -> str:
        try:
            with Path(self.filepath).open() as file:
                return file.readlines()[self.line - 1]
        except (OSError, IndexError):
            with Path(self.filepath).with_name(self.file_name).open() as file:
                return file.readlines()[self.line - 1]


@dataclass(kw_only=True)
class Target:
    source_file_name: str
    qualified_name: str


class TypeKind(enum.Enum):
    ARRAY = "array"
    INTRINSIC = "intrinsic"
    LITERAL = "literal"
    REFERENCE = "reference"
    REFLECTION = "reflection"
    UNION = "union"
    TUPLE = "tuple"
    QUERY = "query"
    OPERATOR = "typeOperator"
    INTERSECTION = "intersection"
    MAPPED = "mapped"


@dataclass(kw_only=True)
class Type:
    type: TypeKind
    name: str | None = None
    target: int | Target | None = None
    package: str | None = None
    type_arguments: list[Type] | None = None
    qualified_name: str | None = None
    element_type: Type | None = None  # array
    refers_to_type_parameter: bool | None = None
    value: str | None = None  # literal
    types: list[Type] | None = None  # union
    declaration: TypeLiteral | None = None  # reflection
    elements: list[Type] | None = None
    prefer_values: bool | None = None
    query_type: Type | None = None
    operator: str | None = None
    parameter: str | None = None
    parameter_type: Type | None = None
    template_type: Type | None = None


@dataclass(kw_only=True)
class Reflection:
    id: int
    name: str
    variant: str
    comment: Comment | None = None
    children: list[Reflection] = field(default_factory=list)
    flags: dict = field(default_factory=dict)
    groups: list[Group] = field(default_factory=list)
    sources: list[Source] = field(default_factory=list)
    parent: Reflection | None = None
    type: Type | None = None

    @property
    def kind(self) -> ReflectionKind:
        raise NotImplementedError

    @property
    def root_module(self) -> Reflection:
        parent = self
        while parent.parent and parent.parent.kind is not ReflectionKind.PROJECT:
            parent = parent.parent
        return parent

    @property
    def root(self) -> Reflection:
        parent = self
        while parent.parent:
            parent = parent.parent
        return parent

    @property
    def path(self) -> str:
        if self.parent is None or isinstance(self.parent, Project):
            return self.name
        if self.kind is ReflectionKind.MODULE and self.name == "index":
            return self.parent.path
        return f"{self.parent.path}/{self.name}"

    @property
    def symbol_map(self) -> dict[int, Reflection]:
        try:
            return self.parent.symbol_map  # type: ignore[union-attr]
        except AttributeError:
            return {}

    @property
    def resolved_target(self) -> Reflection:
        return self.symbol_map[self.target]  # type: ignore[attr-defined]

    @property
    def final_target(self) -> Reflection:
        target = self.resolved_target
        if not hasattr(target, "target"):
            return target
        return target.final_target

    @property
    def resolved_groups(self) -> list[Group]:
        return [
            Group(
                title=group.title,
                children=[self.symbol_map[child] if isinstance(child, int) else child for child in group.children],
            )
            for group in self.groups
        ]

    # TODO: Optimize: get source once (cache it), use line numbers of all sources to get relevant lines.
    @property
    def source_contents(self) -> str:
        return "\n".join(source.contents for source in self.sources).rstrip().removesuffix("{")


@dataclass(kw_only=True)
class Project(Reflection):
    package_name: str  # type: ignore[misc]
    readme: list[BlockTagContent] | None = None
    symbol_id_map: dict[int, Reflection] = field(default_factory=dict, repr=False)
    package_version: str | None = None
    files: FileRegistry | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.PROJECT

    @property
    def symbol_map(self) -> dict[int, Reflection]:
        return self.symbol_id_map


@dataclass(kw_only=True)
class Module(Reflection):
    package_version: str | None = None
    readme: str | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.MODULE

    @property
    def exports(self) -> list[Reflection]:
        for child in self.children:
            if child.kind is ReflectionKind.FUNCTION and child.name == "export=":
                return child.exports  # type: ignore[attr-defined]
        return []


@dataclass(kw_only=True)
class Namespace(Reflection):
    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.NAMESPACE


@dataclass(kw_only=True)
class Enum(Reflection):
    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.ENUM


@dataclass(kw_only=True)
class EnumMember(Reflection):
    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.ENUM_MEMBER


@dataclass(kw_only=True)
class Variable(Reflection):
    type: Type  # type: ignore[misc]
    default_value: str | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.VARIABLE


@dataclass(kw_only=True)
class Function(Reflection):
    signatures: list[CallSignature]  # type: ignore[misc]

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.FUNCTION

    @property
    def exports(self) -> list[Reflection]:
        return [
            Reference(
                id=prop.id,
                variant="reference",
                name=prop.name,
                target=prop.type.target,  # type: ignore[arg-type,union-attr]
                parent=self.parent,
            )
            for prop in self.signatures[0].type.declaration.children  # type: ignore[union-attr]
        ]


@dataclass(kw_only=True)
class Class(Reflection):
    extended_types: list[Type] | None = None
    extended_by: list[Type] | None = None
    implemented_types: list[Type] | None = None
    index_signatures: list[IndexSignature] | None = None
    type_parameters: list[TypeParameter] | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.CLASS


@dataclass(kw_only=True)
class Interface(Reflection):
    extended_types: list[Type] | None = None
    extended_by: list[Type] | None = None
    type_parameters: list[TypeParameter] | None = None
    index_signature: IndexSignature | None = None
    implemented_by: list[Type] | None = None
    index_signatures: list[IndexSignature] | None = None
    signatures: list[CallSignature] | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.INTERFACE


@dataclass(kw_only=True)
class Constructor(Reflection):
    signatures: list[ConstructorSignature] | None = None
    overwrites: Type | None = None
    inherited_from: Type | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.CONSTRUCTOR


@dataclass(kw_only=True)
class Property(Reflection):
    type: Type  # type: ignore[misc]
    inherited_from: Type | None = None
    overwrites: Type | None = None
    default_value: str | None = None
    implementation_of: Type | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.PROPERTY


@dataclass(kw_only=True)
class Method(Reflection):
    signatures: list[CallSignature]  # type: ignore[misc]
    overwrites: Type | None = None
    implementation_of: Type | None = None
    inherited_from: Type | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.METHOD


@dataclass(kw_only=True)
class CallSignature(Reflection):
    type: Type  # type: ignore[misc]
    parameters: list[Parameter] | None = None
    type_parameters: list[TypeParameter] | None = None
    overwrites: Type | None = None
    implementation_of: Type | None = None
    inherited_from: Type | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.CALL_SIGNATURE


@dataclass(kw_only=True)
class IndexSignature(Reflection):
    type: Type  # type: ignore[misc]
    parameters: list[Parameter] | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.INDEX_SIGNATURE


@dataclass(kw_only=True)
class ConstructorSignature(Reflection):
    parameters: list[Parameter] | None = None
    overwrites: Type | None = None
    inherited_from: Type | None = None
    type_parameters: list[TypeParameter] | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.CONSTRUCTOR_SIGNATURE


@dataclass(kw_only=True)
class Parameter(Reflection):
    type: Type | None = None
    default_value: str | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.PARAMETER


@dataclass(kw_only=True)
class TypeLiteral(Reflection):
    signatures: list[CallSignature] | None = None
    index_signatures: list[IndexSignature] | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.TYPE_LITERAL


@dataclass(kw_only=True)
class TypeParameter(Reflection):
    type: Type | None = None
    default: Type | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.TYPE_PARAMETER


@dataclass(kw_only=True)
class Accessor(Reflection):
    get_signature: GetSignature | None = None
    set_signature: SetSignature | None = None
    overwrites: Type | None = None
    implementation_of: Type | None = None
    inherited_from: Type | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.ACCESSOR


@dataclass(kw_only=True)
class GetSignature(Reflection):
    overwrites: Type | None = None
    implementation_of: Type | None = None
    inherited_from: Type | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.GET_SIGNATURE


@dataclass(kw_only=True)
class SetSignature(Reflection):
    parameters: list[Parameter] | None = None
    overwrites: Type | None = None
    implementation_of: Type | None = None
    inherited_from: Type | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.SET_SIGNATURE


@dataclass(kw_only=True)
class TypeAlias(Reflection):
    type: Type  # type: ignore[misc]
    type_parameters: list[TypeParameter] | None = None
    implemented_by: list[Type] | None = None

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.TYPE_ALIAS


@dataclass(kw_only=True)
class Reference(Reflection):
    target: int  # type: ignore[misc]

    @property
    def kind(self) -> ReflectionKind:
        return ReflectionKind.REFERENCE
