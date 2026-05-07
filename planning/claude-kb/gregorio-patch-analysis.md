# Gregorio-Patch-Analyse: Zusammenfuehrung NR-Patch mit Upstream v6.2.0-beta1

**Datum**: 2026-03-13
**Zweck**: Dokumentation der Unterschiede zwischen dem offiziellen Gregorio-Paket und dem Nocturnale-Romanum-Patch, als Grundlage fuer eine Zusammenfuehrung.

---

## Hintergrund

Das TeX-Paket [Gregorio](https://github.com/gregorio-project/gregorio) setzt gregorianische Choralnotation (GABC-Format). Fuer das Projekt *usuale* sollen zwei Dinge kombiniert werden:

1. **Upstream v6.2.0-beta1** — die neueste offizielle Version mit Bugfixes und NABC-Verbesserungen
2. **Nocturnale-Romanum-Patch** ([GitHub](https://github.com/Nocturnale-Romanum/gregorio-patch)) — eine Erweiterung, die eckige Klammern in der NABC-Schicht (adiastematische St.-Galler-Neumen) sowie zusaetzliche Neumen-Glyphen hinzufuegt

Der NR-Patch basiert auf Gregorio v6.1.0 und betrifft zwei Dateien:
- `gregoriotex-nabc.lua` (Lua-Parser fuer NABC-Notation)
- `gregall.ttf` (St.-Galler-Neumen-Schrift, kompiliert aus `gregall.sfd`)

---

## 1. gregoriotex-nabc.lua

### Dateiuebersicht

| Eigenschaft | v6.1.0 | v6.2.0-beta1 | NR-Patch |
|---|---|---|---|
| Zeilenanzahl | 469 | 469 | 470 |
| Versionsstring | `6.1.0` | `6.2.0-beta1` | `6.1.0` |
| Basis | — | v6.1.0 | v6.1.0 |

Alle drei Versionen definieren dieselben 9 Funktionen:

| Funktion | Zeile (v6.1.0) |
|---|---|
| `gregallreadfont(fontname, font_id)` | 74 |
| `gregallparse_base(str, idx, len)` | 121 |
| `gregallparse_neume(str, idx, len)` | 158 |
| `add_ls(base, pre, post, ls, position, ...)` | 214 |
| `add_spacing(str, len, idx, ret)` | 275 |
| `gregallparse_neumes(str, kind, scale)` | 294 |
| `l.try(kind, base, parts, pp, su, ls5, ls)` | 330 (innerhalb `gregallparse_neumes`) |
| `init_font(fontname)` | 456 |
| `print_nabc(nabc)` | 462 |

### Aenderungen: v6.1.0 → v6.2.0-beta1 (Upstream)

**5 geaenderte Zeilen**, alle minimal:

1. **Zeile 23 — Versionsnummer**:
   ```lua
   -- alt:  -- GREGORIO_VERSION 6.1.0
   -- neu:  -- GREGORIO_VERSION 6.2.0-beta1
   ```

2. **Zeilen 278, 281, 284, 287 — Trailing Space in `add_spacing()`**:
   Jede der vier `\gre@hskip`-Strings erhaelt ein abschliessendes Leerzeichen. Dies ist ein TeX-Tokenisierungs-Bugfix (verhindert, dass TeX den naechsten Buchstaben als Teil des Makronamens interpretiert).

   ```lua
   -- Zeile 278
   -- alt:  ret = ret .. "\\gre@hskip \\gre@space@skip@nabclargerspace"
   -- neu:  ret = ret .. "\\gre@hskip \\gre@space@skip@nabclargerspace "

   -- Zeile 281
   -- alt:  ret = ret .. "\\gre@hskip -\\gre@space@skip@nabclargerspace"
   -- neu:  ret = ret .. "\\gre@hskip -\\gre@space@skip@nabclargerspace "

   -- Zeile 284
   -- alt:  ret = ret .. "\\gre@hskip \\gre@space@skip@nabcinterelementspace"
   -- neu:  ret = ret .. "\\gre@hskip \\gre@space@skip@nabcinterelementspace "

   -- Zeile 287
   -- alt:  ret = ret .. "\\gre@hskip -\\gre@space@skip@nabcinterelementspace"
   -- neu:  ret = ret .. "\\gre@hskip -\\gre@space@skip@nabcinterelementspace "
   ```

### Aenderungen: v6.1.0 → NR-Patch

**2 Aenderungen**, ebenfalls minimal:

1. **Nach Zeile 3 — Warnkommentar eingefuegt**:
   ```lua
   --WARNING: this file is a patched version within the scope of the NR Project. Use only if you know what you are doing.
   ```

2. **Zeile 111/112 — Zwei neue Neumen-Typen in `gregallneumekinds`**:
   ```lua
   -- alt:  un = 1, oc = 1, ni = 1 }
   -- neu:  un = 1, oc = 1, ni = 1, ob = 1, cb = 1 }
   ```
   `ob` = open bracket (eckige Klammer auf), `cb` = close bracket (eckige Klammer zu).

### Konfliktanalyse

| Aenderung | Upstream v6.2.0-beta1 | NR-Patch | Konflikt? |
|---|---|---|---|
| Versionsstring (Z. 23) | geaendert | unveraendert | Nein |
| Warnkommentar (nach Z. 3) | — | eingefuegt | Nein |
| `gregallneumekinds` (Z. 111) | unveraendert | `ob`, `cb` ergaenzt | Nein |
| `add_spacing()` (Z. 278–287) | Trailing Space | unveraendert | Nein |

**Ergebnis: Kein Konflikt.** Die Aenderungen betreffen komplett verschiedene Stellen.

### Merge-Anleitung

Ausgehend von v6.2.0-beta1:
1. Warnkommentar nach Zeile 3 einfuegen
2. `, ob = 1, cb = 1` zur `gregallneumekinds`-Tabelle hinzufuegen (Zeile 111)

Fertig — alle anderen Aenderungen (Versionsnummer, Trailing-Space-Fix) sind bereits in v6.2.0-beta1 enthalten.

---

## 2. gregall.sfd / gregall.ttf (St.-Galler-Neumen-Schrift)

### Ueberblick

| Eigenschaft | v6.0.0 | v6.1.0 | v6.2.0-beta1 | NR-Patch |
|---|---|---|---|---|
| Glyphenanzahl | 563 | 603 | 603 | 607 |
| Format im Repo | .sfd | .sfd | .sfd | .ttf (kompiliert) |
| Aenderung ggue. Vorgaenger | — | +40 Glyphen | nur Copyright-Update | +44 ggue. v6.0.0 |

### Gemeinsame Basis: U+E65F bis U+E67D

Upstream v6.1.0 und der NR-Patch fuegen beide Glyphen ab Codepoint U+E65F hinzu. Bis einschliesslich **U+E67D** (31 Glyphen) sind sie **identisch** — dieselben Glyphen an denselben Codepoints.

### Codepoint-Konflikte: U+E67E bis U+E686

Ab U+E67E divergieren die Zuordnungen. Die Ursache: Der NR-Patch hat `ob` und `cb` (Klammern) bei U+E67E und U+E67F eingefuegt und damit die restlichen Glyphen um 2 Positionen verschoben.

| Codepoint | Upstream v6.1.0+ | NR-Patch | Konflikt-Typ |
|---|---|---|---|
| U+E67E | `pqSN` | **`ob`** | NR-exklusiv verdraengt Upstream |
| U+E67F | `qlEclB1` | **`cb`** | NR-exklusiv verdraengt Upstream |
| U+E680 | `qlNppt1sut2su1` | `toSEclNlsi8` | Verschiebung |
| U+E681 | `qlNsut2su1` | `toSEclN` | Verschiebung |
| U+E682 | `toEclB` | `toSEcl` | Verschiebung |
| U+E683 | `toSEclNlsi8` | `qlNppt1sut2su1` | Verschiebung |
| U+E684 | `toSEclN` | `toEclB` | Verschiebung |
| U+E685 | `toSEcllsi8` | `pqSN` | Verschiebung |
| U+E686 | `toSEcl` | `qlEclB1` | Verschiebung |

7 dieser 9 Konflikte sind **dieselben Glyphen an verschiedenen Codepoints** (reine Verschiebung). 2 sind NR-exklusive Glyphen (`ob`, `cb`), die Upstream-Glyphen verdraengt haben.

### NR-exklusive Glyphen (nicht in Upstream)

| Glyphenname | NR-Codepoint | Beschreibung |
|---|---|---|
| `ob` | U+E67E | Open Bracket (eckige Klammer auf) |
| `cb` | U+E67F | Close Bracket (eckige Klammer zu) |
| `qlEclS1` | U+E687 | Quilisma-Clivis-Variante |
| `pfEpi` | U+E688 | Pressus-Verbindung |
| `toEpisu1` | U+E689 | Torculus-Verbindung |
| `pisux1` | U+E68A | Punctum-inclinatum-Variante |

### Im NR-Patch fehlende Upstream-Glyphen

| Glyphenname | Upstream-Codepoint |
|---|---|
| `qlNsut2su1` | U+E681 |
| `toSEcllsi8` | U+E685 |

### Aenderung v6.1.0 → v6.2.0-beta1

Nur ein Copyright-Update (2025 → 2026) in `gregall.sfd`. **Keine neuen Glyphen.**

### Merge-Anleitung

Ausgehend von der Upstream-v6.2.0-beta1 `gregall.sfd`:

1. **Upstream-Codepoints beibehalten** (U+E67E–U+E686 bleiben wie im Original)
2. **6 NR-exklusive Glyphen an neuen, freien Codepoints einfuegen:**

   | Glyphenname | Neuer Codepoint (Vorschlag) |
   |---|---|
   | `ob` | U+E687 |
   | `cb` | U+E688 |
   | `qlEclS1` | U+E689 |
   | `pfEpi` | U+E68A |
   | `toEpisu1` | U+E68B |
   | `pisux1` | U+E68C |

3. **`.ttf` neu kompilieren** (erfordert FontForge)
4. **Codepoints in `gregoriotex-nabc.lua` anpassen**: Die Lua-Datei referenziert Glyphen ueber die Font-Tabelle (`init_nabc_font`), die Glyphennamen auf Codepoints mappt. Da die Glyphennamen gleich bleiben und FontForge die Zuordnung Name → Codepoint im Font speichert, sollte die Zuordnung automatisch stimmen — sofern die Glyphennamen in der `.sfd` korrekt gesetzt sind.

### Werkzeuge

- **FontForge** (GUI oder Python-Scripting-API) zum Bearbeiten der `.sfd` und Kompilieren der `.ttf`
- Installation: `brew install fontforge`
- Scripting-Beispiel:
  ```python
  import fontforge
  # NR-Glyphen aus NR-ttf extrahieren
  nr_font = fontforge.open("gregall-nr.ttf")
  # Upstream-sfd oeffnen
  upstream_font = fontforge.open("gregall.sfd")
  # Glyphen kopieren und an neuen Codepoints einfuegen
  # ...
  upstream_font.generate("gregall.ttf")
  ```

---

## 3. Zusammenfassung

### Aufwand

| Datei | Schwierigkeit | Konfliktrisiko |
|---|---|---|
| `gregoriotex-nabc.lua` | Trivial (2 Zeilen aendern) | Keines |
| `gregall.sfd/.ttf` | Mittel (Font-Bearbeitung + Kompilierung) | Hoch (Codepoint-Konflikte) |

### Abhaengigkeit zwischen den Dateien

Die Lua-Datei und die Schrift muessen konsistent sein:
- Die Glyphennamen in der `.sfd`/`.ttf` muessen den Bezeichnern entsprechen, die `gregoriotex-nabc.lua` erwartet
- Neue Neumen-Typen (`ob`, `cb`) muessen sowohl in der `gregallneumekinds`-Tabelle (Lua) als auch als Glyphen in der Schrift vorhanden sein
- Die Codepoint-Zuordnung geschieht ueber die Font-Tabelle — nicht hartcodiert in der Lua-Datei

### Empfohlene Reihenfolge

1. Font zusammenfuehren (`.sfd` bearbeiten, `.ttf` kompilieren)
2. Lua-Datei mergen (2 Zeilen auf Basis von v6.2.0-beta1 aendern)
3. Testen mit einem GABC-Beispiel, das NABC-Klammern verwendet

---

**Quellen**:
- Upstream: https://github.com/gregorio-project/gregorio (Tag: v6.2.0-beta1)
- NR-Patch: https://github.com/Nocturnale-Romanum/gregorio-patch (Branch: main)
