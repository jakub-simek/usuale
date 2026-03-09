# Usuale

Modernisierung des [Divinum Officium](https://github.com/DivinumOfficium/divinum-officium) Projekts:
Migration der liturgischen Texte und Präzedenzregeln in ein modernes, wissenschaftlich fundiertes Format.

## Architektur

- **Texte**: TEI XML (Text Encoding Initiative, P5)
- **Präzedenzregeln**: YAML
- **Webanwendung**: Python + Flask
- **Cache**: SQLite

## Scope

Tridentinische Rubriken (Breviarium Romanum, vor 1955). Stundengebet und Messe.

## Verzeichnisstruktur

```
usuale/
├── vendor/                      # Git-Submodule (Quellprojekte)
│   └── divinum-officium/        # Originaldaten (Perl/CGI + Textdateien)
├── data/                        # Migrierte Daten
│   ├── psalterium/              # Psalmen und Cantica (TEI XML)
│   ├── offices/                 # Offizien und Messen (TEI XML)
│   └── rules/                   # Präzedenzregeln (YAML)
├── tools/                       # Konvertierungs- und Hilfsskripte
├── app/                         # Python/Flask-Webanwendung
└── planning/                    # Planungsdokumente und Analysen
```

## Submodule

Das Originalprojekt ist als Git-Submodul eingebunden:

```bash
# Nach dem Klonen: Submodule initialisieren
git submodule update --init --recursive

# Submodul auf neuesten Stand bringen
cd vendor/divinum-officium
git pull origin master
cd ../..
git add vendor/divinum-officium
git commit -m "Update divinum-officium submodule"
```

## Lizenz

MIT License (wie das Originalprojekt)
