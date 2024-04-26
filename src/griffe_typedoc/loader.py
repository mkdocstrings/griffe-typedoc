from __future__ import annotations

import json
import re
import subprocess
from tempfile import NamedTemporaryFile

from griffe_typedoc.dataclasses import Project
from griffe_typedoc.decoder import TypedocDecoder
from griffe_typedoc.logger import get_logger

logger = get_logger(__name__)


def _double_brackets(message: str) -> str:
    return message.replace("{", "{{").replace("}", "}}")


def load(typedoc_command: str | list[str], working_directory: str = ".") -> Project:
    with NamedTemporaryFile("r+") as tmpfile:
        if isinstance(typedoc_command, str):
            typedoc_command += f" --json {tmpfile.name}"
            shell = True
        else:
            typedoc_command += ["--json", tmpfile.name]
            shell = False
        process = subprocess.Popen(
            typedoc_command,
            shell=shell,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=working_directory,
        )
        while True:
            if line := process.stdout.readline().strip():  # type: ignore[union-attr]
                level, line = line.split(" ", 1)
                level = match.group(1) if (match := re.search(r"\[(\w+)\]", level)) else "INFO"
                getattr(logger, level)(_double_brackets(line))
            else:
                break
        process.wait()
        return json.load(tmpfile, cls=TypedocDecoder)
