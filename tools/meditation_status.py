#!/usr/bin/env python3
"""Report and validate the editorial status of Usuale meditations."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MEDITATIONS_DIR = PROJECT_ROOT / "data/meditations"
ALLOWED_STATUSES = ("draft", "in_review", "reviewed", "final")
REQUIRED_FIELDS = (
    "id",
    "title",
    "celebration",
    "celebration_ref",
    "liturgical_form",
    "primary_section",
    "primary_source",
    "primary_incipit",
    "status",
)
SCALAR_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_]*):(?:[ \t]*(.*))?$")
LIST_ITEM_RE = re.compile(r"^[ \t]+-[ \t]+(.+)$")


@dataclass(frozen=True)
class Meditation:
    path: Path
    metadata: dict[str, str | list[str]]

    @property
    def title(self) -> str:
        value = self.metadata.get("title")
        return value if isinstance(value, str) else self.path.stem

    @property
    def status(self) -> str:
        value = self.metadata.get("status")
        return value if isinstance(value, str) else ""

    @property
    def reviewed_at(self) -> str:
        value = self.metadata.get("reviewed_at")
        return value if isinstance(value, str) else ""

    @property
    def reviewed_by(self) -> str:
        value = self.metadata.get("reviewed_by")
        return value if isinstance(value, str) else ""

    @property
    def editorial_notes(self) -> list[str]:
        value = self.metadata.get("editorial_notes", [])
        return value if isinstance(value, list) else []


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Show and validate meditation editorial statuses."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit with a non-zero status if metadata is invalid.",
    )
    parser.add_argument(
        "--status",
        choices=ALLOWED_STATUSES,
        help="Show only meditations with this status.",
    )
    return parser.parse_args()


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def read_front_matter(path: Path) -> tuple[dict[str, str | list[str]], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []
    if not lines or lines[0].strip() != "---":
        return {}, ["missing opening YAML front matter delimiter"]

    try:
        end = next(
            index for index, line in enumerate(lines[1:], start=1)
            if line.strip() == "---"
        )
    except StopIteration:
        return {}, ["missing closing YAML front matter delimiter"]

    metadata: dict[str, str | list[str]] = {}
    current_list: str | None = None
    for line_number, line in enumerate(lines[1:end], start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        list_match = LIST_ITEM_RE.match(line)
        if list_match and current_list:
            value = metadata[current_list]
            if isinstance(value, list):
                value.append(unquote(list_match.group(1)))
            continue

        scalar_match = SCALAR_RE.match(line)
        if not scalar_match:
            errors.append(f"line {line_number}: unsupported YAML syntax")
            current_list = None
            continue

        key, raw_value = scalar_match.groups()
        if key in metadata:
            errors.append(f"line {line_number}: duplicate field {key!r}")
            current_list = None
            continue

        if raw_value:
            metadata[key] = [] if raw_value.strip() == "[]" else unquote(raw_value)
            current_list = None
        else:
            metadata[key] = []
            current_list = key

    return metadata, errors


def load_meditations() -> tuple[list[Meditation], dict[Path, list[str]]]:
    meditations: list[Meditation] = []
    parse_errors: dict[Path, list[str]] = {}
    for path in sorted(MEDITATIONS_DIR.glob("*.md")):
        metadata, errors = read_front_matter(path)
        meditations.append(Meditation(path=path, metadata=metadata))
        if errors:
            parse_errors[path] = errors
    return meditations, parse_errors


def validate(meditation: Meditation) -> list[str]:
    errors: list[str] = []
    metadata = meditation.metadata

    for field in REQUIRED_FIELDS:
        value = metadata.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"missing required field {field!r}")

    if meditation.status and meditation.status not in ALLOWED_STATUSES:
        allowed = ", ".join(ALLOWED_STATUSES)
        errors.append(f"invalid status {meditation.status!r}; expected one of: {allowed}")

    expected_id = meditation.path.stem
    meditation_id = metadata.get("id")
    if isinstance(meditation_id, str) and meditation_id != expected_id:
        errors.append(f"id {meditation_id!r} does not match filename {expected_id!r}")

    notes_value = metadata.get("editorial_notes")
    if notes_value is not None and not isinstance(notes_value, list):
        errors.append("'editorial_notes' must be a YAML list")

    if meditation.status in {"reviewed", "final"}:
        if not meditation.reviewed_at:
            errors.append(f"status {meditation.status!r} requires 'reviewed_at'")
        else:
            try:
                date.fromisoformat(meditation.reviewed_at)
            except ValueError:
                errors.append("'reviewed_at' must use YYYY-MM-DD format")
        if not meditation.reviewed_by:
            errors.append(f"status {meditation.status!r} requires 'reviewed_by'")

    if meditation.status in {"reviewed", "final"} and meditation.editorial_notes:
        errors.append(
            f"status {meditation.status!r} cannot have open 'editorial_notes'"
        )

    return errors


def print_report(meditations: list[Meditation]) -> None:
    headers = ("Meditation", "Status", "Review", "Open")
    rows = [
        (
            meditation.title,
            meditation.status or "missing",
            meditation.reviewed_at or "-",
            str(len(meditation.editorial_notes)),
        )
        for meditation in meditations
    ]
    widths = []
    for index, header in enumerate(headers):
        values = [len(row[index]) for row in rows]
        widths.append(max([len(header), *values]))
    print("  ".join(header.ljust(widths[index]) for index, header in enumerate(headers)))
    print("  ".join("-" * width for width in widths))
    for row in rows:
        print("  ".join(value.ljust(widths[index]) for index, value in enumerate(row)))

    counts = {status: 0 for status in ALLOWED_STATUSES}
    for meditation in meditations:
        if meditation.status in counts:
            counts[meditation.status] += 1
    summary = ", ".join(f"{status}: {counts[status]}" for status in ALLOWED_STATUSES)
    print(f"\nTotal: {len(meditations)} ({summary})")


def main() -> int:
    args = parse_args()
    meditations, parse_errors = load_meditations()
    if args.status:
        meditations = [
            meditation for meditation in meditations
            if meditation.status == args.status
        ]

    print_report(meditations)

    errors = dict(parse_errors)
    for meditation in meditations:
        validation_errors = validate(meditation)
        if validation_errors:
            errors.setdefault(meditation.path, []).extend(validation_errors)

    if errors:
        print("\nMetadata problems:", file=sys.stderr)
        for path, messages in sorted(errors.items()):
            relative_path = path.relative_to(PROJECT_ROOT)
            for message in messages:
                print(f"- {relative_path}: {message}", file=sys.stderr)
        return 1 if args.check else 0

    if args.check:
        print("\nMetadata check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
