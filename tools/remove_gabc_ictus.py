#!/usr/bin/env python3
"""Remove apostrophe-encoded vertical episemata from GABC notation."""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


HEADER_SEPARATOR_RE = re.compile(r"(?m)^[ \t]*%%[ \t]*(?:\r?\n|$)")


class GabcFormatError(ValueError):
    """Raised when a file does not contain a GABC header separator."""


@dataclass(frozen=True)
class TransformResult:
    text: str
    removed: int


def remove_vertical_episemata(text: str) -> TransformResult:
    """Remove ASCII apostrophes inside notation groups after the GABC header."""
    separator = HEADER_SEPARATOR_RE.search(text)
    if separator is None:
        raise GabcFormatError("missing GABC header separator '%%'")

    notation_start = separator.end()
    prefix = text[:notation_start]
    notation = text[notation_start:]
    output: list[str] = []
    group_depth = 0
    removed = 0

    for character in notation:
        if character == "(":
            group_depth += 1
            output.append(character)
        elif character == ")":
            if group_depth > 0:
                group_depth -= 1
            output.append(character)
        elif character == "'" and group_depth > 0:
            removed += 1
        else:
            output.append(character)

    return TransformResult(prefix + "".join(output), removed)


def collect_gabc_files(paths: Iterable[Path]) -> list[Path]:
    files: set[Path] = set()
    for path in paths:
        if path.is_dir():
            files.update(candidate for candidate in path.rglob("*.gabc") if candidate.is_file())
        elif path.is_file():
            files.add(path)
        else:
            raise FileNotFoundError(path)
    return sorted(files)


def write_atomically(path: Path, text: str) -> None:
    mode = path.stat().st_mode
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        newline="",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as temporary:
        temporary.write(text)
        temporary_path = Path(temporary.name)

    try:
        os.chmod(temporary_path, mode)
        os.replace(temporary_path, path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Remove apostrophe-encoded vertical episemata from GABC notation "
            "groups. Headers and text outside notation groups are preserved."
        )
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="GABC files or directories to process recursively.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--check",
        action="store_true",
        help="Do not modify files; exit 1 when vertical episemata are found.",
    )
    mode.add_argument(
        "--stdout",
        action="store_true",
        help="Write one transformed file to stdout without modifying it.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        files = collect_gabc_files(args.paths)
    except FileNotFoundError as error:
        print(f"error: path does not exist: {error}", file=sys.stderr)
        return 2

    if not files:
        print("error: no .gabc files found", file=sys.stderr)
        return 2
    if args.stdout and len(files) != 1:
        print("error: --stdout requires exactly one GABC file", file=sys.stderr)
        return 2

    found = False
    format_error = False
    for path in files:
        try:
            original = path.read_text(encoding="utf-8")
            result = remove_vertical_episemata(original)
        except (OSError, UnicodeError, GabcFormatError) as error:
            print(f"{path}: error: {error}", file=sys.stderr)
            format_error = True
            continue

        if args.stdout:
            sys.stdout.write(result.text)
            continue

        if result.removed:
            found = True
            if args.check:
                print(f"{path}: {result.removed} vertical episema marker(s)")
            else:
                write_atomically(path, result.text)
                print(f"{path}: removed {result.removed} vertical episema marker(s)")
        elif not args.check:
            print(f"{path}: unchanged")

    if format_error:
        return 2
    if args.check and found:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
