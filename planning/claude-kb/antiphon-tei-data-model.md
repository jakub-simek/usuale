# TEI-Datenmodell fuer einzelne Antiphonen

## Ziel

Dieses Modell beschreibt Antiphonen als eigenstaendige TEI-Dateien. Eine
Antiphon ist dabei nicht nur ein kurzer liturgischer Text, sondern ein
kommentierbares Editionsobjekt mit:

- lateinischem Text mit Variantenapparat
- kurzer Quellenangabe fuer liturgische Anzeige und Suche
- ausfuehrlicher Quellen-Dokumentation, ggf. mit lateinischer, griechischer
  und hebraeischer Textfassung
- externen Identifikatoren, etwa gregorien.info, Cantus, Gregobase, CAO und
  Antiphonale Synopticum
- Handschriften- und Druckzeugen
- Links zu Digitalisaten und konkreten Bildausschnitten
- extern gespeicherter GABC-Notenedition mit TEI-Pointer
- liturgischen Verwendungen, ohne die Antiphon selbst mehrfach zu duplizieren

Kernentscheidung: Die Antiphon-Datei enthaelt die Identitaet, den edierten Text,
Quellen, Zeugnisse und die Metadaten der Musik. Die GABC-Notation liegt in
einer eigenen Datei und wird aus TEI mit `ptr` referenziert. Die konkrete
Verwendung in einem Offizium referenziert die Antiphon-Datei von aussen.

Die semantische Klassifikation von Antiphonen und ihren Bestandteilen wird
nicht als lokale TEI-Taxonomie gepflegt, sondern soll auf Klassen einer
separaten RDF/OWL-Ontologie verweisen. Die Architektur, URI-Strategie und das
Hosting sind in `../ontology-and-tei.md` dokumentiert.

## Dateiebene und Identitaet

### Dateinamen

Empfohlenes Muster:

```text
data/tei/antiphons/<stable-id>.xml
```

Beispiele:

```text
data/tei/antiphons/ant-dominus-dixit-ad-me.xml
data/tei/antiphons/ant-rex-pacificus.xml
data/tei/antiphons/ant-hodie-christus-natus-est.xml
```

Die `stable-id` sollte nicht von einer einzelnen liturgischen Verwendung
abhaengen. Sie benennt die Antiphon als textlich-musikalische Einheit, nicht
ihre Stelle in einem bestimmten Offizium.

### XML-Identifikatoren

```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0"
     xmlns:xi="http://www.w3.org/2001/XInclude"
     xml:id="ant-dominus-dixit-ad-me"
     xml:lang="la">
```

Empfohlene ID-Schichten:

| Ebene | Beispiel | Zweck |
|-------|----------|-------|
| TEI-Datei | `ant-dominus-dixit-ad-me` | stabile interne Antiphon-ID |
| edierter Text | `ant-dominus-dixit-ad-me.text` | Ziel fuer Zitate und Apparate |
| GABC-Fassung | `ant-dominus-dixit-ad-me.gabc.01` | mehrere Melodiefassungen moeglich |
| Handschriftenausschnitt | `ant-dominus-dixit-ad-me.facsimile.w1` | Bildausschnitt / Zone |
| externer Identifier | `cantus:001234` | Datenbankabgleich |

## Grundstruktur

```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0"
     xmlns:xi="http://www.w3.org/2001/XInclude"
     xml:id="ant-dominus-dixit-ad-me"
     xml:lang="la">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title type="incipit">Dóminus dixit ad me</title>
        <title type="uniform">Dominus dixit ad me: Filius meus es tu</title>
        <respStmt>
          <resp>TEI encoding</resp>
          <name>usuale project</name>
        </respStmt>
      </titleStmt>
      <editionStmt>
        <edition n="0.1">working TEI edition</edition>
      </editionStmt>
      <publicationStmt>
        <publisher>usuale project</publisher>
        <availability status="free">
          <licence target="https://opensource.org/licenses/MIT"/>
        </availability>
      </publicationStmt>
      <sourceDesc>
        <!-- Textzeugen, Quellen, Datenbanken -->
      </sourceDesc>
    </fileDesc>
    <encodingDesc>
      <!-- editorische Prinzipien -->
    </encodingDesc>
    <profileDesc>
      <!-- Klassifikation -->
    </profileDesc>
    <revisionDesc>
      <!-- Aenderungsgeschichte -->
    </revisionDesc>
  </teiHeader>

  <facsimile>
    <!-- Digitalisate und Bildzonen -->
  </facsimile>

  <text xml:lang="la">
    <body>
      <div type="antiphon" xml:id="ant-dominus-dixit-ad-me.text">
        <!-- edierter Text, Quellen, Musik, Notizen -->
      </div>
    </body>
  </text>

  <standOff>
    <!-- Beziehungen zu Psalmen, Offizien, Konkordanzen -->
  </standOff>
</TEI>
```

## Header-Modell

### Zentrale Bibliographie

Alle Literaturangaben, digitalen Quellressourcen, Bibelstellen und
Datenbankdatensaetze werden zentral in folgender TEI-Datei verwaltet:

```text
data/indexes/bibliography.xml
```

Diese Datei hat die Grundstruktur:

```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="bibliography">
  <teiHeader>...</teiHeader>
  <text>
    <body>
      <listBibl>
        <bibl xml:id="bibl-example">...</bibl>
      </listBibl>
    </body>
  </text>
</TEI>
```

Andere TEI-Dateien duplizieren diese Angaben nicht. Sie referenzieren stabile
`bibl/@xml:id`-Werte mit relativen URI-Fragmenten, zum Beispiel:

```text
../../indexes/bibliography.xml#bibl-liber-usualis-1961
```

### `sourceDesc`: Zeugnisse, Quellen, externe Datenbanken

`sourceDesc` trennt drei Dinge, die oft vermischt werden:

1. **Textzeugen**: liturgische Buecher, Handschriften, Drucke, aus denen die
   Antiphon bezeugt ist.
2. **Sachquelle / Textquelle**: Bibel, Kirchenvaeter, liturgische Formel,
   freie Komposition usw.
3. **Referenzdatenbanken**: externe IDs und Konkordanzen.

```xml
<sourceDesc>
  <listWit>
    <witness xml:id="w-ar1912"
             corresp="../../indexes/bibliography.xml#bibl-antiphonale-romanum-1912"/>
    <witness xml:id="w-lu1961"
             corresp="../../indexes/bibliography.xml#bibl-liber-usualis-1961"/>
    <witness xml:id="w-ms-paris-lat-12044"
             corresp="../../indexes/bibliography.xml#bibl-ms-paris-lat-12044"/>
  </listWit>
  <list type="bibliographic-references">
    <head>Text source and concordances</head>
    <item>
      <ref type="text-source"
           target="../../indexes/bibliography.xml#bibl-psalmus-2-7">Ps 2,7</ref>
    </item>
    <item>
      <ref type="concordance"
           target="../../indexes/bibliography.xml#bibl-cantus-001234">Cantus 001234</ref>
    </item>
    <item>
      <ref type="concordance"
           target="../../indexes/bibliography.xml#bibl-cao-1234">CAO 1234</ref>
    </item>
  </list>
</sourceDesc>
```

Lokale `witness/@xml:id`-Werte bleiben notwendig, damit `app`, `lem` und `rdg`
kurze `@wit`-Verweise verwenden koennen. Die Beschreibung des Zeugen steht
jedoch ausschliesslich im referenzierten zentralen `bibl`-Datensatz.

### `profileDesc`: Klassifikation

`profileDesc` beschreibt, was die Antiphon ist: Gattung, liturgische Zeit,
thematische Stichworte, ggf. Sprache und Entstehungskontext.

Freie `keywords` koennen fuer Suchbegriffe erhalten bleiben. Der formale
Texttyp wird dagegen am klassifizierten TEI-Element mit `@ana` auf eine
OWL-Klasse angegeben. Bis der persistente Namensraum registriert ist, bleibt
`ONTOLOGY_BASE_IRI` in diesem Beispiel ein Platzhalter:

```xml
<profileDesc>
  <textClass>
    <keywords scheme="#liturgical-season">
      <term>advent</term>
    </keywords>
  </textClass>
</profileDesc>

<text>
  <body>
    <div type="antiphon"
         ana="ONTOLOGY_BASE_IRI#PsalmAntiphon">
      ...
    </div>
  </body>
</text>
```

### `standOff`: liturgische Beziehungen

Die Antiphon selbst darf mehrfach verwendet werden. Diese Vorkommen gehoeren
als maschinenlesbare Beziehungen in `standOff`, nicht als doppelte Textbloecke.

```xml
<standOff>
  <linkGrp type="liturgical-relations">
    <link type="used-in"
          target="#ant-dominus-dixit-ad-me.text ../offices/tempora/adv1-0.xml#matutinum"/>
    <link type="sung-with"
          target="#ant-dominus-dixit-ad-me.text ../psalms/ps-002.xml"/>
  </linkGrp>
  <list>
    <item corresp="../offices/tempora/adv1-0.xml#matutinum">
      Dominica I Adventus, Matutinum, antiphona 1
    </item>
    <item corresp="../psalms/ps-002.xml">
      Psalmus 2, bevorzugte Psalmassoziation.
    </item>
  </list>
</standOff>
```

Alternativ kann liturgische Verwendung ganz aus der Antiphon-Datei ausgelagert
werden, z.B. in Office-Dateien oder in YAML. Dann enthaelt `standOff` nur
`sung-with` als bevorzugte Psalmassoziation, nicht alle konkreten Vorkommen.

## Textmodell

### Einfacher edierter Text

```xml
<div type="antiphon" xml:id="ant-dominus-dixit-ad-me.text">
  <head>Dóminus dixit ad me</head>
  <ab type="liturgical-text">
    <seg type="incipit">Dóminus dixit</seg>
    <caesura type="asteriscus"/>
    <seg type="continuatio">ad me: Fílius meus es tu, ego hódie génui te.</seg>
  </ab>
</div>
```

Der Asteriskus wird als `caesura type="asteriscus"` kodiert. Dadurch bleibt
klar, dass `*` nicht einfach Interpunktion ist, sondern eine liturgisch-musikalische
Textmarke.

### Variantenapparat

TEI-Standard fuer Varianten ist `app` mit `lem` und `rdg`. Das Lemma ist der
edierte Text, die Lesarten verweisen ueber `@wit` auf `listWit`.

```xml
<ab type="liturgical-text">
  <seg type="incipit">Dóminus dixit</seg>
  <caesura type="asteriscus"/>
  ad me:
  <app>
    <lem wit="#w-ar1960 #w-lu1961">Fílius meus es tu</lem>
    <rdg wit="#w-ms-paris-lat-12044">filius meus es tu</rdg>
  </app>,
  ego hódie
  <app>
    <lem wit="#w-ar1960">génui</lem>
    <rdg wit="#w-lu1961" type="orthographic">genui</rdg>
  </app>
  te.
</ab>
```

Empfohlene `@type`-Werte fuer `rdg`:

| Wert | Bedeutung |
|------|-----------|
| `substantive` | inhaltlich relevante Lesart |
| `orthographic` | Schreibungs-/Akzentvariante |
| `punctuation` | Interpunktionsvariante |
| `melodic-text` | Textvariante, die durch Melodietradition bedingt ist |
| `omission` | Auslassung |
| `addition` | Zusatz |

## Quellenmodell

### Kurze Quellenangabe

Fuer liturgische Anzeige und Suchfilter reicht eine kurze Quellenangabe direkt
am Textblock:

```xml
<note type="source-summary" target="#ant-dominus-dixit-ad-me.text">
  Ps 2:7
</note>
```

Bei ungenauer oder indirekter Herkunft:

```xml
<note type="source-summary" cert="medium">
  cf. Ps 2:7
</note>
```

Empfohlene `@cert`-Werte: `high`, `medium`, `low`, `unknown`.

### Ausfuehrliche Quellenzitate

Ausfuehrliche Quellen gehoeren in einen eigenen `div type="source-context"`.
Die Fassungen koennen parallel als `quote` mit `xml:lang` und `@source`
angelegt werden.

```xml
<div type="source-context" xml:id="ant-dominus-dixit-ad-me.sources">
  <head>Textquelle</head>
  <ref type="bibliographic"
       target="../../indexes/bibliography.xml#bibl-psalmus-2-7">Psalmus 2:7</ref>

  <quote xml:lang="la"
         source="../../indexes/bibliography.xml#bibl-psalmus-2-7-vulgata">
    Dóminus dixit ad me: Fílius meus es tu; ego hódie génui te.
  </quote>

  <quote xml:lang="grc"
         source="../../indexes/bibliography.xml#bibl-psalmus-2-7-septuaginta">
    Κύριος εἶπεν πρός με· υἱός μου εἶ σύ, ἐγὼ σήμερον γεγέννηκά σε.
  </quote>

  <quote xml:lang="he"
         source="../../indexes/bibliography.xml#bibl-psalmus-2-7-masoreticus"
         rend="rtl">
    יהוה אמר אלי בני אתה אני היום ילדתיך
  </quote>

  <note type="source-relation">
    Die Antiphon uebernimmt den Vulgatatext fast woertlich und setzt den
    liturgischen Asteriskus nach dem ersten Verbalkomplex.
  </note>
</div>
```

Bei patristischen Quellen wird der Datensatz ebenfalls zentral angelegt:

```xml
<bibl xml:id="bibl-augustinus-sermo-185-3" type="patristic">
  <author>Augustinus</author>
  <title>Sermo 185</title>
  <biblScope unit="section">3</biblScope>
</bibl>
```

## Handschriften und Bildausschnitte

### Ganze Digitalisate

Im `facsimile` werden Digitalisate, Seiten und Ausschnitte beschrieben. Die
Antiphon im Text kann dann ueber `@facs` auf die passende Zone zeigen.

```xml
<facsimile>
  <surface xml:id="surf-paris-lat-12044-045r">
    <graphic url="https://example.org/iiif/paris-lat-12044/canvas/45r/full/full/0/default.jpg"
             mimeType="image/jpeg"/>
    <zone xml:id="zone-paris-lat-12044-045r-ant"
          ulx="1200" uly="840" lrx="2380" lry="1040">
      <desc>Dóminus dixit ad me, antiphon with notation</desc>
    </zone>
  </surface>
</facsimile>
```

### Verknuepfung mit Text und Varianten

```xml
<ab type="liturgical-text" facs="#zone-paris-lat-12044-045r-ant">
  Dóminus dixit <caesura type="asteriscus"/> ad me:
  <app>
    <lem wit="#w-ar1960">Fílius meus es tu</lem>
    <rdg wit="#w-ms-paris-lat-12044"
         facs="#zone-paris-lat-12044-045r-ant">Filius meus es tu</rdg>
  </app>
</ab>
```

Fuer IIIF-Umgebungen kann `@url` direkt auf eine IIIF-Image-API-URL zeigen.
Wenn ein Projekt eigene Bildausschnitte erzeugt, kann die `zone` zusaetzlich
eine lokale Datei referenzieren.

## GABC-Modell

GABC wird nicht in die TEI-Datei eingebettet. Die kanonische Notationsdatei
liegt unter:

```text
data/gabc/antiphons/<stable-id>.gabc
```

TEI beschreibt die Notationsfassung und referenziert sie mit `ptr`. So bleibt
die GABC-Datei unmittelbar mit Gregorio und anderen Notationswerkzeugen
verwendbar, waehrend TEI Identitaet, Provenienz und Beziehungen verwaltet.

```xml
<div type="notation" xml:id="ant-dominus-dixit-ad-me.music">
  <notatedMusic xml:id="ant-dominus-dixit-ad-me.gabc.01"
                type="gabc"
                corresp="#ant-dominus-dixit-ad-me.text">
    <head>GABC edition</head>
    <ptr type="notation-file"
         target="../../gabc/antiphons/ant-dominus-dixit-ad-me.gabc"
         mimeType="text/plain"/>
  </notatedMusic>
</div>
```

Wenn mehrere Melodietraditionen vorliegen, erhaelt jede Fassung eine eigene
GABC-Datei und einen eigenen `notatedMusic`-Block:

```xml
<notatedMusic xml:id="ant-dominus-dixit-ad-me.gabc.ar"
              type="gabc"
              source="#w-ar1960">
  <ptr type="notation-file"
       target="../../gabc/antiphons/ant-dominus-dixit-ad-me.ar.gabc"
       mimeType="text/plain"/>
</notatedMusic>
<notatedMusic xml:id="ant-dominus-dixit-ad-me.gabc.ms-paris"
              type="gabc"
              source="#w-ms-paris-lat-12044"
              facs="#zone-paris-lat-12044-045r-ant">
  <ptr type="notation-file"
       target="../../gabc/antiphons/ant-dominus-dixit-ad-me.ms-paris.gabc"
       mimeType="text/plain"/>
</notatedMusic>
```

## Externe Identifikatoren

Externe IDs sollten nicht als freie Notizen verstreut werden. Sie stehen in
zentralen `bibl[@type='database']`-Datensaetzen in `bibliography.xml`; die
Antiphon-Datei verweist aus `sourceDesc/listRef` auf diese Datensaetze.

Empfohlene `@type`-Werte:

| Datenbank | `idno/@type` |
|-----------|--------------|
| Cantus Index | `cantus` |
| CAO | `cao` |
| gregorien.info | `gregorien.info` |
| Gregobase | `gregobase` |
| Antiphonale Synopticum | `antiphonale-synopticum` |
| lokale ID | `usuale` |
| Divinum Officium Herkunft | `divinum-officium` |

Beispiel:

```xml
<bibl xml:id="bibl-cantus-001234" type="database">
  <title>Cantus Index</title>
  <idno type="cantus">001234</idno>
  <ptr target="https://cantusindex.org/id/001234"/>
</bibl>
```

## Beziehungen zu Psalmen und Offizien

Die heutige Divinum-Officium-Zeile:

```text
Dóminus dixit * ad me: Fílius meus es tu, ego hódie génui te.;;2
```

wird in zwei Beziehungen aufgeloest:

1. Antiphon-Datei kodiert den Text.
2. Office- oder Psalmodie-Datei verknuepft Antiphon und Psalm.

In einer Office-Datei:

```xml
<div type="hour" subtype="matutinum">
  <div type="psalmody" n="1">
    <ref type="antiphon" target="../antiphons/ant-dominus-dixit-ad-me.xml"/>
    <ref type="psalm" target="../psalms/ps-002.xml"/>
  </div>
</div>
```

Bei Psalmabschnitten:

```xml
<ref type="psalm" target="../psalms/ps-135.xml#range(1,9)"/>
```

Fuer XPath- oder XPointer-faehige Verarbeitung waere auch eine explizite
Struktur robuster:

```xml
<ref type="psalm" target="../psalms/ps-135.xml">
  <biblScope unit="verse" from="1" to="9"/>
</ref>
```

## Vollbeispiel

```xml
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0"
     xml:id="ant-dominus-dixit-ad-me"
     xml:lang="la">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title type="incipit">Dóminus dixit ad me</title>
        <title type="uniform">Dominus dixit ad me: Filius meus es tu</title>
        <respStmt>
          <resp>TEI encoding</resp>
          <name>usuale project</name>
        </respStmt>
      </titleStmt>
      <editionStmt>
        <edition n="0.1">working TEI edition</edition>
      </editionStmt>
      <publicationStmt>
        <publisher>usuale project</publisher>
        <availability status="free">
          <licence target="https://opensource.org/licenses/MIT"/>
        </availability>
      </publicationStmt>
      <sourceDesc>
        <listWit>
          <witness xml:id="w-ar1912"
                   corresp="../../indexes/bibliography.xml#bibl-antiphonale-romanum-1912"/>
          <witness xml:id="w-ms-paris-lat-12044"
                   corresp="../../indexes/bibliography.xml#bibl-ms-paris-lat-12044"/>
        </listWit>
        <list type="bibliographic-references">
          <head>Text source and concordances</head>
          <item>
            <ref type="text-source"
                 target="../../indexes/bibliography.xml#bibl-psalmus-2-7">Ps 2,7</ref>
          </item>
          <item>
            <ref type="concordance"
                 target="../../indexes/bibliography.xml#bibl-cantus-001234">Cantus 001234</ref>
          </item>
          <item>
            <ref type="concordance"
                 target="../../indexes/bibliography.xml#bibl-cao-1234">CAO 1234</ref>
          </item>
        </list>
      </sourceDesc>
    </fileDesc>

    <encodingDesc>
      <editorialDecl>
        <p>Akzente werden als liturgische Vortragshilfen erhalten. Der
        Asteriskus wird als caesura type="asteriscus" kodiert.</p>
      </editorialDecl>
    </encodingDesc>

    <profileDesc>
      <textClass>
        <keywords scheme="#genre">
          <term>antiphon</term>
          <term>psalm-antiphon</term>
        </keywords>
        <keywords scheme="#liturgical-season">
          <term>advent</term>
        </keywords>
      </textClass>
    </profileDesc>

    <revisionDesc>
      <change when="2026-05-09" who="#encoder">Initial model example.</change>
    </revisionDesc>
  </teiHeader>

  <facsimile>
    <surface xml:id="surf-paris-lat-12044-045r">
      <graphic url="https://example.org/iiif/paris-lat-12044/45r/full/full/0/default.jpg"
               mimeType="image/jpeg"/>
      <zone xml:id="zone-paris-lat-12044-045r-ant"
            ulx="1200" uly="840" lrx="2380" lry="1040"/>
    </surface>
  </facsimile>

  <text>
    <body>
      <div type="antiphon" xml:id="ant-dominus-dixit-ad-me.text">
        <head>Dóminus dixit ad me</head>

        <ab type="liturgical-text" facs="#zone-paris-lat-12044-045r-ant">
          <seg type="incipit">Dóminus dixit</seg>
          <caesura type="asteriscus"/>
          ad me:
          <app>
            <lem wit="#w-ar1912">Fílius meus es tu</lem>
            <rdg wit="#w-ms-paris-lat-12044" type="orthographic">Filius meus es tu</rdg>
          </app>,
          ego hódie génui te.
        </ab>

        <note type="source-summary" target="#ant-dominus-dixit-ad-me.text"
              cert="high">Ps 2:7</note>

        <div type="source-context" xml:id="ant-dominus-dixit-ad-me.sources">
          <head>Textquelle</head>
          <quote xml:lang="la"
                 source="../../indexes/bibliography.xml#bibl-psalmus-2-7-vulgata">
            Dóminus dixit ad me: Fílius meus es tu; ego hódie génui te.
          </quote>
          <quote xml:lang="grc"
                 source="../../indexes/bibliography.xml#bibl-psalmus-2-7-septuaginta">
            Κύριος εἶπεν πρός με· υἱός μου εἶ σύ, ἐγὼ σήμερον γεγέννηκά σε.
          </quote>
          <quote xml:lang="he"
                 source="../../indexes/bibliography.xml#bibl-psalmus-2-7-masoreticus"
                 rend="rtl">
            יהוה אמר אלי בני אתה אני היום ילדתיך
          </quote>
        </div>

        <div type="notation" xml:id="ant-dominus-dixit-ad-me.music">
          <notatedMusic xml:id="ant-dominus-dixit-ad-me.gabc.01"
                        type="gabc"
                        corresp="#ant-dominus-dixit-ad-me.text">
            <head>GABC edition</head>
            <ptr type="notation-file"
                 target="../../gabc/antiphons/ant-dominus-dixit-ad-me.gabc"
                 mimeType="text/plain"/>
          </notatedMusic>
        </div>
      </div>
    </body>
  </text>

  <standOff>
    <linkGrp type="liturgical-relations">
      <link type="sung-with"
            target="#ant-dominus-dixit-ad-me.text ../psalms/ps-002.xml"/>
    </linkGrp>
  </standOff>
</TEI>
```

## Validierungsregeln fuer eine ODD/RelaxNG-Anpassung

Mindestregeln:

- Jede Antiphon-Datei hat genau ein `div[@type='antiphon']` im Body.
- Das Wurzelelement hat ein stabiles `xml:id`.
- `titleStmt/title[@type='incipit']` ist Pflicht.
- Alle bibliographischen Datensaetze stehen in
  `data/indexes/bibliography.xml` unter `text/body/listBibl`.
- Antiphon-Dateien enthalten keine eigenen `bibl` oder `biblStruct`.
- `sourceDesc/listWit` ist optional, aber wenn Variantenapparat vorhanden ist,
  muessen alle `@wit`-Verweise auf existierende `witness/@xml:id` zeigen und
  jedes `witness` muss mit `@corresp` auf einen zentralen `bibl`-Datensatz
  verweisen.
- Externe IDs werden nur als `idno` mit kontrolliertem `@type` in der zentralen
  Bibliographie kodiert.
- Jede GABC-Fassung wird durch `notatedMusic[@type='gabc']` beschrieben.
- Jedes `notatedMusic[@type='gabc']` enthaelt genau einen
  `ptr[@type='notation-file']` auf eine existierende `.gabc`-Datei.
- GABC-Inhalt wird nicht als `ab`, CDATA oder Freitext in TEI dupliziert.
- Der liturgische Asteriskus wird als `caesura[@type='asteriscus']`, nicht als
  rohes Sternchen im Haupttext, kodiert.
- Bildausschnitte werden als `facsimile/surface/zone` modelliert und aus Text,
  Lesart oder Notation mit `@facs` referenziert.

## Empfehlungen

1. **Antiphon als Werk-/Editionsobjekt behandeln**: Text, Quellen und
   Musikmetadaten gehoeren in die Antiphon-Datei; die GABC-Notation liegt in
   einer referenzierten `.gabc`-Datei. Kalender- und Rubrikenlogik gehoeren in
   Office-/YAML-Dateien.
2. **Psalmzuordnung nicht in den Text einbetten**: Das alte `;;109` wird als
   Beziehung modelliert, nicht als Teil der Antiphon.
3. **Quellenangabe zweistufig halten**: kurze `source-summary` fuer Anzeige,
   ausfuehrliche `source-context` fuer Forschung.
4. **Datenbank-IDs normalisieren**: alle externen IDs ueber `idno/@type`, damit
   spaeter Konkordanzen und Dublettenabgleich einfach bleiben; die Datensaetze
   stehen zentral in `data/indexes/bibliography.xml`.
5. **GABC aus TEI auslagern**: die kanonische GABC-Edition wird unter
   `data/gabc/antiphons/` gepflegt und aus TEI ausschliesslich mit
   `ptr[@type='notation-file']` referenziert.
6. **Facsimile-Zonen frueh einplanen**: auch wenn noch keine Bildausschnitte
   vorhanden sind, sollte die Struktur dafuer von Anfang an im Schema erlaubt
   sein.
