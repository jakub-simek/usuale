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

Als lateinischer Terminus fuer `celebration` empfiehlt sich `celebratio`.
Der Begriff ist kirchlich verstaendlich und neutral genug fuer Sonntage,
Feste, Feriae, Vigilien, Oktavtage, Rogationen und Kommemorationen. Er ist
besser geeignet als:

- `festum`, weil das fuer Feriae, Vigilien und Rogationen zu eng ist
- `sollemnitas`, weil es zu hochrangig klingt
- `dies liturgicus`, weil es zu stark den Kalendertag betont
- `officium`, weil es mit Brevier/Office und DO-Dateien verwechselt wuerde
- `memoria`, weil es besonders fuer Heiligenfeiern zu eng ist

In lateinisch benannten Datenfeldern koennte die Entitaet also `celebratio`
heissen, waehrend `calendar_assignment` etwa als `assignatio_calendarii`
modelliert werden kann.

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
  source_path: sources/divinum-officium/web/www/missa/Latin/Tempora/Pasc5-0.txt

liturgical_form:
  id: officium:tempora:pasc5-0
  celebration_id: tempora:pasc5-0
  form: officium
  source_path: sources/divinum-officium/web/www/horas/Latin/Tempora/Pasc5-0.txt
```

So kann eine Meditation ueber den Introitus zugleich den Kontext von Epistel,
Evangelium und Officium beruecksichtigen.

## Celebration-Register in TEI

Die normalisierten `celebrations` koennen als TEI-basiertes Sachregister nach
dem Registerschema von heiEDITIONS modelliert werden. Die `celebratio` ist in
diesem Register nicht das konkrete Auftreten an einem Datum, sondern die
liturgische Sache selbst: z. B. `Dominica V Post Pascha`, `In Rogationibus` oder
`S. Benedicti Abbatis`.

Die Grundform ist:

```xml
<text ana="hc:IndexOfSubjects">
  <body>
    <list>
      <item xml:id="celebratio-temporale-dominica-5-post-pascha">
        <label xml:lang="la" ana="hc:PreferredAppellation">Dominica V Post Pascha</label>
        <label xml:lang="de" ana="hc:PreferredAppellation">Fuenfter Sonntag nach Ostern</label>
        <idno ana="hc:PrivateIdentifier">temporale:dominica-5-post-pascha</idno>
        <note xml:lang="la">
          <p>Celebratio temporalis temporis paschalis.</p>
        </note>
        <listRef>
          <desc>Fontes Divinum Officium</desc>
          <ref target="../sources/divinum-officium/web/www/missa/Latin/Tempora/Pasc5-0.txt">Missa</ref>
          <ref target="../sources/divinum-officium/web/www/horas/Latin/Tempora/Pasc5-0.txt">Officium</ref>
        </listRef>
      </item>
    </list>
  </body>
</text>
```

Dabei sind einige Schema-Eigenheiten zu beachten:

- Das Register ist ein Sachregister: `text/@ana` steht auf
  `hc:IndexOfSubjects`.
- Die einzelnen Feiern stehen als `<item>` in einer einfachen `<list>`.
- Jedes `<item>` braucht ein stabiles `xml:id`.
- `<idno>` verwendet nach dem heiEDITIONS-Schema `@ana`, nicht ein freies
  `@type`.
- Fuer interne IDs ist `ana="hc:PrivateIdentifier"` geeignet.
- Pro `<item>` sollte nicht mehrfach derselbe Identifier-Typ verwendet werden;
  weitere Herkunftsangaben gehoeren deshalb eher in `<listRef>` oder `<note>`.
- DO-Dateien und DO-Keys bleiben als Quellen- und Konkordanzangaben erhalten,
  werden aber nicht zur eigentlichen Identitaet der `celebratio`.

## Konstruktion der Register-IDs

Die `xml:id`-Werte der `<item>`-Elemente sollen stabiler sein als die
bestehenden DO-Dateinamen. Sie sollen die liturgische Identitaet bezeichnen,
nicht primaer Datum, Dateipfad oder konkreten Kalenderstand.

Empfohlene Grundform:

```text
celebratio-<bereich>-<sachslug>[-<qualifikator>]
```

Moegliche Bereiche:

```text
temporale     beweglicher Jahreskreis
sanctorale    Heiligen- und Herren-/Marienfeste mit Kalenderdatum
commune       Commune-Formulare
votiva        Votivmessen und Votivoffizien
defuncti      Totenliturgie
rituale       prozessionale, sakramentale oder rituelle Feiern
appendix      Anhaenge, Litaneien, Sondertexte
```

Normalisierungsregeln:

- nur Kleinbuchstaben
- ASCII-Schreibung ohne Akzente, Ligaturen oder Sonderzeichen
- Bindestriche als Worttrenner
- keine Leerzeichen
- kein Doppelpunkt im `xml:id`
- nicht mit einer Zahl beginnen
- Kalenderdaten nur verwenden, wenn das Datum selbst sachlich wesentlich ist

Beispiele:

```xml
<item xml:id="celebratio-temporale-dominica-5-post-pascha">
```

```xml
<item xml:id="celebratio-temporale-rogationes-minores">
```

```xml
<item xml:id="celebratio-sanctorale-benedictus-abbas-transitus">
```

```xml
<item xml:id="celebratio-sanctorale-benedictus-abbas-translatio">
```

```xml
<item xml:id="celebratio-commune-confessoris-pontificis">
```

```xml
<item xml:id="celebratio-votiva-sacratissimi-cordis-iesu">
```

Die interne fachliche ID kann daneben als `idno` stehen:

```xml
<idno ana="hc:PrivateIdentifier">temporale:dominica-5-post-pascha</idno>
```

Diese ID darf Doppelpunkt-Syntax verwenden, weil sie nicht `xml:id` ist. Sie
kann fuer API, Datenbank oder Konkordanzen handlicher sein, waehrend `xml:id`
fuer TEI-Verweise stabil bleibt.

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

Die derzeitige Extraktion wird durch `tools/extract_celebrations.py`
durchgefuehrt. Das Skript erzeugt deterministisch:

```text
data/indexes/celebrations.xml
data/indexes/celebrations-review.tsv
```

`celebrations.xml` ist das eigentliche TEI-Sachregister nach dem
heiEDITIONS-Schema. `celebrations-review.tsv` ist eine editorische Pruefliste
fuer Quellen, die noch nicht automatisch einer `celebratio` zugeordnet werden
konnten.

### Quellenumfang

Die Extraktion beruecksichtigt derzeit die lateinischen Mess- und
Officiumsdateien aus:

- `missa/Latin/Tempora/*.txt`
- `horas/Latin/Tempora/*.txt`
- `missa/Latin/Sancti/*.txt`
- `horas/Latin/Sancti/*.txt`
- `missa/Latin/Commune/*.txt`
- `horas/Latin/Commune/*.txt`
- die entsprechenden `Cist`-, `M`- und `OP`-Varianten, soweit sie in den
  Quellverzeichnissen vorhanden sind

Zu lesen waeren besonders:

- `[Officium]`
- `[Rank]`
- `[Rule]`
- Querverweise mit `@...`

Tatsaechlich verwendet das Skript fuer die erste Bildung einer `celebratio`
primaer den Titel aus `[Officium]`. Dateien ohne eigenen Officium-Titel werden
nicht automatisch als eigene Feier behandelt.

### Gruppierung

Die Grundentscheidung lautet: Eine `celebratio` entsteht nicht pro DO-Datei,
sondern pro liturgischer Sache.

Bei `Tempora`-Dateien wird zuerst nach dem DO-Key gruppiert. Varianten wie
`Pasc5-0t`, `Pasc5-1r` oder andere rubrikale Fassungen werden, soweit die
Heuristik sie erkennt, als Quellen derselben Feier angehaengt. Messe und
Officium mit demselben normalisierten Temporal-Key werden unter derselben
`celebratio` zusammengefuehrt.

Bei `Sancti`- und `Commune`-Dateien wird staerker nach dem normalisierten
Officium-Titel gruppiert, weil der Dateiname im Sanctorale oft primaer ein
Kalenderdatum bezeichnet und keine stabile sachliche Identitaet ist.

Querverweis-Dateien werden rekursiv aufgeloest. Wenn sie auf eine bereits
erkannte Feier zeigen, werden sie als weitere Quelle in `listRef` derselben
`celebratio` aufgenommen. Wenn sie nicht aufgeloest werden koennen, erscheinen
sie in der Review-TSV.

Dabei muessen Varianten klassifiziert werden:

```text
Pasc5-0    kanonischer Temporal-Tag
Pasc5-0t   Variante oder versionsspezifische Ersatzdatei
Pasc5-1    Feria
Pasc5-1r   rubrikale/reformbezogene Variante
```

### Erzeugte TEI-Datei

Jede automatisch erzeugte Feier wird als `<item>` in
`data/indexes/celebrations.xml` geschrieben:

```xml
<item xml:id="celebratio-temporale-dominica-5-post-pascha">
  <label xml:lang="la" ana="hc:PreferredAppellation">Dominica V Post Pascha</label>
  <idno ana="hc:PrivateIdentifier">temporale:dominica-5-post-pascha</idno>
  <listRef>
    <desc>Fontes Divinum Officium</desc>
    <ref target="../../sources/divinum-officium/web/www/missa/Latin/Tempora/Pasc5-0.txt">missa/Latin/Tempora/Pasc5-0.txt</ref>
  </listRef>
</item>
```

Die Eintraege enthalten bewusst keine `<note>`-Elemente. Die Herkunft wird
ueber `<listRef>` dokumentiert. Die erzeugte Datei wird gegen das
heiEDITIONS-RNG validiert.

### Review-TSV

`data/indexes/celebrations-review.tsv` enthaelt alle Quellen, die das Skript
nicht sicher in das Register aufnehmen konnte. Das Format ist tab-separiert:

```text
kind    form    directory    key    path    redirect_ref
```

Die Spalten bedeuten:

- `kind`: derzeit `unmatched_source`; die Quelle wurde nicht automatisch einer
  `celebratio` zugeordnet
- `form`: `missa` oder `horas`
- `directory`: DO-Unterverzeichnis, z. B. `Tempora`, `Sancti`, `Commune`,
  `Appendix`
- `key`: Dateikey ohne `.txt`
- `path`: relativer Pfad der Quelle im Repository
- `redirect_ref`: erkannter DO-Querverweis, falls die Datei mit einem
  `@...`-Verweis beginnt

Ein Eintrag in der Review-TSV ist nicht automatisch ein Fehler. Viele Dateien
sind Textbausteine, Appendices, reine Querverweise, rubrikale Varianten oder
Quellen, fuer die erst entschieden werden muss, ob sie als eigene
`celebratio`, als `text_unit`, als `usage`, als `source_witness` oder als
anderer Datentyp modelliert werden sollen.

Die Review-TSV dient deshalb als Arbeitsliste fuer spaetere editorische
Normalisierung. Wenn eine Quelle eindeutig zuordenbar ist, kann die Heuristik
des Importers verbessert oder eine manuelle Override-Regel im Skript ergaenzt
werden.

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
Der entsprechende lateinische Fachbegriff im eigenen Modell soll `celebratio`
sein.

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
