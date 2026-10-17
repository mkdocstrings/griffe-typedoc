# SPDX-License-Identifier: ISC
#
# ISC License
#
# Copyright (c) 2026, Timothée Mazzucotelli and contributors
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

"""Tests for decoding TypeDoc JSON output."""

from __future__ import annotations

import json

import pytest

from griffe_typedoc import Project, ReflectionKind, TypedocDecoder


@pytest.mark.parametrize("schema_version", [None, "2.0"])
def test_decode_project_schema_version(schema_version: str | None) -> None:
    """Decode projects from TypeDoc versions with and without schema metadata."""
    project_json = {
        "id": 0,
        "name": "package",
        "kind": 1,
        "variant": "project",
        "packageName": "package",
        "symbolIdMap": {},
        "children": [
            {
                "id": 1,
                "name": "message",
                "kind": 32,
                "variant": "declaration",
                "type": {"type": "intrinsic", "name": "string"},
            },
        ],
    }
    # Older TypeDoc output does not include schemaVersion.
    if schema_version is not None:
        project_json["schemaVersion"] = schema_version

    project = json.loads(json.dumps(project_json), cls=TypedocDecoder)

    # Schema metadata must not prevent decoding symbols or resolving their parents.
    assert isinstance(project, Project)
    assert project.schema_version == schema_version
    assert project.package_name == "package"
    variable = project.children[0]
    assert variable.kind is ReflectionKind.VARIABLE
    assert variable.name == "message"
    assert variable.parent is project
    assert project.symbol_map[variable.id] is variable
