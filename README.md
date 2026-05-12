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
├── sources/                     # Git submodules and external source corpora
│   └── divinum-officium/        # DO source corpus (Perl/CGI + text files)
├── data/                        # Normalized and migrated data
│   ├── indexes/                 # TEI index files, including celebrations
│   ├── psalterium/              # Psalms and canticles (TEI XML)
│   ├── offices/                 # Offices and Masses (TEI XML)
│   └── rules/                   # Precedence rules (YAML)
├── tools/                       # Conversion and helper scripts
├── app/                         # Python/Flask web application
└── planning/                    # Planning documents and analyses
```

## Sources

Divinum Officium is included as an external source corpus through a Git
submodule:

```bash
# Initialize submodules after cloning
git submodule update --init --recursive

# Update the DO source corpus
cd sources/divinum-officium
git pull origin master
cd ../..
git add sources/divinum-officium
git commit -m "Update divinum-officium submodule"
```

## License

MIT License. External source corpora retain their own provenance and licensing.
