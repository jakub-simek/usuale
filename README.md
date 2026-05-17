# Usuale

Usuale is an independent project for the scholarly description, normalization,
and digital use of traditional liturgical texts. It develops its own data
models for liturgical celebrations, texts, calendars, precedence rules, and
companion meditations.

Data from [Divinum Officium](https://github.com/DivinumOfficium/divinum-officium)
is used as an important source corpus, but it does not define this project's
identity.

## Architecture

- **Texts**: TEI XML (Text Encoding Initiative, P5)
- **Precedence rules**: YAML
- **Web application**: Python + Flask
- **Cache**: SQLite

## Scope

Tridentine rubrics (Breviarium Romanum, pre-1955), Divine Office, and Mass.

## Directory Structure

```
usuale/
├── shared/                      # Shared guidelines and cross-project assets
│   └── latin-meditations-guidelines/
├── sources/                     # External source corpora
│   └── divinum-officium/        # DO source corpus (Perl/CGI + text files)
├── data/                        # Normalized and migrated data
│   ├── indexes/                 # TEI index files, including celebrations
│   ├── psalterium/              # Psalms and canticles (TEI XML)
│   ├── offices/                 # Offices and Masses (TEI XML)
│   └── rules/                   # Precedence rules (YAML)
├── tools/                       # Conversion and helper scripts
├── skills/                      # Codex/ChatGPT skills for repo-specific work
├── app/                         # Python/Flask web application
└── planning/                    # Planning documents and analyses
```

## Sources

Divinum Officium and the shared Latin meditation guidelines are included through
Git submodules:

```bash
# Initialize submodules after cloning
git submodule update --init --recursive

# Update the shared meditation guidelines
cd shared/latin-meditations-guidelines
git pull origin main
cd ../..
git add shared/latin-meditations-guidelines
git commit -m "Update shared meditation guidelines"

# Update the DO source corpus
cd sources/divinum-officium
git pull origin master
cd ../..
git add sources/divinum-officium
git commit -m "Update divinum-officium submodule"
```

## Generated Indexes

The TEI register of liturgical celebrations is generated from the Divinum
Officium source corpus:

```bash
tools/extract_celebrations.py
```

This writes:

- `data/indexes/celebrations.xml`: the heiEDITIONS-compatible TEI subject index
- `data/indexes/celebrations-review.tsv`: sources that could not yet be mapped
  automatically to a celebration

The review TSV is an editorial control file. An entry there is not necessarily
an error; many rows are source fragments, appendices, or redirect files that
require later modeling decisions.

## Repo Skills

Repo-specific Codex/ChatGPT skills live in `skills/`. The current meditation
workflow is a project adapter for the shared Latin meditation guidelines:

```text
skills/latin-liturgical-meditations/SKILL.md
shared/latin-meditations-guidelines/skills/latin-meditations-core/SKILL.md
```

When starting a chat task about writing, revising, reviewing, or adding metadata
to a meditation, refer to the skill by name:

```text
Use latin-liturgical-meditations and write a meditation on the Introit ...
```

Other useful prompts:

```text
Use latin-liturgical-meditations and add the YAML front matter.
Use latin-liturgical-meditations and run a final review against the guidelines.
Use latin-liturgical-meditations and check the citations and cf. references.
```

The skill is only an operational entry point. The authoritative rules remain in
the shared submodule plus the local Usuale overlay:

```text
shared/latin-meditations-guidelines/guidelines/
planning/meditations-guidelines.md
```

## License

MIT License. External source corpora retain their own provenance and licensing.
