#!/usr/bin/env python3
"""Generate the TEI subject index of liturgical celebrations from DO data."""

from __future__ import annotations

import argparse
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET


TEI_NS = "http://www.tei-c.org/ns/1.0"
XML_NS = "http://www.w3.org/XML/1998/namespace"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DO_LATIN_ROOTS = (
    PROJECT_ROOT / "sources/divinum-officium/web/www/missa/Latin",
    PROJECT_ROOT / "sources/divinum-officium/web/www/horas/Latin",
)
OUTPUT_PATH = PROJECT_ROOT / "data/indexes/celebrations.xml"
REVIEW_PATH = PROJECT_ROOT / "data/indexes/celebrations-review.tsv"

INCLUDED_DIRS = {
    "Tempora",
    "TemporaCist",
    "TemporaM",
    "TemporaOP",
    "Sancti",
    "SanctiCist",
    "SanctiM",
    "SanctiOP",
    "Commune",
    "CommuneCist",
    "CommuneM",
    "CommuneOP",
    "Appendix",
}

DOMAIN_BY_PREFIX = {
    "Tempora": "temporale",
    "Sancti": "sanctorale",
    "Commune": "commune",
    "Appendix": "appendix",
}

TRADITION_SUFFIXES = {
    "Cist": "cist",
    "M": "monasticum",
    "OP": "op",
}

ROMAN_NUMERALS = {
    "i": "1",
    "ii": "2",
    "iii": "3",
    "iv": "4",
    "v": "5",
    "vi": "6",
    "vii": "7",
    "viii": "8",
    "ix": "9",
    "x": "10",
    "xi": "11",
    "xii": "12",
    "xiii": "13",
    "xiv": "14",
    "xv": "15",
    "xvi": "16",
    "xvii": "17",
    "xviii": "18",
    "xix": "19",
    "xx": "20",
    "xxi": "21",
    "xxii": "22",
    "xxiii": "23",
    "xxiv": "24",
}

MANUAL_OVERRIDES_BY_SOURCE = {
    ("temporale", "Tempora", "Pasc5-0"): {
        "xml_id": "celebratio-temporale-dominica-5-post-pascha",
        "private_id": "temporale:dominica-5-post-pascha",
    },
    ("sanctorale", "Sancti", "03-21"): {
        "xml_id": "celebratio-sanctorale-benedictus-abbas-transitus",
        "private_id": "sanctorale:benedictus-abbas-transitus",
    },
}

SECTION_RE = re.compile(r"^\[([^]]+)]")
REFERENCE_RE = re.compile(r"^@([A-Za-z0-9_ ./-]+)")
VARIANT_SUFFIX_RE = re.compile(r"^(.+?\d(?:-\d)?)([a-z]+|Feria|Feriat|Feriae|t)+$")


@dataclass(frozen=True)
class SourceRecord:
    form: str
    do_dir: str
    key: str
    path: Path
    title: str | None
    redirect_ref: str | None = None

    @property
    def rel_path(self) -> Path:
        return self.path.relative_to(PROJECT_ROOT)


@dataclass
class CelebrationGroup:
    domain: str
    do_dir: str
    canonical_key: str
    preferred_title: str
    titles: set[str] = field(default_factory=set)
    sources: list[SourceRecord] = field(default_factory=list)
    xml_id: str | None = None
    private_id: str | None = None


def tei(tag: str) -> str:
    return f"{{{TEI_NS}}}{tag}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_PATH,
        help="Path of the generated TEI index.",
    )
    parser.add_argument(
        "--review-output",
        type=Path,
        default=REVIEW_PATH,
        help="Path of the generated review TSV.",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def parse_sections(path: Path) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in read_text(path).splitlines():
        match = SECTION_RE.match(line.strip())
        if match:
            current = match.group(1).strip()
            sections.setdefault(current, [])
            continue
        if current:
            sections[current].append(line.rstrip())
    return sections


def first_plain_line(lines: Iterable[str]) -> str | None:
    for line in lines:
        value = line.strip()
        if not value:
            continue
        if value.startswith(("!", "@", ";;", "$", "&")):
            continue
        return clean_title(value)
    return None


def clean_title(value: str) -> str:
    value = re.sub(r"\s+", " ", value.strip())
    value = value.strip("; ")
    return value


def top_level_reference(path: Path) -> str | None:
    for line in read_text(path).splitlines():
        value = line.strip()
        if not value:
            continue
        match = REFERENCE_RE.match(value)
        return match.group(1) if match else None
    return None


def classify_dir(do_dir: str) -> tuple[str, str | None]:
    for prefix, domain in DOMAIN_BY_PREFIX.items():
        if not do_dir.startswith(prefix):
            continue
        suffix = do_dir.removeprefix(prefix)
        tradition = TRADITION_SUFFIXES.get(suffix) if suffix else None
        return domain, tradition
    return "appendix", None


def canonical_key_for(domain: str, key: str) -> str:
    if domain != "temporale":
        return key
    match = VARIANT_SUFFIX_RE.match(key)
    return match.group(1) if match else key


def latin_root_form(root: Path) -> str:
    return root.parent.name


def collect_sources() -> list[SourceRecord]:
    records: list[SourceRecord] = []
    for root in DO_LATIN_ROOTS:
        if not root.exists():
            continue
        form = latin_root_form(root)
        for path in sorted(root.glob("*/*.txt")):
            do_dir = path.parent.name
            if do_dir not in INCLUDED_DIRS:
                continue
            sections = parse_sections(path)
            title = first_plain_line(sections.get("Officium", []))
            redirect_ref = top_level_reference(path) if not title else None
            records.append(
                SourceRecord(
                    form=form,
                    do_dir=do_dir,
                    key=path.stem,
                    path=path,
                    title=title,
                    redirect_ref=redirect_ref,
                )
            )
    return records


def grouping_key(record: SourceRecord) -> tuple[str, str, str]:
    domain, tradition = classify_dir(record.do_dir)
    canonical_key = canonical_key_for(domain, record.key)
    normalized_title = normalize_for_compare(record.title or "")
    if domain in {"sanctorale", "commune"} and normalized_title:
        return (domain, "", normalized_title)
    elif tradition:
        canonical_key = f"{canonical_key}-{tradition}"
    return (domain, record.do_dir, canonical_key)


def build_groups(records: list[SourceRecord]) -> tuple[list[CelebrationGroup], list[SourceRecord]]:
    groups: dict[tuple[str, str, str], CelebrationGroup] = {}
    source_aliases: dict[tuple[str, str, str], CelebrationGroup] = {}
    form_source_aliases: dict[tuple[str, str, str, str], CelebrationGroup] = {}
    record_index = {(record.form, record.do_dir, record.key): record for record in records}
    unmatched: list[SourceRecord] = []
    titled_records = [record for record in records if record.title]
    for record in titled_records:
        domain, _ = classify_dir(record.do_dir)
        canonical_key = canonical_key_for(domain, record.key)
        key = grouping_key(record)
        if domain in {"sanctorale", "commune"}:
            canonical_key = key[2]
        group = groups.get(key)
        if not group:
            group = CelebrationGroup(
                domain=domain,
                do_dir=record.do_dir,
                canonical_key=canonical_key,
                preferred_title=record.title or record.key,
            )
            groups[key] = group
        group.titles.add(record.title or record.key)
        group.sources.append(record)
        source_aliases[(domain, record.do_dir, canonical_key_for(domain, record.key))] = group
        form_source_aliases[(record.form, domain, record.do_dir, canonical_key_for(domain, record.key))] = group

    for record in records:
        if record.title:
            continue
        if record.redirect_ref:
            target = group_for_redirect(record, form_source_aliases, source_aliases, record_index)
            if target:
                target.sources.append(record)
                continue
        domain, _ = classify_dir(record.do_dir)
        candidates = [
            (domain, record.do_dir, canonical_key_for(domain, record.key)),
            (domain, record.do_dir, normalize_for_compare(record.key)),
        ]
        for key in candidates:
            group = groups.get(key) or source_aliases.get(key)
            if group:
                group.sources.append(record)
                break
        else:
            unmatched.append(record)

    assign_ids(groups.values())
    return (
        sorted(groups.values(), key=lambda g: (g.domain, sort_title(g.preferred_title), g.xml_id or "")),
        unmatched,
    )


def group_for_redirect(
    record: SourceRecord,
    form_source_aliases: dict[tuple[str, str, str, str], CelebrationGroup],
    source_aliases: dict[tuple[str, str, str], CelebrationGroup],
    record_index: dict[tuple[str, str, str], SourceRecord],
) -> CelebrationGroup | None:
    seen: set[tuple[str, str, str]] = set()
    current = record
    for _ in range(12):
        if not current.redirect_ref:
            return None
        parts = current.redirect_ref.split(":", 1)[0].split("/")
        if len(parts) != 2:
            return None
        target_dir, target_key = parts
        domain, _ = classify_dir(target_dir)
        canonical_key = canonical_key_for(domain, target_key)
        group = (
            form_source_aliases.get((current.form, domain, target_dir, canonical_key))
            or source_aliases.get((domain, target_dir, canonical_key))
        )
        if group:
            return group
        index_key = (current.form, target_dir, target_key)
        if index_key in seen:
            return None
        seen.add(index_key)
        target_record = record_index.get(index_key)
        if not target_record:
            return None
        current = target_record
    return None


def assign_ids(groups: Iterable[CelebrationGroup]) -> None:
    used_xml_ids: set[str] = set()
    used_private_ids: set[str] = set()
    for group in groups:
        override = override_for_group(group)
        slug = slugify(group.preferred_title)
        xml_id = override["xml_id"] if override else f"celebratio-{group.domain}-{slug}"
        private_id = override["private_id"] if override else f"{group.domain}:{slug}"
        group.xml_id = unique_value(xml_id, used_xml_ids)
        group.private_id = unique_value(private_id, used_private_ids, separator="-")


def override_for_group(group: CelebrationGroup) -> dict[str, str] | None:
    for source in group.sources:
        domain, _ = classify_dir(source.do_dir)
        override = MANUAL_OVERRIDES_BY_SOURCE.get((domain, source.do_dir, canonical_key_for(domain, source.key)))
        if override:
            return override
    return None


def unique_value(value: str, used: set[str], separator: str = "-") -> str:
    candidate = value
    counter = 2
    while candidate in used:
        candidate = f"{value}{separator}{counter}"
        counter += 1
    used.add(candidate)
    return candidate


def normalize_for_compare(value: str) -> str:
    return slugify(value)


def sort_title(value: str) -> str:
    return strip_accents(value).casefold()


def strip_accents(value: str) -> str:
    value = value.replace("æ", "ae").replace("Æ", "Ae")
    value = value.replace("œ", "oe").replace("Œ", "Oe")
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def slugify(value: str) -> str:
    value = strip_accents(value).casefold()
    words = re.findall(r"[a-z0-9]+", value)
    normalized_words = [ROMAN_NUMERALS.get(word, word) for word in words]
    slug = "-".join(normalized_words)
    return slug or "sine-titulo"


def build_tree(groups: list[CelebrationGroup]) -> ET.ElementTree:
    ET.register_namespace("", TEI_NS)
    root = ET.Element(tei("TEI"), {f"{{{XML_NS}}}lang": "la"})
    header = ET.SubElement(root, tei("teiHeader"))
    file_desc = ET.SubElement(header, tei("fileDesc"))
    title_stmt = ET.SubElement(file_desc, tei("titleStmt"))
    ET.SubElement(title_stmt, tei("title")).text = "Index celebrationum"
    publication_stmt = ET.SubElement(file_desc, tei("publicationStmt"))
    ET.SubElement(publication_stmt, tei("p")).text = "Usuale project."
    source_desc = ET.SubElement(file_desc, tei("sourceDesc"))
    ET.SubElement(source_desc, tei("p")).text = (
        "Born-digital register of liturgical celebrations, generated from Divinum Officium source files."
    )
    text = ET.SubElement(root, tei("text"), {"ana": "hc:IndexOfSubjects"})
    body = ET.SubElement(text, tei("body"))
    items = ET.SubElement(body, tei("list"))
    ET.SubElement(items, tei("head")).text = "Index celebrationum"
    for group in groups:
        add_item(items, group)
    ET.indent(root, space="  ")
    return ET.ElementTree(root)


def add_item(parent: ET.Element, group: CelebrationGroup) -> None:
    item = ET.SubElement(parent, tei("item"), {f"{{{XML_NS}}}id": group.xml_id or ""})
    ET.SubElement(
        item,
        tei("label"),
        {f"{{{XML_NS}}}lang": "la", "ana": "hc:PreferredAppellation"},
    ).text = group.preferred_title
    for title in sorted(group.titles - {group.preferred_title}, key=sort_title):
        ET.SubElement(
            item,
            tei("label"),
            {f"{{{XML_NS}}}lang": "la", "ana": "hc:AlternativeAppellation"},
        ).text = title
    ET.SubElement(item, tei("idno"), {"ana": "hc:PrivateIdentifier"}).text = group.private_id
    refs = ET.SubElement(item, tei("listRef"))
    ET.SubElement(refs, tei("desc")).text = "Fontes Divinum Officium"
    for source in sorted(unique_sources(group.sources), key=lambda s: str(s.rel_path)):
        ref = ET.SubElement(refs, tei("ref"), {"target": relative_target(source.rel_path)})
        ref.text = source_label(source)


def unique_sources(sources: Iterable[SourceRecord]) -> list[SourceRecord]:
    seen: set[Path] = set()
    unique: list[SourceRecord] = []
    for source in sources:
        if source.rel_path in seen:
            continue
        seen.add(source.rel_path)
        unique.append(source)
    return unique


def relative_target(path: Path) -> str:
    return str(Path("../..") / path)


def source_label(source: SourceRecord) -> str:
    rel = source.rel_path
    return "/".join(rel.parts[4:])


def write_tree(tree: ET.ElementTree, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    tree.write(output, encoding="utf-8", xml_declaration=True)
    content = output.read_text(encoding="utf-8")
    model = (
        '<?xml-model href="https://digi.ub.uni-heidelberg.de/schema/tei/heiEDITIONS/tei_hes_index.rng" '
        'type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>\n'
    )
    content = content.replace("?>\n<TEI", f"?>\n{model}<TEI", 1)
    output.write_text(content, encoding="utf-8")


def write_review(unmatched: list[SourceRecord], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = ["kind\tform\tdirectory\tkey\tpath\tredirect_ref\n"]
    for source in sorted(unmatched, key=lambda s: str(s.rel_path)):
        lines.append(
            "\t".join(
                [
                    "unmatched_source",
                    source.form,
                    source.do_dir,
                    source.key,
                    str(source.rel_path),
                    source.redirect_ref or "",
                ]
            )
            + "\n"
        )
    output.write_text("".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    records = collect_sources()
    groups, unmatched = build_groups(records)
    write_tree(build_tree(groups), args.output)
    write_review(unmatched, args.review_output)
    print(f"records={len(records)}")
    print(f"celebrations={len(groups)}")
    print(f"unmatched={len(unmatched)}")
    print(f"output={args.output}")
    print(f"review={args.review_output}")


if __name__ == "__main__":
    main()
