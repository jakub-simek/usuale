#!/usr/bin/env python3
from __future__ import annotations

import csv
import html
import json
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path


ROOT = Path("sources/divinum-officium/web/www/horas/Latin")
OUT_DIR = Path("data/studies/corpora/roman-breviary-pre-divino-afflatu")
OUT_MD = OUT_DIR / "nonbiblical-reading-sources.md"
OUT_CSV = OUT_DIR / "nonbiblical-reading-sources.csv"
OUT_EXCLUDED_CSV = OUT_DIR / "excluded-source-lines.csv"
OUT_JSON = OUT_DIR / "nonbiblical-reading-sources.json"
OUT_AUTHOR_SVG = OUT_DIR / "assets/authors.svg"
OUT_WORK_SVG = OUT_DIR / "assets/works.svg"

BASE_DIRS = ["Tempora", "Sancti", "Commune"]
SKIP_PARTS = {"aliquibus locis", "Urbis", "Votiva"}

BIB_BOOKS = [
    "Gen", "Exod", "Lev", "Num", "Deut", "Jos", "Judic", "Judg", "Ruth",
    "1 Reg", "2 Reg", "3 Reg", "4 Reg", "1 Paral", "2 Paral",
    "1 Chr", "2 Chr", "1 Chron", "2 Chron", "Esdr",
    "Nehem", "Tob", "Judith", "Jdt", "Esth", "Job", "Ps", "Prov", "Eccl",
    "Cant", "Song", "Sap", "Wis", "Eccli", "Sir", "Isa", "Isai", "Is",
    "Jer", "Lam", "Bar", "Ezech", "Ezek", "Dan", "Osee", "Joel", "Amos", "Abd", "Jonas", "Mich", "Mic", "Nah",
    "Hab", "Soph", "Agg", "Zach", "Mal", "Matt", "Marc", "Luc", "Joann",
    "Joannes", "Act", "Acts", "Rom", "1 Cor", "2 Cor", "Gal", "Eph", "Phil", "Col",
    "1 Thess", "2 Thess", "1 Tim", "2 Tim", "Tit", "Titus", "Philem",
    "Phlm", "Hebr", "Heb", "Jac", "Jas", "1 Pet", "2 Pet", "1 Petr", "2 Petr", "Petr",
    "1 Joann",
    "2 Joann", "3 Joann", "1 Joannes", "2 Joannes", "3 Joannes",
    "Jude", "Judas", "Apoc", "Apo", "Apoc",
    "1 Mac", "2 Mac", "1 Macc", "2 Macc",
]

AUTHOR_PATTERNS = [
    ("Augustinus Hipponensis", r"August"),
    ("Ambrosius Mediolanensis", r"Ambros"),
    ("Gregorius Magnus", r"Gregor"),
    ("Leo Magnus", r"\bLeonis\b|\bLeo\b"),
    ("Hieronymus Stridonensis", r"Hieronym"),
    ("Beda Venerabilis", r"\bBed"),
    ("Ioannes Chrysostomus", r"Chrysost|Joann(?:is|es).*Chrys"),
    ("Bernardus Claraevallensis", r"Bernard"),
    ("Athanasius Alexandrinus", r"Athanas"),
    ("Hilarius Pictaviensis", r"Hilar"),
    ("Fulgentius Ruspensis", r"Fulgent"),
    ("Maximus Taurinensis", r"Maxim"),
    ("Cyprianus Carthaginiensis", r"Cyprian"),
    ("Isidorus Hispalensis", r"Isidor"),
    ("Anselmus Cantuariensis", r"Anselm"),
    ("Basilius Magnus", r"Basili"),
    ("Ephraem Syrus", r"Ephr"),
    ("Petrus Chrysologus", r"Chrysolog"),
    ("Petrus Damianus", r"Damian"),
    ("Cyrillus Alexandrinus", r"Cyrill"),
    ("Irenaeus Lugdunensis", r"Iren"),
    ("Origenes", r"Origen"),
    ("Rabanus Maurus", r"Raban"),
    ("Vigilius Tapsensis", r"Vigil"),
    ("Theodoretus Cyrrhensis", r"Theodoret"),
    ("Ioannes Damascenus", r"Damasc"),
    ("Sophronius Hierosolymitanus", r"Sophron"),
    ("Gaudentius Brixiensis", r"Gaudent"),
    ("Asterius Amaseenus", r"Aster"),
    ("Bonaventura", r"Bonavent"),
    ("Thomas Aquinas", r"Thom"),
    ("Epiphanius Salaminensis", r"Epiphan"),
    ("Tarasius Constantinopolitanus", r"Tharas|Taras"),
    ("Felix IV Papa", r"Felicis Papae quarti"),
    ("Petrus Canisius", r"Canis"),
]


@dataclass
class Section:
    name: str
    start_line: int
    lines: list[str]


@dataclass
class Record:
    corpus: str
    file: str
    line: int
    office: str
    section: str
    lesson_span: str
    lesson_count: int
    author: str
    work: str
    source: str
    author_line: str
    incipit: str


@dataclass
class Excluded:
    reason: str
    corpus: str
    file: str
    line: int
    office: str
    section: str
    source: str
    author_line: str


def strip_accents(text: str) -> str:
    text = (
        text.replace("æ", "ae")
        .replace("Æ", "Ae")
        .replace("œ", "oe")
        .replace("Œ", "Oe")
    )
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def norm_space(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\u00a0", " ")).strip()


def clean_markup(text: str) -> str:
    text = re.sub(r"\{:[^}]+:\}", "", text)
    text = text.replace("_", " ")
    text = re.sub(r"^\(?sed rubrica[^)]*\)\s*", "", text, flags=re.I)
    return norm_space(text)


def parse_sections(path: Path) -> list[Section]:
    sections: list[Section] = []
    current_name: str | None = None
    current_start = 0
    current_lines: list[str] = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        m = re.match(r"^\[([^]]+)\]\s*$", raw)
        if m:
            if current_name is not None:
                sections.append(Section(current_name, current_start, current_lines))
            current_name = m.group(1)
            current_start = lineno
            current_lines = []
        elif current_name is not None:
            current_lines.append(raw.rstrip("\n"))
    if current_name is not None:
        sections.append(Section(current_name, current_start, current_lines))
    return sections


def section_number(name: str) -> int | None:
    m = re.match(r"Lectio(\d+)", name)
    return int(m.group(1)) if m else None


def is_biblical_source(source: str) -> bool:
    source0 = strip_accents(source).strip()
    if not source0:
        return False
    for book in BIB_BOOKS:
        pattern = r"^" + re.escape(book) + r"\b"
        if re.search(pattern, source0, flags=re.I):
            return True
    if re.search(r"^(?:Epistola|Evangelium)\b", source0, flags=re.I):
        return True
    return False


def likely_author_line(line: str) -> bool:
    line0 = strip_accents(clean_markup(line)).lower()
    if not line0 or line0.startswith(("!", "@", "$", "&")):
        return False
    saint_title = re.search(r"\bsanct(?:i|ae|o|um|orum|arum)\b", line0)
    markers = [
        "beati", "beatae", "venerabilis", "sermo", "homilia",
        "ex libro", "de libro", "ex commentario", "ex expositione",
        "tractatus", "lectio sancti", "ex opere", "ex epistola",
    ]
    return bool(saint_title) or any(m in line0 for m in markers)


def is_author_heading_source(source: str) -> bool:
    source0 = strip_accents(clean_markup(source)).lower()
    if not likely_author_line(source):
        return False
    citation_markers = [
        r"\b(?:lib|liber|cap|homil|homilia|serm|sermo|tract|tractatus|epist|orat)\.?\s*\d",
        r"\b(?:in|de)\s+(?:joann|luc|matth|marc|psalm|cant|evang)",
    ]
    return not any(re.search(pattern, source0) for pattern in citation_markers)


def nonbib_sources(section: Section) -> list[tuple[int, str]]:
    raw_sources: list[tuple[int, str]] = []
    for idx, line in enumerate(section.lines):
        if line.startswith("!"):
            source = clean_markup(line[1:])
            if source and not is_biblical_source(source):
                raw_sources.append((idx, source))

    sources: list[tuple[int, str]] = []
    for pos, (idx, source) in enumerate(raw_sources):
        later_real_source = any(
            not is_author_heading_source(later_source)
            for _, later_source in raw_sources[pos + 1:]
        )
        if is_author_heading_source(source) and later_real_source:
            continue
        sources.append((idx, source))
    return sources


def find_author_line(section: Section, source_idx: int) -> str:
    for line in reversed(section.lines[:source_idx]):
        cleaned = clean_markup(line)
        if line.startswith("!"):
            bang_cleaned = clean_markup(line[1:])
            if is_author_heading_source(bang_cleaned):
                return bang_cleaned
        if likely_author_line(cleaned):
            return cleaned
    return ""


def canonical_author(author_line: str, source: str) -> str:
    hay = strip_accents(f"{author_line} {source}")
    for author, pattern in AUTHOR_PATTERNS:
        if re.search(pattern, hay, flags=re.I):
            return author
    cleaned = re.sub(r"^(?:Sermo|Homil[ií]a|Lectio)\s+", "", author_line, flags=re.I)
    cleaned = re.sub(r"^(?:Ex|De)\s+(?:libro|commentario|expositione|opere)\s+", "", cleaned, flags=re.I)
    return cleaned or "Unklarer Autor"


def canonical_work(author: str, source: str, author_line: str) -> str:
    s = strip_accents(source).lower()
    a = strip_accents(author_line).lower()
    if author == "Ambrosius Mediolanensis" and "luc" in s:
        return "Expositio evangelii secundum Lucam"
    if author == "Ambrosius Mediolanensis" and "apolog" in s:
        return "Apologia David"
    if author == "Augustinus Hipponensis" and "joann" in s:
        return "Tractatus in Iohannis Evangelium"
    if author == "Augustinus Hipponensis" and ("psalm" in s or "psal" in s):
        return "Enarrationes in Psalmos"
    if author == "Augustinus Hipponensis" and "verbis domini" in s:
        return "Sermones de verbis Domini"
    if author == "Augustinus Hipponensis" and "serm" in s:
        return "Sermones"
    if author == "Augustinus Hipponensis" and "civitate dei" in s:
        return "De civitate Dei"
    if author == "Gregorius Magnus" and "evangel" in s:
        return "Homiliae in Evangelia"
    if author == "Gregorius Magnus" and ("ezech" in s or "ezec" in s):
        return "Homiliae in Ezechielem"
    if author == "Gregorius Magnus" and ("moral" in s or "job" in s):
        return "Moralia in Iob"
    if author == "Gregorius Magnus" and "pastor" in s:
        return "Regula pastoralis"
    if author == "Leo Magnus" and "serm" in s:
        return "Sermones"
    if author == "Hieronymus Stridonensis" and "matth" in s:
        return "Commentarii in Matthaeum"
    if author == "Hieronymus Stridonensis" and "epist" in s:
        return "Epistulae"
    if author == "Beda Venerabilis" and "luc" in s:
        return "Expositio in Lucam / homiliae de tempore"
    if author == "Ioannes Chrysostomus" and "matth" in s:
        return "Homiliae in Matthaeum"
    if author == "Bernardus Claraevallensis" and "cant" in s:
        return "Sermones super Cantica canticorum"
    if "sermo" in a or "serm" in s:
        return "Sermones"
    if "homilia" in a or "homil" in s:
        base = re.sub(r",?\s*(?:homil(?:ia)?\.?|serm(?:o)?\.?)\s*\d+.*$", "", source, flags=re.I)
        return norm_space(base) or "Homiliae"
    return source


def office_title(sections: list[Section]) -> str:
    for section in sections:
        if section.name == "Officium":
            lines = [clean_markup(line) for line in section.lines if clean_markup(line)]
            return lines[0] if lines else ""
    return ""


def first_text_after_source(section: Section, source_idx: int) -> str:
    for line in section.lines[source_idx + 1:]:
        cleaned = clean_markup(line)
        if not cleaned or cleaned.startswith(("!", "@", "$", "&")):
            continue
        if cleaned.lower().startswith("in illo tempore"):
            continue
        return cleaned[:180]
    return ""


def inferred_span(sections: list[Section], idx: int) -> tuple[str, int]:
    section = sections[idx]
    n = section_number(section.name)
    if n is None:
        return section.name, 1
    if n in (1, 4, 7):
        expected_end = n + 2
    else:
        expected_end = n

    nums = [n]
    for later in sections[idx + 1:]:
        later_n = section_number(later.name)
        if later_n is None:
            continue
        if later_n <= nums[-1] or later_n > expected_end:
            break
        if nonbib_sources(later) or any(line.startswith("!") for line in later.lines):
            break
        if any(likely_author_line(line) for line in later.lines):
            break
        nums.append(later_n)
        if later_n == expected_end:
            break
    if len(nums) == 1:
        return f"Lectio{n}", 1
    return f"Lectio{nums[0]}-{nums[-1]}", len(nums)


def files_to_scan() -> list[Path]:
    allowed_sancti = allowed_sancti_stems_1906()
    paths: list[Path] = []
    for dirname in BASE_DIRS:
        for path in (ROOT / dirname).rglob("*.txt"):
            if any(part in SKIP_PARTS for part in path.parts):
                continue
            if dirname == "Sancti" and path.stem not in allowed_sancti:
                continue
            paths.append(path)
    return sorted(paths)


def calendar_entries(path: Path) -> dict[str, set[str]]:
    entries: dict[str, set[str]] = {}
    if not path.exists():
        return entries
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("*"):
            continue
        parts = line.split("=")
        if len(parts) < 2:
            continue
        day, refs = parts[0], parts[1]
        if refs == "XXXXX":
            entries[day] = set()
            continue
        stems = {ref for ref in refs.split("~") if ref and ref != "XXXXX"}
        entries[day] = stems
    return entries


def allowed_sancti_stems_1906() -> set[str]:
    base = Path("sources/divinum-officium/web/www/Tabulae/Kalendaria")
    calendar: dict[str, set[str]] = {}
    for name in ["1570.txt", "1888.txt", "1906.txt"]:
        calendar.update(calendar_entries(base / name))
    return {stem for stems in calendar.values() for stem in stems}


def exclusion_reason(source: str, author_line: str, section: Section) -> str | None:
    combined = strip_accents(" ".join([source, author_line, *section.lines])).lower()
    source0 = strip_accents(source).lower()
    if re.match(r"^(commemoratio|si lectio commemorandi)\b", source0):
        return "Kommemorationsmarker, keine eigentliche Werkquelle"
    post_1906_markers = [
        "pii papae undecimi",
        "pii papae duodecimi",
        "pius undecimus",
        "pius duodecimus",
        "benedictus decimus quintus",
        "benedictus xv",
        "quas primas",
        "miserentissimus redemptor",
        "ad caeli reginam",
        "anno millesimo nongentesimo",
        "1925",
        "1931",
        "1942",
        "1954",
    ]
    if any(marker in combined for marker in post_1906_markers):
        return "post-1906-Textschicht in DO"
    return None


def scan() -> tuple[list[Record], list[Excluded]]:
    records: list[Record] = []
    excluded: list[Excluded] = []
    for path in files_to_scan():
        sections = parse_sections(path)
        title = office_title(sections)
        rel = path.relative_to(ROOT).as_posix()
        corpus = rel.split("/", 1)[0]
        for idx, section in enumerate(sections):
            if not section.name.startswith("Lectio"):
                continue
            sources = nonbib_sources(section)
            if not sources:
                continue
            span, count = inferred_span(sections, idx)
            for source_idx, source in sources:
                author_line = find_author_line(section, source_idx)
                reason = exclusion_reason(source, author_line, section)
                if reason:
                    excluded.append(
                        Excluded(
                            reason=reason,
                            corpus=corpus,
                            file=rel,
                            line=section.start_line + source_idx + 1,
                            office=title,
                            section=section.name,
                            source=source,
                            author_line=author_line,
                        )
                    )
                    continue
                author = canonical_author(author_line, source)
                work = canonical_work(author, source, author_line)
                records.append(
                    Record(
                        corpus=corpus,
                        file=rel,
                        line=section.start_line + source_idx + 1,
                        office=title,
                        section=section.name,
                        lesson_span=span,
                        lesson_count=count,
                        author=author,
                        work=work,
                        source=source,
                        author_line=author_line,
                        incipit=first_text_after_source(section, source_idx),
                    )
                )
    return records, excluded


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def link(record: Record) -> str:
    return f"`{record.file}:{record.line}`"


def write_csv(records: list[Record]) -> None:
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(records[0]).keys()))
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))


def write_excluded_csv(records: list[Excluded]) -> None:
    with OUT_EXCLUDED_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(asdict(records[0]).keys()))
        writer.writeheader()
        for record in records:
            writer.writerow(asdict(record))


def write_json(records: list[Record]) -> None:
    OUT_JSON.write_text(
        json.dumps([asdict(r) for r in records], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def bar_svg(counter: Counter[str], title: str, out: Path, limit: int = 20) -> None:
    items = counter.most_common(limit)
    label_w = 280
    bar_w = 520
    row_h = 26
    top = 54
    width = label_w + bar_w + 90
    height = top + row_h * len(items) + 28
    max_v = max((v for _, v in items), default=1)
    rows = []
    for i, (label, value) in enumerate(items):
        y = top + i * row_h
        w = int(bar_w * value / max_v)
        rows.append(
            f'<text x="12" y="{y + 16}" font-size="12">{html.escape(label[:42])}</text>'
            f'<rect x="{label_w}" y="{y + 4}" width="{w}" height="16" fill="#5b7f95"/>'
            f'<text x="{label_w + w + 8}" y="{y + 16}" font-size="12">{value}</text>'
        )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">\n'
        '<rect width="100%" height="100%" fill="#ffffff"/>\n'
        f'<text x="12" y="28" font-family="Arial, sans-serif" font-size="18" '
        f'font-weight="700">{html.escape(title)}</text>\n'
        '<g font-family="Arial, sans-serif" fill="#1f2933">\n'
        + "\n".join(rows)
        + "\n</g>\n</svg>\n"
    )
    out.write_text(svg, encoding="utf-8")


def write_report(records: list[Record], excluded: list[Excluded]) -> None:
    author_lessons = Counter()
    author_blocks = Counter()
    work_lessons = Counter()
    work_blocks = Counter()
    corpus_lessons = Counter()
    corpus_blocks = Counter()
    grouped: dict[tuple[str, str], list[Record]] = defaultdict(list)
    source_variants: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for record in records:
        author_lessons[record.author] += record.lesson_count
        author_blocks[record.author] += 1
        key = f"{record.author} — {record.work}"
        work_lessons[key] += record.lesson_count
        work_blocks[key] += 1
        corpus_lessons[record.corpus] += record.lesson_count
        corpus_blocks[record.corpus] += 1
        grouped[(record.author, record.work)].append(record)
        source_variants[(record.author, record.work)][record.source] += 1

    bar_svg(author_lessons, "Nichtbiblische Quellen nach Autor", OUT_AUTHOR_SVG)
    bar_svg(work_lessons, "Nichtbiblische Quellen nach Werk", OUT_WORK_SVG)

    lines: list[str] = []
    lines.append("# Nichtbiblische Lesungen mit Quellenangabe im römischen Brevier vor Divino afflatu")
    lines.append("")
    lines.append(f"Erstellt am {date.today().isoformat()} aus `sources/divinum-officium/web/www/horas/Latin`.")
    lines.append("")
    lines.append("## Abgrenzung und Methode")
    lines.append("")
    lines.append("- Ausgewertet wurden die römischen Basisordner `Tempora`, `Sancti` und `Commune`.")
    lines.append("- Das Sanctorale wurde auf die in `Tabulae/Kalendaria/1906.txt` sichtbare Kalenderstufe eingegrenzt, kumulativ über `1570 → 1888 → 1906`.")
    lines.append("- Nicht ausgewertet wurden Ordensfassungen, lokale Anhänge (`aliquibus locis`, `Urbis`) und Votivanhänge.")
    lines.append("- Gezählt werden nur Matutin-Lesungen `[Lectio...]`, in denen eine nichtbiblische Quellenzeile `!…` ausdrücklich steht.")
    lines.append("- Biblische Quellenzeilen, etwa `!2 Reg 12:1-4` oder `!Marc 8:1-9`, wurden ausgeschlossen; bei Evangelienhomilien wurde die nachfolgende patristische Quellenzeile gezählt.")
    lines.append("- `Quellenblöcke` meint eine ausdrücklich genannte Quellenangabe; `Lesungen` zählt den daraus erschlossenen Brevierumfang, also etwa `Lectio7-9` als drei Lesungen.")
    lines.append("- Erkennbar spätere DO-Textschichten, besonders Quellen aus Pius XI/Pius XII oder nach 1906 entstandene universale Feste, wurden aus der Hauptstatistik ausgeschlossen und separat protokolliert.")
    lines.append("- Die Rubriken-/Versionslogik von Divinum Officium wurde nicht vollständig als Kalenderlauf simuliert. Der Befund ist daher eine quellennahe, aber noch manuell kontrollbedürftige Bestandsaufnahme des 1906-nahen römischen Textbestands.")
    lines.append("")
    lines.append("## Gesamtstatistik")
    lines.append("")
    lines.append(f"- Quellenblöcke mit expliziter nichtbiblischer Quelle: **{sum(author_blocks.values())}**")
    lines.append(f"- Daraus erschlossene Einzel-Lesungen: **{sum(author_lessons.values())}**")
    lines.append(f"- Autoren/Autorzeilen nach Normalisierung: **{len(author_blocks)}**")
    lines.append(f"- Autor-Werk-Gruppen nach Normalisierung: **{len(grouped)}**")
    lines.append(f"- Detaildaten: `{OUT_CSV}` und `{OUT_JSON}`")
    lines.append(f"- Ausgeschlossene Quellenzeilen: `{OUT_EXCLUDED_CSV}`")
    lines.append(f"- Grafiken: `{OUT_AUTHOR_SVG}` und `{OUT_WORK_SVG}`")
    lines.append("")
    lines.append("### Nach Korpus")
    lines.append("")
    lines.append("| Korpus | Quellenblöcke | Lesungen |")
    lines.append("|---|---:|---:|")
    for corpus in sorted(corpus_blocks):
        lines.append(f"| {corpus} | {corpus_blocks[corpus]} | {corpus_lessons[corpus]} |")
    lines.append("")
    lines.append("### Ausgeschlossene Quellenzeilen")
    lines.append("")
    excl_by_reason = Counter(e.reason for e in excluded)
    lines.append("| Grund | Zahl |")
    lines.append("|---|---:|")
    for reason, count in excl_by_reason.most_common():
        lines.append(f"| {md_escape(reason)} | {count} |")
    lines.append("")
    lines.append("### Häufigste Autoren")
    lines.append("")
    lines.append("| Autor | Quellenblöcke | Lesungen |")
    lines.append("|---|---:|---:|")
    for author, lessons in author_lessons.most_common(30):
        lines.append(f"| {md_escape(author)} | {author_blocks[author]} | {lessons} |")
    lines.append("")
    lines.append("### Häufigste Werke")
    lines.append("")
    lines.append("| Autor und Werk | Quellenblöcke | Lesungen |")
    lines.append("|---|---:|---:|")
    for key, lessons in work_lessons.most_common(40):
        lines.append(f"| {md_escape(key)} | {work_blocks[key]} | {lessons} |")
    lines.append("")
    lines.append("## Vollständige Übersicht nach Autor und Werk")
    lines.append("")
    lines.append("| Autor | Werk | Quellenblöcke | Lesungen | Quellenvarianten | Belege |")
    lines.append("|---|---|---:|---:|---|---|")
    for (author, work), recs in sorted(grouped.items(), key=lambda item: (strip_accents(item[0][0]).lower(), strip_accents(item[0][1]).lower())):
        block_count = len(recs)
        lesson_count = sum(r.lesson_count for r in recs)
        variants = "; ".join(
            f"{source} ({count}x)"
            for source, count in source_variants[(author, work)].most_common(6)
        )
        if len(source_variants[(author, work)]) > 6:
            variants += "; …"
        examples = "; ".join(link(r) for r in recs[:6])
        if len(recs) > 6:
            examples += "; …"
        lines.append(
            f"| {md_escape(author)} | {md_escape(work)} | {block_count} | {lesson_count} | "
            f"{md_escape(variants)} | {md_escape(examples)} |"
        )
    lines.append("")
    lines.append("## Hinweise zur Weiterarbeit")
    lines.append("")
    lines.append("- Für eine streng datierte Fassung `1906` müsste als nächster Schritt die DO-Rubrikenlogik beziehungsweise ein konkreter Kalenderlauf ausgewertet werden. Das würde vor allem Temporale-Varianten mit `o`-/`r`-Suffixen und Referenzen `@...` noch sauberer auflösen.")
    lines.append("- Die Normalisierung von Werktiteln ist heuristisch. Die CSV bewahrt deshalb immer die originale DO-Quellenzeile (`source`) und die erkannte Autorzeile (`author_line`).")
    lines.append("- Für wissenschaftliche Arbeit sollten die normalisierten Werkgruppen gegen Clavis/CPL, PL/CSEL/CCSL oder BHL-nahe Spezialfälle kontrolliert werden.")
    lines.append("")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "assets").mkdir(parents=True, exist_ok=True)
    records, excluded = scan()
    if not records:
        raise SystemExit("No records found")
    write_csv(records)
    write_excluded_csv(excluded)
    write_json(records)
    write_report(records, excluded)
    print(f"records={len(records)} lessons={sum(r.lesson_count for r in records)}")
    print(f"excluded={len(excluded)}")
    print(OUT_MD)
    print(OUT_CSV)
    print(OUT_AUTHOR_SVG)
    print(OUT_WORK_SVG)


if __name__ == "__main__":
    main()
