# Projektkontext: Divinum Officium Migration

Dieses Dokument fasst den gesamten Kontext unserer bisherigen Zusammenarbeit zusammen.
Es dient als Briefing fuer die Weiterarbeit auf einem anderen Rechner.

## Projektziel

Migration des bestehenden Divinum Officium Projekts (Perl/CGI + Textdateien) zu einer
modernen Architektur:
- **Textdaten**: TEI XML (Text Encoding Initiative)
- **Praezedenzregeln**: YAML-Dateien (statt SQL oder JSON)
- **Webanwendung**: Python + Flask

## Scope-Einschraenkung

Der Nutzer moechte **nicht** alle Rubrik-Versionen migrieren. Konkret:
- **Gewuenscht**: Tridentinische Rubriken (1570, vor 1955)
- **Nicht benoetigt**: Neuerungen nach 1955 (1955er Reform, 1960er Codex Rubricarum)
- **Offen**: Ob Zisterzienser-/Dominikaner-Varianten benoetigt werden

## Entscheidung: Fork vs. Neues Repository

Empfehlung: **Fork des Original-Repositorys** anlegen, weil:
- Tausende sorgfaeltig erfasste Texte als Ausgangsbasis vorhanden
- Git-History und Herkunft der Daten bleiben dokumentiert
- Selektive Migration nur der relevanten Teile (pre-1955)
- Community-Verbindung bleibt erhalten
- Alternative waere ein Import-Skript, das nur relevante Texte extrahiert

## Erarbeitete Dokumente

### Analyse und Uebersicht
| Datei | Inhalt |
|-------|--------|
| `project-overview.md` | Technische Dokumentation des bestehenden Systems (Perl, Datenstruktur, Sonderzeichen @$#!~, Praezedenz-Engine) |
| `json-vs-sql-analysis.md` | Vergleich JSON vs. SQL fuer Praezedenzregeln, Empfehlung: JSON + SQLite Cache Hybrid |

### Datenmodelle
| Datei | Inhalt |
|-------|--------|
| `tei-data-model.md` | Vollstaendige TEI P5 Spezifikation fuer liturgische Texte (Antiphonen, Psalmen, Lesungen, Responsorien). XML-Schema (RelaxNG), Migrations-Mapping |
| `precedence-data-model.md` | SQL-Datenbankschema fuer Praezedenzregeln (erstes Konzept, spaeter durch JSON/YAML ersetzt) |

### Migrationsplanung
| Datei | Inhalt |
|-------|--------|
| `migration-proposal.md` | Umfassender Migrationsplan (5 Phasen, 21-24 Monate, Risikobewertung) |
| `mass-migration-addendum.md` | Ergaenzung zur Migration der Messe (Missa), TEI-Struktur fuer Messpropers |

### Praesentationen
| Datei | Inhalt |
|-------|--------|
| `tei-presentation.md` | 60+ Folien: TEI-Datenmodell Vorschlag |
| `tei-presentation.html` | Interaktive reveal.js Version |
| `json-precedence-presentation.md` | 80+ Folien: JSON-Praezedenzregeln |
| `json-precedence-presentation.html` | Interaktive reveal.js Version |
| `yaml-introduction.md` | 50+ Folien: YAML-Einfuehrung (Syntax, Features, Vergleich mit JSON) |
| `yaml-introduction.html` | Interaktive reveal.js Version |

### Werkzeuge
| Datei | Inhalt |
|-------|--------|
| `convert-presentation.py` | Python-Skript zur Konvertierung von Markdown zu reveal.js HTML. Nutzung: `python3 convert-presentation.py input.md output.html` |

### Datenstruktur-Analysen
| Datei | Inhalt |
|-------|--------|
| `psalmody-data-structure.md` | Detailanalyse der Psalmodie: Psalmen, Cantica, Antiphonen, Zuordnungstabellen, Referenzsystem, Rubrikenvarianten. Grundlage fuer TEI-Migration. (2026-03-09) |

### Dokumentation
| Datei | Inhalt |
|-------|--------|
| `README.md` | Index und Nutzungsanleitung fuer alle Dateien |
| `KONTEXT.md` | Dieses Dokument |

## Entwicklung der Architektur-Entscheidungen

1. **Textformat**: TEI XML wurde als ideal fuer wissenschaftliche/liturgische Texte bewertet
2. **Praezedenzregeln**: SQL -> JSON -> **YAML** (aktuelle Empfehlung)
   - SQL: Zu rigide, schwer versionierbar
   - JSON: Gut, aber keine Kommentare, keine Vererbung (Anchors)
   - YAML: Human-readable, Kommentare, Anchors/Aliases, Git-freundlich
3. **Web-Framework**: Python + Flask (statt Perl CGI)
4. **Scope**: Reduktion auf pre-1955 Rubriken (Tridentinisch)

## Offene Punkte / Naechste Schritte

1. **YAML-Praezedenzregeln**: Vollstaendiges YAML-Schema erstellen (bisher nur Beispiele)
2. ~~**Fork anlegen**~~: Erledigt – Repository `usuale` auf GitLab angelegt
3. **TEI-Schema fuer Psalmodie**: Konkretes TEI-Format fuer Psalmen/Antiphonen festlegen
4. **Prototyp**: Erste TEI-Konvertierung eines Beispieltages
4. **Python-Rule-Engine**: Prototyp fuer YAML-basierte Praezedenzberechnung
5. **Flask-App**: Grundgeruest der Webanwendung
6. **Import-Skript**: Automatische Extraktion der pre-1955 Texte aus dem Original

## Technische Details des Originalprojekts

### Verzeichnisstruktur (Original)
```
web/www/horas/
  Latin/Sancti/     # Heiligenfeste (01-01.txt, 01-02.txt, ...)
  Latin/Tempora/     # Temporale (Adv1-0.txt, Quad1-1.txt, ...)
  Latin/Commune/     # Commune-Texte
  Latin/Psalterium/  # Psalmen, Hymnen
```

### Sonderzeichen in Textdateien
- `@` - Verweis auf andere Datei (@Commune/C1)
- `$` - Rubrik-Anweisung
- `#` - Psalm-Verweis
- `!` - Rubrik in rot
- `~` - Zeilenumbruch innerhalb eines Absatzes
- `_` - Kursiv

### Perl-Hauptdateien
- `horas.pl` - Hauptskript Stundengebet
- `horascommon.pl` - Praezedenzlogik (occurrence(), precedence(), concurrence())
- `missa.pl` - Hauptskript Messe

## Sprache

Der Nutzer kommuniziert auf Deutsch und Englisch.
Die technischen Dokumente sind auf Englisch verfasst.
