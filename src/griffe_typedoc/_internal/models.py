# SPDX-License-Identifier: ISC
#
# ISC License
#
# Copyright (c) 2024, Timothée Mazzucotelli and contributors
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Any

# from pydantic.dataclasses import dataclass, Field as field

# TODO: Use info from https://typedoc.org/api/modules/JSONOutput.html to rebuild models!
# We could also use https://github.com/koxudaxi/datamodel-code-generator to generate the models,
# after generating a JSON Schema with ts-json-schema-generator:
#
# ```
# git clone https://github.com/TypeStrong/typedoc
# cd typedoc
# npx ts-json-schema-generator -f tsconfig.json --path src/**.ts --type ProjectReflection --no-type-check
# uvx --from datamodel-code-generator datamodel-codegen \
#   --input typedoc-schema.json --input-file-type jsonschema \
#   --output-model-type dataclasses.dataclass --output models/
# ```
#
# Initially discussed in https://github.com/TypeStrong/typedoc/issues/2705.
# See issue generating schema: https://github.com/vega/ts-json-schema-generator/issues/2197.

# TODO: I have aggressively added type-ignore comments to this file,
# they should all be removed and fixed (unless we rewrite the whole thing as per previous comment).


# https://github.com/TypeStrong/typedoc/blob/master/src/lib/models/reflections/kind.ts
class ReflectionKind(enum.Enum):
    """Kinds of TypeDoc reflections."""

    PROJECT = "project"
    """The project reflection kind."""
    MODULE = "module"
    """The module reflection kind."""
    NAMESPACE = "namespace"
    """The namespace reflection kind."""
    ENUM = "enum"
    """The enum reflection kind."""
    ENUM_MEMBER = "enum_member"
    """The enum member reflection kind."""
    VARIABLE = "variable"
    """The variable reflection kind."""
    FUNCTION = "function"
    """The function reflection kind."""
    CLASS = "class"
    """The class reflection kind."""
    INTERFACE = "interface"
    """The interface reflection kind."""
    CONSTRUCTOR = "constructor"
    """The constructor reflection kind."""
    PROPERTY = "property"
    """The property reflection kind."""
    METHOD = "method"
    """The method reflection kind."""
    CALL_SIGNATURE = "call_signature"
    """The call signature reflection kind."""
    INDEX_SIGNATURE = "index_signature"
    """The index signature reflection kind."""
    CONSTRUCTOR_SIGNATURE = "constructor_signature"
    """The constructor signature reflection kind."""
    PARAMETER = "parameter"
    """The parameter reflection kind."""
    TYPE_LITERAL = "type_literal"
    """The type literal reflection kind."""
    TYPE_PARAMETER = "type_parameter"
    """The type parameter reflection kind."""
    ACCESSOR = "accessor"
    """The accessor reflection kind."""
    GET_SIGNATURE = "get_signature"
    """The get signature reflection kind."""
    SET_SIGNATURE = "set_signature"
    """The set signature reflection kind."""
    TYPE_ALIAS = "type_alias"
    """The type alias reflection kind."""
    REFERENCE = "reference"
    """The reference reflection kind."""

    @classmethod
    def from_int(cls, value: int) -> ReflectionKind:
        """Convert a TypeDoc reflection kind integer to an enum member.

        Parameters:
            value: Integer identifying one reflection kind.

        Returns:
            The matching reflection kind.

        Raises:
            KeyError: If the integer does not identify a supported kind.
        """
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
        """Return the TypeDoc integer identifying this reflection kind."""
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
    """Tags supported in TypeDoc comments."""

    ALPHA = "@alpha"
    """The `@alpha` comment tag."""
    BETA = "@beta"
    """The `@beta` comment tag."""
    CATEGORY = "@category"
    """The `@category` comment tag."""
    DEFAULT_VALUE = "@defaultValue"
    """The `@defaultValue` comment tag."""
    DEPRECATED = "@deprecated"
    """The `@deprecated` comment tag."""
    ENUM = "@enum"
    """The `@enum` comment tag."""
    EVENT = "@event"
    """The `@event` comment tag."""
    EVENT_PROPERTY = "@eventProperty"
    """The `@eventProperty` comment tag."""
    EXAMPLE = "@example"
    """The `@example` comment tag."""
    EXPERIMENTAL = "@experimental"
    """The `@experimental` comment tag."""
    GROUP = "@group"
    """The `@group` comment tag."""
    HIDDEN = "@hidden"
    """The `@hidden` comment tag."""
    IGNORE = "@ignore"
    """The `@ignore` comment tag."""
    INHERIT_DOC = "@inheritDoc"
    """The `@inheritDoc` comment tag."""
    INTERFACE = "@interface"
    """The `@interface` comment tag."""
    INTERNAL = "@internal"
    """The `@internal` comment tag."""
    LABEL = "@label"
    """The `@label` comment tag."""
    LINK = "@link"
    """The `@link` comment tag."""
    MODULE = "@module"
    """The `@module` comment tag."""
    NAMESPACE = "@namespace"
    """The `@namespace` comment tag."""
    OVERLOAD = "@overload"
    """The `@overload` comment tag."""
    OVERRIDE = "@override"
    """The `@override` comment tag."""
    PACKAGE_DOCUMENTATION = "@packageDocumentation"
    """The `@packageDocumentation` comment tag."""
    PARAM = "@param"
    """The `@param` comment tag."""
    PRIVATE = "@private"
    """The `@private` comment tag."""
    PRIVATE_REMARKS = "@privateRemarks"
    """The `@privateRemarks` comment tag."""
    PROPERTY = "@property"
    """The `@property` comment tag."""
    PROTECTED = "@protected"
    """The `@protected` comment tag."""
    PUBLIC = "@public"
    """The `@public` comment tag."""
    READONLY = "@readonly"
    """The `@readonly` comment tag."""
    REMARKS = "@remarks"
    """The `@remarks` comment tag."""
    RETURNS = "@returns"
    """The `@returns` comment tag."""
    SATISFIES = "@satisfies"
    """The `@satisfies` comment tag."""
    SEALED = "@sealed"
    """The `@sealed` comment tag."""
    SEE = "@see"
    """The `@see` comment tag."""
    TEMPLATE = "@template"
    """The `@template` comment tag."""
    THROWS = "@throws"
    """The `@throws` comment tag."""
    TYPE_PARAM = "@typeParam"
    """The `@typeParam` comment tag."""
    VIRTUAL = "@virtual"
    """The `@virtual` comment tag."""


class BlockTagContentKind(enum.Enum):
    """Kinds of content in a TypeDoc comment."""

    TEXT = "text"
    """Plain text content."""
    CODE = "code"
    """Code content."""
    INLINE_TAG = "inline-tag"
    """An inline comment tag."""


@dataclass(kw_only=True)
class FileRegistry:
    """Source files and their associated reflections."""

    entries: dict[int, str]
    """File paths indexed by file ID."""
    reflections: dict[int, int]
    """Reflection IDs indexed by file ID."""

    @cached_property
    def reverse_reflections(self) -> dict[int, int]:
        """File IDs indexed by reflection ID."""
        return {value: key for key, value in self.reflections.items()}

    def filepath(self, reflection_id: int) -> str:
        """Return the file path associated with a reflection ID.

        Parameters:
            reflection_id: ID of the reflection whose file path is requested.

        Returns:
            The registered file path.

        Raises:
            KeyError: If the reflection or file ID is not registered.
        """
        return self.entries[self.reverse_reflections[reflection_id]]


@dataclass(kw_only=True)
class BlockTagContent:
    """A text, code, or inline tag segment in a comment."""

    kind: BlockTagContentKind
    """Kind of comment content."""
    text: str
    """Text of the content segment."""
    target: int | str | None = None
    """Reflection ID or URL targeted by an inline link."""
    ts_link_text: str | None = None
    """Link text supplied in the TypeScript comment."""

    def __str__(self) -> str:
        return self.markdown()

    def markdown(self, symbol_map: dict[int, Reflection] | None = None) -> str:
        """Render the content segment as Markdown.

        Parameters:
            symbol_map: Reflections indexed by ID, used to resolve internal links.

        Returns:
            Text, a Markdown link, or an autoref element for a resolved internal link.
        """
        if self.target:
            if isinstance(self.target, int) and symbol_map:
                return f'<autoref identifier="{symbol_map[self.target].path}">{self.text}</autoref>'
            return f"[{self.text}]({self.target})"
        return self.text


@dataclass(kw_only=True)
class BlockTag:
    """A comment tag and its content."""

    kind: BlockTagKind
    """Kind of comment tag."""
    content: list[BlockTagContent]
    """Content segments of the tag."""

    def __str__(self) -> str:
        return "".join(str(block) for block in self.content)

    def markdown(self, **kwargs: Any) -> str:
        """Render tag content as Markdown.

        Parameters:
            **kwargs: Keyword arguments passed to each content segment's `markdown` method.

        Returns:
            The rendered content segments joined together.
        """
        return "".join(block.markdown(**kwargs) for block in self.summary)  # ty:ignore[unresolved-attribute]


@dataclass(kw_only=True)
class Comment:
    """A TypeDoc comment with a summary and optional tags."""

    summary: list[BlockTagContent]
    """Content segments of the comment summary."""
    tags: list[BlockTag] | None = None
    """Tags associated with the comment."""
    block_tags: list[BlockTag] | None = None
    """Block tags associated with the comment."""

    def __str__(self) -> str:
        return "".join(str(block) for block in self.summary)

    def markdown(self, **kwargs: Any) -> str:
        """Render the comment summary as Markdown.

        Parameters:
            **kwargs: Keyword arguments passed to each content segment's `markdown` method.

        Returns:
            The rendered summary segments joined together.
        """
        return "".join(block.markdown(**kwargs) for block in self.summary)


@dataclass(kw_only=True)
class Group:
    """A named group of reflections."""

    title: str
    """Title of the group."""
    children: list[int | Reflection]
    """IDs or reflections belonging to the group."""


@dataclass(kw_only=True)
class Source:
    """The source location of a reflection."""

    file_name: str
    """Name of the source file."""
    line: int
    """Source line number, starting at one."""
    character: int
    """Character offset within the source line."""
    url: str | None = None
    """URL of the source location."""

    @property
    def filepath(self) -> str:
        """Path of the source file resolved through the project file registry."""
        root = self.parent.root  # ty:ignore[unresolved-attribute]
        try:
            return root.files.filepath(self.parent.root_module.id)  # ty:ignore[unresolved-attribute]
        except IndexError:
            return root.files.filepath(root.id)

    @property
    def contents(self) -> str:
        """Source text at the recorded line number, including its line ending."""
        try:
            with Path(self.filepath).open() as file:
                return file.readlines()[self.line - 1]
        except (OSError, IndexError):
            with Path(self.filepath).with_name(self.file_name).open() as file:
                return file.readlines()[self.line - 1]


@dataclass(kw_only=True)
class Target:
    """A reference target identified by its source file and qualified name."""

    source_file_name: str
    """Source file containing the target."""
    qualified_name: str
    """Qualified name of the referenced symbol."""


class TypeKind(enum.Enum):
    """Kinds of TypeScript types represented by TypeDoc."""

    ARRAY = "array"
    """An array type."""
    INTRINSIC = "intrinsic"
    """A built-in TypeScript type."""
    LITERAL = "literal"
    """A literal value type."""
    REFERENCE = "reference"
    """A reference to a named type."""
    REFLECTION = "reflection"
    """A type described by a reflection declaration."""
    UNION = "union"
    """A union of types."""
    TUPLE = "tuple"
    """A tuple type."""
    QUERY = "query"
    """A type query."""
    OPERATOR = "typeOperator"
    """A type operator expression."""
    INTERSECTION = "intersection"
    """An intersection of types."""
    MAPPED = "mapped"
    """A mapped type."""


@dataclass(kw_only=True)
class Type:
    """A TypeScript type and the details associated with its kind."""

    type: TypeKind
    """Kind of the TypeScript type."""
    name: str | None = None
    """Name of the type, when applicable."""
    target: int | Target | None = None
    """Reflection ID or external symbol targeted by a reference type."""
    package: str | None = None
    """Package containing the referenced type."""
    type_arguments: list[Type] | None = None
    """Type arguments supplied to a generic type."""
    qualified_name: str | None = None
    """Qualified name of the referenced symbol."""
    element_type: Type | None = None  # array
    """Element type of an array."""
    refers_to_type_parameter: bool | None = None
    """Whether the reference points to a type parameter."""
    value: str | None = None  # literal
    """Value of a literal type."""
    types: list[Type] | None = None  # union
    """Types in a union or intersection."""
    declaration: TypeLiteral | None = None  # reflection
    """Declaration of a reflection type."""
    elements: list[Type] | None = None
    """Element types of a tuple."""
    prefer_values: bool | None = None
    """Whether the type reference prefers a value target."""
    query_type: Type | None = None
    """Type referenced by a type query."""
    operator: str | None = None
    """Operator applied to a type."""
    parameter: str | None = None
    """Parameter name in a mapped type."""
    parameter_type: Type | None = None
    """Type of the parameter in a mapped type."""
    template_type: Type | None = None
    """Template type used by a mapped type."""


@dataclass(kw_only=True)
class Reflection:
    """Base model for a TypeDoc reflection."""

    id: int
    """Unique reflection ID within the project."""
    name: str
    """Name of the reflection."""
    variant: str
    """Reflection variant recorded by TypeDoc."""
    comment: Comment | None = None
    """Documentation comment associated with the reflection."""
    children: list[Reflection] = field(default_factory=list)
    """Child reflections."""
    flags: dict = field(default_factory=dict)
    """Reflection flags recorded by TypeDoc."""
    groups: list[Group] = field(default_factory=list)
    """Named groups of child reflections."""
    sources: list[Source] = field(default_factory=list)
    """Source locations of the reflection."""
    parent: Reflection | None = None
    """Parent reflection, or `None` for a root reflection."""
    type: Type | None = None
    """Type associated with the reflection."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        raise NotImplementedError

    @property
    def root_module(self) -> Reflection:
        """The highest ancestor below the project, or this reflection if it has no parent."""
        parent = self
        while parent.parent and parent.parent.kind is not ReflectionKind.PROJECT:
            parent = parent.parent
        return parent

    @property
    def root(self) -> Reflection:
        """The root ancestor of the reflection tree."""
        parent = self
        while parent.parent:
            parent = parent.parent
        return parent

    @property
    def path(self) -> str:
        """Slash-separated symbol path, with `index` modules omitted."""
        if self.parent is None or isinstance(self.parent, Project):
            return self.name
        if self.kind is ReflectionKind.MODULE and self.name == "index":
            return self.parent.path
        return f"{self.parent.path}/{self.name}"

    @property
    def symbol_map(self) -> dict[int, Reflection]:
        """Reflections indexed by ID, inherited from the parent when available."""
        try:
            return self.parent.symbol_map  # ty:ignore[unresolved-attribute]
        except AttributeError:
            return {}

    @property
    def resolved_target(self) -> Reflection:
        """Referenced reflection resolved through the symbol map."""
        return self.symbol_map[self.target]  # ty:ignore[unresolved-attribute]

    @property
    def final_target(self) -> Reflection:
        """Final reflection reached by following reference targets."""
        target = self.resolved_target
        if not hasattr(target, "target"):
            return target
        return target.final_target

    @property
    def resolved_groups(self) -> list[Group]:
        """Groups with child IDs replaced by their reflections."""
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
        """Source lines joined together, with trailing whitespace and an opening brace removed."""
        return "\n".join(source.contents for source in self.sources).rstrip().removesuffix("{")


@dataclass(kw_only=True)
class Project(Reflection):
    """The root reflection of a TypeDoc project."""

    package_name: str  # type: ignore[misc]
    """Name of the documented package."""
    readme: list[BlockTagContent] | None = None
    """README content associated with the reflection."""
    symbol_id_map: dict[int, Reflection] = field(default_factory=dict, repr=False)
    """Reflections indexed by ID."""
    package_version: str | None = None
    """Version of the documented package."""
    files: FileRegistry | None = None
    """Registry of source files in the project."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.PROJECT

    @property
    def symbol_map(self) -> dict[int, Reflection]:
        """Project reflections indexed by ID."""
        return self.symbol_id_map


@dataclass(kw_only=True)
class Module(Reflection):
    """A TypeScript module reflection."""

    package_version: str | None = None
    """Version of the documented package."""
    readme: str | None = None
    """README content associated with the reflection."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.MODULE

    @property
    def exports(self) -> list[Reflection]:
        """Reflections exported by the module through an `export=` function, or an empty list."""
        for child in self.children:
            if child.kind is ReflectionKind.FUNCTION and child.name == "export=":
                return child.exports  # ty:ignore[unresolved-attribute]
        return []


@dataclass(kw_only=True)
class Namespace(Reflection):
    """A TypeScript namespace reflection."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.NAMESPACE


@dataclass(kw_only=True)
class Enum(Reflection):
    """A TypeScript enum reflection."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.ENUM


@dataclass(kw_only=True)
class EnumMember(Reflection):
    """A member of a TypeScript enum."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.ENUM_MEMBER


@dataclass(kw_only=True)
class Variable(Reflection):
    """A TypeScript variable reflection."""

    type: Type  # type: ignore[misc]
    """Type of the variable."""
    default_value: str | None = None
    """Default value as TypeScript source text."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.VARIABLE


@dataclass(kw_only=True)
class Function(Reflection):
    """A TypeScript function and its call signatures."""

    signatures: list[CallSignature]  # type: ignore[misc]
    """Callable signatures of the reflection."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.FUNCTION

    @property
    def exports(self) -> list[Reflection]:
        """References to properties of the first signature's return type declaration."""
        return [
            Reference(
                id=prop.id,
                variant="reference",
                name=prop.name,
                target=prop.type.target,  # ty:ignore[invalid-argument-type,unresolved-attribute]
                parent=self.parent,
            )
            for prop in self.signatures[0].type.declaration.children  # ty:ignore[unresolved-attribute]
        ]


@dataclass(kw_only=True)
class Class(Reflection):
    """A TypeScript class reflection."""

    extended_types: list[Type] | None = None
    """Types extended by the declaration."""
    extended_by: list[Type] | None = None
    """Types that extend the declaration."""
    implemented_types: list[Type] | None = None
    """Interfaces implemented by the class."""
    index_signatures: list[IndexSignature] | None = None
    """Index signatures of the declaration."""
    type_parameters: list[TypeParameter] | None = None
    """Generic type parameters of the declaration."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.CLASS


@dataclass(kw_only=True)
class Interface(Reflection):
    """A TypeScript interface reflection."""

    extended_types: list[Type] | None = None
    """Types extended by the declaration."""
    extended_by: list[Type] | None = None
    """Types that extend the declaration."""
    type_parameters: list[TypeParameter] | None = None
    """Generic type parameters of the declaration."""
    index_signature: IndexSignature | None = None
    """Index signature of the interface."""
    implemented_by: list[Type] | None = None
    """Types that implement the declaration."""
    index_signatures: list[IndexSignature] | None = None
    """Index signatures of the declaration."""
    signatures: list[CallSignature] | None = None
    """Callable signatures of the reflection."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.INTERFACE


@dataclass(kw_only=True)
class Constructor(Reflection):
    """A constructor and its signatures."""

    signatures: list[ConstructorSignature] | None = None
    """Callable signatures of the reflection."""
    overwrites: Type | None = None
    """Reference to the declaration that this reflection overrides."""
    inherited_from: Type | None = None
    """Reference to the declaration that this reflection inherits."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.CONSTRUCTOR


@dataclass(kw_only=True)
class Property(Reflection):
    """A TypeScript property reflection."""

    type: Type  # type: ignore[misc]
    """Type of the property."""
    inherited_from: Type | None = None
    """Reference to the declaration that this reflection inherits."""
    overwrites: Type | None = None
    """Reference to the declaration that this reflection overrides."""
    default_value: str | None = None
    """Default value as TypeScript source text."""
    implementation_of: Type | None = None
    """Reference to the declaration that this reflection implements."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.PROPERTY


@dataclass(kw_only=True)
class Method(Reflection):
    """A TypeScript method and its call signatures."""

    signatures: list[CallSignature]  # type: ignore[misc]
    """Callable signatures of the reflection."""
    overwrites: Type | None = None
    """Reference to the declaration that this reflection overrides."""
    implementation_of: Type | None = None
    """Reference to the declaration that this reflection implements."""
    inherited_from: Type | None = None
    """Reference to the declaration that this reflection inherits."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.METHOD


@dataclass(kw_only=True)
class CallSignature(Reflection):
    """A callable signature with its parameters and return type."""

    type: Type  # type: ignore[misc]
    """Return type of the signature."""
    parameters: list[Parameter] | None = None
    """Parameters of the signature."""
    type_parameters: list[TypeParameter] | None = None
    """Generic type parameters of the declaration."""
    overwrites: Type | None = None
    """Reference to the declaration that this reflection overrides."""
    implementation_of: Type | None = None
    """Reference to the declaration that this reflection implements."""
    inherited_from: Type | None = None
    """Reference to the declaration that this reflection inherits."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.CALL_SIGNATURE


@dataclass(kw_only=True)
class IndexSignature(Reflection):
    """An index signature with its parameters and value type."""

    type: Type  # type: ignore[misc]
    """Value type of the index signature."""
    parameters: list[Parameter] | None = None
    """Parameters of the signature."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.INDEX_SIGNATURE


@dataclass(kw_only=True)
class ConstructorSignature(Reflection):
    """A constructor signature with its parameters."""

    parameters: list[Parameter] | None = None
    """Parameters of the signature."""
    overwrites: Type | None = None
    """Reference to the declaration that this reflection overrides."""
    inherited_from: Type | None = None
    """Reference to the declaration that this reflection inherits."""
    type_parameters: list[TypeParameter] | None = None
    """Generic type parameters of the declaration."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.CONSTRUCTOR_SIGNATURE


@dataclass(kw_only=True)
class Parameter(Reflection):
    """A parameter in a callable signature."""

    type: Type | None = None
    """Type of the parameter."""
    default_value: str | None = None
    """Default value as TypeScript source text."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.PARAMETER


@dataclass(kw_only=True)
class TypeLiteral(Reflection):
    """A type literal with its members and signatures."""

    signatures: list[CallSignature] | None = None
    """Callable signatures of the reflection."""
    index_signatures: list[IndexSignature] | None = None
    """Index signatures of the declaration."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.TYPE_LITERAL


@dataclass(kw_only=True)
class TypeParameter(Reflection):
    """A generic type parameter with an optional constraint and default."""

    type: Type | None = None
    """Type constraint of the generic parameter."""
    default: Type | None = None
    """Default type used when no type argument is supplied."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.TYPE_PARAMETER


@dataclass(kw_only=True)
class Accessor(Reflection):
    """A property accessor with getter and setter signatures."""

    get_signature: GetSignature | None = None
    """Getter signature of the accessor."""
    set_signature: SetSignature | None = None
    """Setter signature of the accessor."""
    overwrites: Type | None = None
    """Reference to the declaration that this reflection overrides."""
    implementation_of: Type | None = None
    """Reference to the declaration that this reflection implements."""
    inherited_from: Type | None = None
    """Reference to the declaration that this reflection inherits."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.ACCESSOR


@dataclass(kw_only=True)
class GetSignature(Reflection):
    """A getter signature."""

    overwrites: Type | None = None
    """Reference to the declaration that this reflection overrides."""
    implementation_of: Type | None = None
    """Reference to the declaration that this reflection implements."""
    inherited_from: Type | None = None
    """Reference to the declaration that this reflection inherits."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.GET_SIGNATURE


@dataclass(kw_only=True)
class SetSignature(Reflection):
    """A setter signature with its parameters."""

    parameters: list[Parameter] | None = None
    """Parameters of the signature."""
    overwrites: Type | None = None
    """Reference to the declaration that this reflection overrides."""
    implementation_of: Type | None = None
    """Reference to the declaration that this reflection implements."""
    inherited_from: Type | None = None
    """Reference to the declaration that this reflection inherits."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.SET_SIGNATURE


@dataclass(kw_only=True)
class TypeAlias(Reflection):
    """A TypeScript type alias reflection."""

    type: Type  # type: ignore[misc]
    """Type represented by the alias."""
    type_parameters: list[TypeParameter] | None = None
    """Generic type parameters of the declaration."""
    implemented_by: list[Type] | None = None
    """Types that implement the declaration."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.TYPE_ALIAS


@dataclass(kw_only=True)
class Reference(Reflection):
    """A reflection that refers to another reflection by ID."""

    target: int  # type: ignore[misc]
    """ID of the referenced reflection."""

    @property
    def kind(self) -> ReflectionKind:
        """Kind of the reflection."""
        return ReflectionKind.REFERENCE
