"""Griffe TypeDoc package.

Signatures for entire TypeScript programs using TypeDoc.
"""

from __future__ import annotations

from griffe_typedoc._internal.cli import get_parser, main
from griffe_typedoc._internal.decoder import TypedocDecoder
from griffe_typedoc._internal.loader import load
from griffe_typedoc._internal.logger import LogLevel, get_logger, patch_loggers
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
    Reflection,
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

__all__: list[str] = [
    "Accessor",
    "BlockTag",
    "BlockTagContent",
    "BlockTagContentKind",
    "BlockTagKind",
    "CallSignature",
    "Class",
    "Comment",
    "Constructor",
    "ConstructorSignature",
    "Enum",
    "EnumMember",
    "FileRegistry",
    "Function",
    "GetSignature",
    "Group",
    "IndexSignature",
    "Interface",
    "LogLevel",
    "Method",
    "Module",
    "Namespace",
    "Parameter",
    "Project",
    "Property",
    "Reference",
    "Reflection",
    "ReflectionKind",
    "SetSignature",
    "Source",
    "Target",
    "Type",
    "TypeAlias",
    "TypeKind",
    "TypeLiteral",
    "TypeParameter",
    "TypedocDecoder",
    "Variable",
    "get_logger",
    "get_parser",
    "load",
    "main",
    "patch_loggers",
]
