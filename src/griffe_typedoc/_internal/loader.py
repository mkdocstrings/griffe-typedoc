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

import json
import os
import re
import subprocess
from tempfile import NamedTemporaryFile
from typing import TYPE_CHECKING

from griffe_typedoc._internal.decoder import TypedocDecoder
from griffe_typedoc._internal.logger import get_logger

if TYPE_CHECKING:
    from griffe_typedoc._internal.models import Project

_logger = get_logger(__name__)


def _double_brackets(message: str) -> str:
    return message.replace("{", "{{").replace("}", "}}")


def load(typedoc_command: str | list[str], working_directory: str = ".") -> Project:
    """Load TypeScript API data using TypeDoc.

    Parameters:
        typedoc_command: Name/path of the 1`typedoc` executable, or a command as list.
        working_directory: Where to execute the command.

    Returns:
        Top-level project object containing API data.
    """
    with NamedTemporaryFile("r+") as tmpfile:
        if isinstance(typedoc_command, str):
            typedoc_command += f" --json {tmpfile.name}"
            shell = True
        else:
            typedoc_command += ["--json", tmpfile.name]
            shell = False
        env = os.environ.copy()
        env["NO_COLOR"] = "1"
        process = subprocess.Popen(  # noqa: S603
            typedoc_command,
            shell=shell,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=working_directory,
            env=env,
        )
        while True:
            if line := process.stdout.readline().strip():  # ty:ignore[unresolved-attribute]
                level, line = line.split(" ", 1)
                level = match.group(1) if (match := re.search(r"\[(\w+)\]", level)) else "info"
                getattr(_logger, level.lower())(_double_brackets(line))
            else:
                break
        process.wait()
        return json.load(tmpfile, cls=TypedocDecoder)
