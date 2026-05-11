# Planung: Datenmodell fuer eine Neuauflage von Divinum Officium

Stand: 2026-05-11

Diese Notiz fasst die bisherigen Ueberlegungen zum Datenmodell zusammen. Sie
geht von den Daten des bestehenden Divinum Officium aus, zielt aber auf eine
sauberere Normalisierung fuer ein eigenes System, in dem liturgische Texte,
Messe, Officium, Kalender und Meditationen miteinander verknuepft werden
koennen.

## Ausgangspunkt im bestehenden DO-Modell

Divinum Officium ist primaer ein file- und regelbasiertes System. Ein
liturgischer Tag erscheint nicht als zentrale eigenstaendige Entitaet, sondern
als Dateischluessel mit Textdateien und Rubriken.

Beispiel:

- `horas/Latin/Tempora/Pasc5-0.txt`
- `missa/Latin/Tempora/Pasc5-0.txt`

Beide Dateien enthalten den Titel `Dominica V Post Pascha`, aber es gibt keine
separate, zentrale Entitaet `Dominica V Post Pascha`, auf die Messe und Officium
gemeinsam verweisen.

Das bestehende Modell waehlt fuer ein Datum einen Temporal- oder Sanctoral-Key,
laedt die zugehoerigen Dateien und loest Regeln, Occurrence, Concurrence,
Kommemorationen, Transfers und Querverweise.

## Bedeutung der Temporal-Keys

Temporal-Keys wie `Pasc5-0` sind zusammengesetzt:

```text
Pasc5-0
|    |
|    +-- Wochentag: 0 = Sonntag
+------- Zeit-/Wochenkey: Pasc5 = fuenfte Woche der Osterzeit nach DO-Zaehllogik
```

Die Wochentagskodierung ist:

```text
0 = Sonntag
1 = Montag
2 = Dienstag
3 = Mittwoch
4 = Donnerstag
5 = Freitag
6 = Samstag
```

Fuer ein eigenes Modell sollte dieser Key daher nicht als undurchsichtiger
String behandelt werden. Sinnvoll ist eine Zerlegung in:

```yaml
temporal_key: Pasc5-0
season: paschaltide
week_index: 5
weekday: 0
```

## Problem der Sanctorale-Keys

Sanctorale-Dateien sind im bestehenden DO-Modell stark datumsgesteuert:

```text
Sancti/03-21.txt
Sancti/01-08.txt
```

Das ist praktisch fuer einen bestimmten Kalenderstand, aber als stabile
Identitaet eines Festes problematisch. Ein Key wie `03-21` bedeutet zunaechst
nur: An diesem Datum steht in diesem Kalender eine Feier. Er sagt nicht
inhaltlich, welches Fest oder welcher Heilige gemeint ist.

Fuer historisch bewegliche Kalender ist das ein Nachteil. Wenn ein Fest in
verschiedenen Kalendern oder Rubrikstaenden auf verschiedene Daten faellt,
sollte die Identitaet des Festes stabil bleiben.

## Zentrale Modellentscheidung

Das eigene System sollte trennen zwischen:

```text
celebration
= die liturgische Feier als inhaltliche Entitaet

calendar_assignment
= die Eintragung dieser Feier in einem konkreten Kalender an einem Datum

occurrence
= das konkrete Auftreten dieser Feier an einem wirklichen Datum in einem Jahr
```

Beispiel fuer ein Heiligenfest:

```yaml
celebration:
  id: sancti:benedictus-abbas
  title: S. Benedicti Abbatis
  subject_id: person:benedictus-nursiae
  kind: saint

calendar_assignment:
  calendar_id: roman-general
  celebration_id: sancti:benedictus-abbas
  date: 03-21
  rank: duplex_majus
```

Bei einem historisch verschobenen Fest koennen mehrere Kalenderzuordnungen auf
dieselbe Feier zeigen:

```yaml
calendar_assignment:
  calendar_id: roman-general-1960
  celebration_id: sancti:thomas-aquinas
  date: 03-07

calendar_assignment:
  calendar_id: roman-general-1970
  celebration_id: sancti:thomas-aquinas
  date: 01-28
```

## Celebration als gemeinsame Klammer fuer Messe und Officium

Fuer Meditationen ist wichtig, dass ein liturgischer Tag gleichzeitig Messe und
Officium umfasst. Deshalb braucht das eigene Modell eine gemeinsame
`celebration`-Entitaet, unter der die verschiedenen liturgischen Formen haengen.

Beispiel:

```yaml
celebration:
  id: tempora:pasc5-0
  title: Dominica V Post Pascha
  cycle: temporale
  temporal_key: Pasc5-0
  season: paschaltide
  weekday: 0

liturgical_form:
  id: missa:tempora:pasc5-0
  celebration_id: tempora:pasc5-0
  form: missa
  source_path: vendor/divinum-officium/web/www/missa/Latin/Tempora/Pasc5-0.txt

liturgical_form:
  id: officium:tempora:pasc5-0
  celebration_id: tempora:pasc5-0
  form: officium
  source_path: vendor/divinum-officium/web/www/horas/Latin/Tempora/Pasc5-0.txt
```

So kann eine Meditation ueber den Introitus zugleich den Kontext von Epistel,
Evangelium und Officium beruecksichtigen.

## Textmodell

Das bestehende DO-Modell mischt inline gespeicherte Texte und Querverweise.
Manche Texte stehen direkt in einer Officiums- oder Messdatei; andere werden
per `@Tempora/...:Section` referenziert.

Fuer ein eigenes Modell waere eine Normalisierung sinnvoll:

```text
text_unit
= der liturgische Text als wiederverwendbare Einheit

source_witness
= eine konkrete Fassung dieses Textes in einer Quelle

usage
= die Verwendung eines Textes an einer Stelle einer Messe oder eines Officiums
```

Beispiel:

```yaml
text_unit:
  id: introitus:vocem-iucunditatis
  genre: introitus
  incipit: Vocem iucunditatis

usage:
  id: missa:tempora:pasc5-0:introitus
  celebration_id: tempora:pasc5-0
  form_id: missa:tempora:pasc5-0
  section: Introitus
  text_id: introitus:vocem-iucunditatis
```

Wichtig ist, bei mehrfach bezeugten oder leicht variierenden Texten nicht zu
aggressiv zu deduplizieren. Sinnvoll ist eine Unterscheidung:

```text
text_family
= der wiedererkennbare liturgische Text als konzeptionelle Einheit

text_witness
= die konkrete Fassung in einer bestimmten Quelle, Sprache, Orthographie oder
   Rubrikversion

usage
= die konkrete liturgische Verwendung
```

## Querverweise und Provenienz

Wenn DO einen Text per Querverweis laedt, sollte das eigene Modell zwei Ebenen
festhalten:

```yaml
source_declared:
  path: missa/Latin/Tempora/Pasc5-0.txt
  section: Secreta

source_resolved:
  path: missa/Latin/Tempora/Pasc0-2.txt
  section: Secreta
```

So bleibt sichtbar:

- wo der Text im konkreten Formular aufgerufen wurde
- woher der tatsaechliche Wortlaut stammt
- ob mehrere Formulare denselben Text verwenden

## Meditationen im Datenmodell

Eine Meditation sollte nicht nur an einem Dateipfad haengen. Sie sollte einen
primaeren liturgischen Text haben und zugleich ihren liturgischen Kontext
angeben koennen.

Beispiel:

```yaml
meditation:
  id: meditatio:vocem-iucunditatis
  title: Meditatio de Introitu Dominicae V Post Pascha
  primary_usage: missa:tempora:pasc5-0:introitus
  primary_text: introitus:vocem-iucunditatis
  celebration_id: tempora:pasc5-0
  contextual_usages:
    - missa:tempora:pasc5-0:epistola
    - missa:tempora:pasc5-0:evangelium
    - officium:tempora:pasc5-0:lectiones
```

Dadurch ist moeglich:

- Meditationen ueber denselben Text bei verschiedenen Verwendungen zu erkennen
- den Kontext eines bestimmten Tages zu beruecksichtigen
- Wiederholungen zwischen mehreren Meditationen desselben Tages zu vermeiden
- Texte aus Messe und Officium gemeinsam auszuwerten

## Extraktion aus DO-Daten

Aus DO laesst sich eine erste Liste von `celebrations` extrahieren, aber nicht
als endgueltige Wahrheit, sondern als importierter Katalog.

Statische Extraktion:

- `missa/Latin/Tempora/*.txt`
- `horas/Latin/Tempora/*.txt`
- `missa/Latin/Sancti/*.txt`
- `horas/Latin/Sancti/*.txt`

Zu lesen waeren besonders:

- `[Officium]`
- `[Rank]`
- `[Rule]`
- Querverweise mit `@...`

Dabei muessen Varianten klassifiziert werden:

```text
Pasc5-0    kanonischer Temporal-Tag
Pasc5-0t   Variante oder versionsspezifische Ersatzdatei
Pasc5-1    Feria
Pasc5-1r   rubrikale/reformbezogene Variante
```

Neben dem statischen Katalog braucht es einen dynamischen Kalenderindex, der
fuer ein konkretes Jahr, eine Rubrikversion und ggf. einen lokalen Kalender
berechnet:

- welche Feier gewinnt
- welche Messe genommen wird
- welches Officium genommen wird
- welche Kommemorationen auftreten
- welche Transfers gelten
- welche DO-Variante tatsaechlich geladen wird

## Empfohlene Kernentitaeten

```text
calendar
calendar_assignment
celebration
liturgical_form
text_family
text_witness
usage
source_witness
occurrence
meditation
person / mystery / event
```

`celebration` sollte neutral benannt werden, nicht `feast`, weil das Modell
auch Sonntage, Feriae, Vigilien, Oktavtage und Kommemorationen aufnehmen muss.

## Leitentscheidung

DO bleibt wertvoll als Quell- und Regelbestand. Das eigene System sollte seine
Keys, Dateien und Querverweise aber nicht unveraendert zur theologischen
Identitaet erheben.

Die bessere Architektur ist:

```text
DO source data
  -> importierte source_witnesses und usages
  -> normalisierte celebrations und text_units
  -> kalender- und rubrikabhaengige occurrences
  -> Meditationen mit primaerem Text und liturgischem Kontext
```
