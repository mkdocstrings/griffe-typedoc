"""Griffe TypeDoc package.

Signatures for entire TypeScript programs using TypeDoc.
"""

from __future__ import annotations

from griffe_typedoc._internal.cli import get_parser, main

__all__: list[str] = ["get_parser", "main"]
