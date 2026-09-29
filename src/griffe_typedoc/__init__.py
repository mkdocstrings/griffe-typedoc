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
