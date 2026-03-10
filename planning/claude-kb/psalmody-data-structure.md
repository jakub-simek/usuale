# Psalmodie-Datenstruktur im Divinum Officium

## Überblick

Die Psalmodie – Antiphonen und Psalmentexte – ist der musikalisch-textliche Kern des
Stundengebets. Im bestehenden System ist sie über mehrere Verzeichnisse und Dateien
verteilt, die durch ein Referenzsystem miteinander verbunden sind.

Dieses Dokument beschreibt den Ist-Zustand als Grundlage für die TEI-Migration.

**Erstellt**: 2026-03-09
**Basiert auf**: Analyse des Repositorys `usuale` (Fork von DivinumOfficium)

---

## 1. Psalmtexte

### 1.1 Speicherort

```
web/www/horas/Latin/Psalterium/Psalmorum/
```

### 1.2 Dateien

| Bereich | Dateien | Nummerierung | Inhalt |
|---------|---------|--------------|--------|
| Biblische Psalmen | Psalm1.txt – Psalm150.txt | 1–150 | Vulgata-Psalmen (Zählung nach LXX/Vulgata) |
| Laudes-Cantica | Psalm210.txt – Psalm216.txt | 210–216 | Alttestamentliche Cantica für Laudes |
| Laudes-Cantica (Feria) | Psalm220.txt – Psalm226.txt | 220–226 | Cantica für Laudes-Wochentage |
| Evangelische Cantica | Psalm231.txt – Psalm234.txt | 231–234 | Benedictus (231), Magnificat (232), Nunc dimittis (233), Te Deum (234) |
| Matutin-Cantica | Psalm240.txt – Psalm273.txt | 240–273 | Alttestamentliche Cantica für die Matutin |

Insgesamt ca. **200 Dateien**.

### 1.3 Dateiformat der Psalmen

Jede Datei enthält den Volltext eines Psalms, Vers für Vers, eine Zeile pro Vers:

```
109:1a Dixit Dóminus Dómino meo: * Sede a dextris meis:
109:1b Donec ponam inimícos tuos, * scabéllum pedum tuórum.
109:2 Virgam virtútis tuæ emíttet Dóminus ex Sion: * domináre in médio inimicórum tuórum.
```

#### Zeilenformat

```
PSALM:VERS TEXT_ERSTER_HALBVERS * TEXT_ZWEITER_HALBVERS
```

#### Elemente im Detail

| Element | Zeichen | Bedeutung | Beispiel |
|---------|---------|-----------|----------|
| Versreferenz | `109:2` | Psalm:Vers | Psalm 109, Vers 2 |
| Halbvers-Suffix | `1a`, `1b` | Aufteilung langer Verse | `109:1a`, `109:1b` |
| Mediatio | `*` | Hauptpause im Vers (Mitte) | `...meo: * Sede...` |
| Versunterteilung | `‡` (U+2021) | Zusätzliche Verseinteilung (siehe 1.3.1) | `...inaquósa: ‡ sic in sancto...` |
| Flexa (gerendert) | `†` (U+2020) | Sollte in Quelldateien nicht vorkommen (siehe 1.3.1) | |
| Akzente | `á é í ó ú ǽ` | Betonungszeichen für den Vortrag | `Dóminus`, `tuórum` |
| Kreuzzeichen | `+` | Kreuzzeichen bei Benedictus/Magnificat | `Benedíctus + Dóminus` |
| Sektionsmarker | `(Aleph)` | Hebräische Buchstaben in Psalm 118 | `118:1 (Aleph) Beáti...` |

#### 1.3.1 Versunterteilung: ‡ vs. † (Doppelkreuz vs. Kreuz)

In den Quelldateien kommen zwei ähnliche Kreuzzeichen vor, deren Unterschied
in der technischen Dokumentation erklärt wird (siehe `Help/technical.html`):

> *The ‡ symbol is used in the files to demark a verse division which is
> printed as a flexa, i.e., † in the Antiphonale Romanum, Liber Usualis,
> and Breviarum Monasticum but a mediant, i.e. \*, in the Breviarum Romanum.*

**Bedeutung**: Es handelt sich um **eine einzige Verseinteilung**, die je
nach liturgischem Buch verschieden dargestellt wird:

| Kontext | Darstellung von `‡` |
|---------|---------------------|
| Antiphonale Romanum, Liber Usualis, Breviarium Monasticum | `†` (Flexa – kurze Absenkung im Gesang) |
| Breviarium Romanum | `*` (Mediante – wie eine normale Vershälfte) |

Das **kanonische Zeichen in den Quelldateien** ist `‡` (U+2021, Double Dagger).
Die Perl-Engine (`horas.pl`, Funktion `getantcross`) setzt ebenfalls nur
`\x{2021}` und wandelt es bei der Ausgabe je nach gewählter Darstellung um.

Das Zeichen `†` (U+2020, Single Dagger) kommt dennoch in einigen Psalmdateien
direkt vor. Laut Dokumentation sollte es dort nicht stehen – es handelt sich
vermutlich um **Dateninkonsistenzen**, bei denen das Ausgabezeichen statt des
Quellzeichens eingetragen wurde. Bei der TEI-Migration sollten beide Zeichen
einheitlich als Versunterteilung behandelt und normalisiert werden.

### 1.4 Dateiformat der Cantica

Identisch zu den Psalmen, aber mit einer Titelzeile in Klammern:

```
(Canticum Trium Puerorum * Dan 3:57-88,56)
3:57 Benedícite, ómnia ópera Dómini, Dómino: * laudáte et superexaltáte eum in sǽcula.
```

```
(Canticum Zachariæ * Luc. 1:68-79)
1:68 Benedíctus + Dóminus, Deus Israël: * quia visitávit, et fecit redemptiónem plebis suæ:
```

Die Titelzeile enthält:
- Name des Canticums
- `*` als Trenner
- Bibelstellenverweis

### 1.5 Sonderfälle

- **Psalm 118**: Längster Psalm, unterteilt in 22 Sektionen nach hebräischen Buchstaben.
  Wird in den Zuordnungsdateien häufig in Bereichen referenziert: `118(1-16)`, `118(17-32)` etc.
- **Psalm 9**: In der Vulgata ein einziger Psalm, der aber häufig in Teilbereichen
  verwendet wird: `9(2-11)`, `9(12-21)`, `9(22-32)`, `9(33-39)`.
- **Psalm 135**: Wird ebenfalls geteilt: `135(1-9)`, `135(10-26)`.
- **Psalm 143, 144**: Werden je in zwei Hälften geteilt: `143(1-8)`, `143(9-15)`.

---

## 2. Antiphonen

### 2.1 Was sind Antiphonen?

Antiphonen sind kurze liturgische Texte (meist ein Satz), die vor und nach einem Psalm
gesungen werden. Sie geben dem Psalm eine bestimmte theologische Deutung je nach Fest
oder liturgischer Zeit.

### 2.2 Quellen der Antiphonen

Antiphonen werden an **drei Stellen** definiert, in absteigender Priorität:

#### a) Eigentexte in Sancti/Tempora-Dateien (höchste Priorität)

Feste und bestimmte Tage bringen eigene Antiphonen mit:

```
# In Sancti/12-25.txt (Weihnachten):
[Ant Vespera]
Rex pacíficus * magnificátus est, cujus vultum desíderat univérsa terra.;;109
Magnificátus est * Rex pacíficus super omnes reges univérsæ terræ.;;110
```

```
# In Tempora/Adv1-0.txt (1. Adventssonntag):
[Ant Matutinum]
Dóminus dixit * ad me: Fílius meus es tu, ego hódie génui te.;;2
```

#### b) Commune-Texte (mittlere Priorität)

Heilige ohne eigene Texte verweisen auf Commune-Antiphonen:

```
# In Sancti/07-02.txt:
[Ant Vespera]
@Commune/C6:Ant Vespera
```

Die Commune-Dateien (C1.txt – C12.txt) enthalten vollständige Antiphonen-Sätze
für verschiedene Heiligenkategorien.

#### c) Psalterium-Wochenschema (Grundstock, niedrigste Priorität)

```
# In Psalterium/Psalmi/Psalmi major.txt:
[Day0 Vespera]
Dixit Dóminus * Dómino meo: Sede a dextris meis.;;109
Magna ópera Dómini: * exquisíta in omnes voluntátes ejus.;;110
```

Wird verwendet, wenn weder Eigentexte noch Commune-Antiphonen vorliegen
(gewöhnliche Ferientage).

### 2.3 Sektionsnamen für Antiphonen

| Sektion | Hore | Anzahl Antiphonen |
|---------|------|-------------------|
| `[Ant Vespera]` | Vesper | 5 (röm.) / 4 (monast.) |
| `[Ant Laudes]` | Laudes | 5 |
| `[Ant Matutinum]` | Matutin | 9 (3 Nokturnen × 3) oder 12 |
| `[Ant Prima]` | Prim | 1 (+ 3 Psalmen) |
| `[Ant Tertia]` | Terz | 1 (+ 3 Psalmen) |
| `[Ant Sexta]` | Sext | 1 (+ 3 Psalmen) |
| `[Ant Nona]` | Non | 1 (+ 3 Psalmen) |
| `[Ant Completorium]` | Komplet | 1 (+ 3 Psalmen) |
| `[Ant Benedictus]` | Laudes (Benedictus) | 1 |
| `[Ant Magnificat]` | Vesper (Magnificat) | 1 |
| `[Ant Nunc dimittis]` | Komplet (Nunc dimittis) | 1 |

Die Antiphonen für Benedictus, Magnificat und Nunc dimittis stehen separat,
da sie einen eigenen liturgischen Stellenwert haben.

### 2.4 Format einer Antiphon-Zeile

```
Dixit Dóminus * Dómino meo: Sede a dextris meis.;;109
```

#### Bestandteile

| Teil | Beschreibung |
|------|--------------|
| `Dixit Dóminus` | Incipit (Anfang der Antiphon) |
| `*` | Einschnitt/Asteriscus – markiert die Stelle, an der beim Alterniergesang unterbrochen wird |
| `Dómino meo: Sede a dextris meis.` | Fortsetzung des Antiphontextes |
| `;;` | Trennzeichen zum Psalmverweis |
| `109` | Nummer des zugehörigen Psalms |

#### Varianten der Psalmreferenz

| Muster | Bedeutung | Beispiel |
|--------|-----------|----------|
| `;;109` | Ganzer Psalm 109 | Standard |
| `;;135(1-9)` | Psalm 135, Verse 1–9 | Teilpsalm |
| `;;17('36a'-51)` | Psalm 17, Vers 36a bis 51 | Halbvers als Grenze |
| `;;148;149;150` | Psalmen 148, 149, 150 unter einer Antiphon | Laudes-Schlusspsalmen |
| `;;62;66` | Psalm 62 und 66 verbunden | Laudes-Kombination |
| (ohne `;;`) | Antiphon ohne Psalmverweis | Bei Benedictus/Magnificat-Antiphonen |

---

## 3. Psalm-Zuordnungstabellen

### 3.1 Übersicht

```
web/www/horas/Latin/Psalterium/Psalmi/
├── Psalmi major.txt       # Laudes + Vesper
├── Psalmi matutinum.txt   # Matutin
└── Psalmi minor.txt       # Kleine Horen + Komplet
```

### 3.2 Psalmi major.txt – Laudes und Vesper

Organisiert nach Wochentagen (Day0 = Sonntag, Day6 = Samstag).

#### Sektionstypen

| Sektion | Inhalt |
|---------|--------|
| `[Day0 Laudes1]` | Sonntag Laudes, Variante 1: Antiphon + Psalm je Zeile |
| `[Day0 Laudes2]` | Sonntag Laudes, Variante 2: andere Antiphonen, gleiche Psalmen |
| `[Day0 Vespera]` | Sonntag Vesper: 5 Antiphonen + 5 Psalmen |
| `[Daya0 Laudes]` | Kurzform-Antiphonen (a = abbreviata?) |
| `[Daya0 Vespera]` | Kurzform-Vesper-Antiphonen |
| `[Day1 Laudes3]` | Adventsspezifische Laudes-Antiphonen für Montag |
| `[DaymF Laudes]` | Monastische Ferial-Laudes |
| `[DaymP Laudes]` | Monastische Paschal-Laudes |
| `[Monastic Laudes]` | Monastische Laudes je Feria |
| `[Monastic Vespera]` | Monastische Vesper je Feria |
| `[Cistercian Laudes]` | Zisterziensische Laudes |
| `[Cistercian Vespera]` | Zisterziensische Vesper |

#### Psalmverteilung Sonntagsvesper (römisch)

```
Psalm 109 – Dixit Dominus
Psalm 110 – Confitebor tibi
Psalm 111 – Beatus vir
Psalm 112 – Laudate pueri
Psalm 113 – In exitu Israel
```

Dies ist die klassische Sonntagsvesper-Psalmenreihe, die seit dem Mittelalter
unverändert ist.

### 3.3 Psalmi matutinum.txt – Matutin

Organisiert nach Wochentagen. Je Wochentag 3 Nokturnen mit je 3-4 Psalmen,
dazwischen Versikeln (V./R.):

```
[Day0]
Beátus vir * qui in lege Dómini meditátur.;;1
Servíte Dómino * in timóre, et exsultáte ei cum tremóre.;;2
Exsúrge, * Dómine, salvum me fac, Deus meus.;;3
V. Memor fui nocte nóminis tui, Dómine.
R. Et custodívi legem tuam.
Quam admirábile * est nomen tuum, Dómine, in univérsa terra!;;8
...
```

Die Struktur einer Nokturn:
1. 3 Antiphonen mit Psalmen
2. Versikel (V.) und Responsum (R.)
3. (Dann folgen in der eigentlichen Matutin die Lesungen, die aber nicht hier stehen)

#### Sondersektionen

| Sektion | Bedeutung |
|---------|-----------|
| `[Day31]` | Alternative Mittwoch-Matutin (z.B. für bestimmte Rubriken) |
| `[Adv Day0]` | Adventszeit-Matutin für Sonntag |
| `[P Day0]` | Osterzeit-Matutin |

### 3.4 Psalmi minor.txt – Kleine Horen und Komplet

Format: Eine Antiphon pro Hore + 3 Psalmnummern:

```
[Prima]
Dominica = Allelúja, * confitémini Dómino, quóniam in sǽculum misericórdia ejus, allelúja, allelúja.
117,118(1-16),118(17-32)
Feria II = Ínnocens mánibus * et mundo corde ascéndet in montem Dómini.
23,18(2-'7b'),18(8-'15b'),[46]
```

Format je Eintrag:
1. Zeile: `Wochentag = Antiphontext`
2. Zeile: `Psalm1,Psalm2,Psalm3` (kommagetrennt)

Eckige Klammern `[46]` um Psalmnummern bedeuten: Psalm wird nur an bestimmten
Wochentagen (vermutlich Athanasianisches Credo an Sonntagen) oder unter bestimmten
Bedingungen eingefügt.

---

## 4. Spezialzuordnungen

### 4.1 Speicherort

```
web/www/horas/Latin/Psalterium/Special/
├── Major Special.txt      # 53 KB – Spezial für Laudes/Vesper
├── Matutinum Special.txt  # 23 KB – Spezial für Matutin
├── Minor Special.txt      # 24 KB – Spezial für kleine Horen
├── Prima Special.txt      #  4 KB – Spezial für Prim
└── Preces.txt             # 14 KB – Preces (Bittgebete)
```

### 4.2 Funktion

Diese Dateien enthalten **saisonale und festtagsbezogene Überschreibungen**
der Standard-Psalmodie. Sie werden von der Perl-Engine konsultiert, wenn
bestimmte liturgische Zeiten oder Feste vorliegen.

Beispiel aus Major Special.txt:

```
[Dominica Laudes]
!Apo 7:12
v. Benedíctio, et cláritas, et sapiéntia...
```

```
[Hymnus Day0 Laudes]
{:H-Ecceiamnoctis:}v. Ecce, jam noctis tenuátur umbra...
```

Die Special-Dateien enthalten neben Psalmzuordnungen auch Hymnen, Versikel,
Kapiteln und kurze Responsorien – also alles, was im Psalterium-Rahmen
saisonabhängig variiert.

---

## 5. Steuerungsmechanismen

### 5.1 Die [Rule]-Sektion

In jeder Office-Datei (Sancti, Tempora, Commune) steuert die `[Rule]`-Sektion,
wie die Psalmodie zusammengebaut wird:

| Direktive | Bedeutung |
|-----------|-----------|
| `Psalmi Dominica` | Verwende Sonntagspsalmen (statt Ferialpsalmen) |
| `Antiphonas horas` | Wende die Vesper-/Laudes-Antiphonen auch auf kleine Horen an |
| `Psalm5 Vespera=116` | Ersetze den 5. Vesperpsalm durch Psalm 116 |
| `Psalm5 Vespera3=113` | Ersetze den 5. Psalm der 3. Vesper-Variante |
| `9 lectiones` | 9 Lesungen → 3 Nokturnen in der Matutin |
| `3 lectiones` | 3 Lesungen → 1 Nokturn in der Matutin |

### 5.2 Referenzsystem (@)

Das `@`-Zeichen erstellt Querverweise zwischen Dateien und Sektionen:

| Muster | Bedeutung |
|--------|-----------|
| `@Commune/C1:Ant Vespera` | Hole Sektion `[Ant Vespera]` aus `Commune/C1.txt` |
| `@Sancti/12-25:Versum 2` | Hole Sektion `[Versum 2]` aus `Sancti/12-25.txt` |
| `@:Ant Laudes` | Hole Sektion `[Ant Laudes]` aus der aktuellen Datei |
| `@Psalterium/Special/Major Special:Adv Versum 3` | Hole Sektion aus Special-Datei |

### 5.3 Substitutionsmechanismus

Referenzen können mit sed-artigen Substitutionen kombiniert werden:

```
@:Ant Vespera:s/;;.*//g
```
→ Kopiere Ant Vespera, entferne alle Psalmreferenzen

```
@:Hymnus Laudes:s/auctor/Auctor/ s/almo/Sancto/
```
→ Kopiere Hymnus Laudes mit Textersetzungen

```
@:DaymF Laudes:s/92/50/ s/99/117/
```
→ Kopiere monastische Ferial-Laudes, ersetze Psalm 92 durch 50, Psalm 99 durch 117

Dieses System ermöglicht eine kompakte Darstellung von Varianten, ist aber
für maschinelle Verarbeitung komplex.

---

## 6. Rubrikenvarianten

### 6.1 Römisch (Standard)

Die Standardverteilung der Psalmen folgt der mittelalterlichen römischen Tradition:
- **Laudes**: 5 Psalmen (inkl. Canticum) + Laudate-Psalmen
- **Vesper**: 5 Psalmen
- **Matutin**: 9 oder 12 Psalmen (3 Nokturnen)
- **Kleine Horen**: je 3 Psalmen (hauptsächlich Psalm 118)
- **Komplet**: 3 Psalmen

### 6.2 Monastisch

Separate Sektionen in den Zuordnungsdateien:
- `[Monastic Laudes]`, `[Monastic Vespera]`
- Andere Psalmverteilung (z.B. 4 Vesperpsalmen statt 5)
- Ganze Psalterrezitation in einer Woche

### 6.3 Zisterziensisch

Basiert auf der monastischen Tradition mit eigenen Abweichungen:
- `[Cistercian Laudes]`, `[Cistercian Vespera]`
- Oft definiert durch Referenz auf monastische Sektionen mit Modifikationen

### 6.4 Dominikanisch

Eigene Sektionen und eigene Verzeichnisse:
- `TemporaOP/`, `SanctiOP/` für dominikanische Eigentexte
- In Zuordnungsdateien durch Rubrikenbedingungen gesteuert

### 6.5 Rubrikenbedingungen in den Texten

```
(sed rubrica 1960)           → nur für 1960er Rubriken
(rubrica tridentina)         → nur für tridentinische Rubriken
(rubrica cisterciensis)      → nur für Zisterzienser
(nisi rubrica praedicatorum) → nicht für Dominikaner
(sed tempore paschali)       → nur in der Osterzeit
```

---

## 7. Doxologien

### 7.1 Speicherort

```
web/www/horas/Latin/Psalterium/Doxologies.txt
```

### 7.2 Funktion

Enthält saisonabhängige Varianten der Schlussdoxologie (Gloria-Patri-Strophe),
die am Ende von Hymnen je nach liturgischer Zeit variiert:

| Sektion | Liturgische Zeit | Schlüsseltext |
|---------|-----------------|---------------|
| `[Nat]` / `[NatT]` | Weihnachten | *Qui natus es de Vírgine* |
| `[Epi]` / `[EpiT]` | Epiphanie | *Qui apparuísti Géntibus* |
| `[Pasch]` / `[PaschT]` | Ostern | *qui a mórtuis surréxit* |
| `[Asc]` / `[AscT]` | Himmelfahrt | *Qui victor in cælum redis* |
| `[Pent]` / `[PentT]` | Pfingsten | Variante mit Paraklet |
| `[Heart]` / `[HeartT]` | Herz Jesu | *Qui Corde fundis grátiam* |

Die Suffixe ohne/mit `T` bezeichnen zwei verschiedene Hymnenfamilien
(vermutlich Prä-/Post-Urban VIII Hymnenreform).

---

## 8. Zusammenfassung für die TEI-Migration

### 8.1 Zu migrierende Datentypen

| Datentyp | Anzahl | Quelle | Priorität |
|----------|--------|--------|-----------|
| Psalmtexte (Vulgata) | 150 | Psalmorum/ | Hoch |
| Cantica (bibl.) | ~50 | Psalmorum/ (210+) | Hoch |
| Wochenantiphonen (Laudes/Vesper) | ~7×10 = 70 | Psalmi major.txt | Hoch |
| Wochenantiphonen (Matutin) | ~7×12 = 84 | Psalmi matutinum.txt | Hoch |
| Wochenantiphonen (Kleine Horen) | ~7×5 = 35 | Psalmi minor.txt | Hoch |
| Festantiphonen | ~1000+ | Sancti/, Tempora/ | Mittel (mit Office) |
| Commune-Antiphonen | ~120 | Commune/ | Mittel |
| Saisonale Sondertexte | ~200+ | Special/ | Mittel |
| Doxologien | ~12 | Doxologies.txt | Niedrig |

### 8.2 Herausforderungen

1. **Referenzsystem**: Das `@`-basierte System mit sed-Substitutionen muss
   in TEI in explizite Verweise oder aufgelöste Texte überführt werden.

2. **Rubrikenvarianten**: Monastische, zisterziensische und dominikanische
   Varianten müssen entweder als separate TEI-Dateien oder als Varianten
   innerhalb eines Dokuments kodiert werden.

3. **Scope-Entscheidung**: Nur tridentinische (pre-1955) Rubriken werden
   migriert – monastische/dominikanische Varianten sind optional.

4. **Psalmteilungen**: Das System der Psalmverse-Bereiche (z.B. `135(1-9)`)
   muss in TEI-Verweise übersetzt werden, die auf Versebene selektieren können.

5. **Antiphon-Psalm-Bindung**: Die `;;`-Verknüpfung muss in ein semantisches
   TEI-Modell überführt werden, das die Beziehung Antiphon→Psalm ausdrückt.

---

## Anhang: Nummerierungsschema der Cantica

| Nummernbereich | Hore | Inhalt |
|----------------|------|--------|
| 210 | Laudes (So.) | Canticum Trium Puerorum (Dan 3:57-88) |
| 211–216 | Laudes (Mo.–Sa.) | Wochentags-Cantica (Isa, Eccli, 1 Sam, Hab, Deut, Jer) |
| 220 | Laudes (So.) alt. | Dan 3:52-57 |
| 221–226 | Laudes (Mo.–Sa.) alt. | Alternative Wochentags-Cantica |
| 231 | Laudes | Benedictus (Luc 1:68-79) |
| 232 | Vesper | Magnificat (Luc 1:46-55) |
| 233 | Komplet | Nunc dimittis (Luc 2:29-32) |
| 234 | Matutin | Te Deum laudamus |
| 240–273 | Matutin | AT-Cantica für Matutin-Nokturnen |
