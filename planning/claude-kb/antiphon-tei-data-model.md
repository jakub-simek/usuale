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
- GABC-Notenedition
- liturgischen Verwendungen, ohne die Antiphon selbst mehrfach zu duplizieren

Kernentscheidung: Die Antiphon-Datei enthaelt die Identitaet, den edierten Text,
Quellen, Zeugnisse und Musik. Die konkrete Verwendung in einem Offizium
referenziert diese Datei von aussen.

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
    <witness xml:id="w-ar1960">
      <bibl>
        <title>Antiphonale Romanum</title>
        <date when="1912">1912</date>
      </bibl>
    </witness>
    <witness xml:id="w-lu1961">
      <bibl>
        <title>Liber Usualis</title>
        <date when="1961">1961</date>
      </bibl>
    </witness>
    <witness xml:id="w-ms-paris-lat-12044">
      <msDesc>
        <msIdentifier>
          <settlement>Paris</settlement>
          <repository>Bibliothèque nationale de France</repository>
          <idno>lat. 12044</idno>
        </msIdentifier>
      </msDesc>
    </witness>
  </listWit>

  <listBibl type="text-sources">
    <bibl xml:id="src-ps-2-7" type="biblical">
      <title>Psalmus 2</title>
      <biblScope unit="verse">7</biblScope>
      <ref target="urn:cts:latinLit:stoa0049.stoa001:2.7">Ps 2:7</ref>
    </bibl>
  </listBibl>

  <listBibl type="external-identifiers">
    <bibl xml:id="id-cantus" type="database">
      <title>Cantus Index</title>
      <idno type="cantus">001234</idno>
      <ptr target="https://cantusindex.org/id/001234"/>
    </bibl>
    <bibl xml:id="id-cao" type="database">
      <title>Corpus Antiphonalium Officii</title>
      <idno type="cao">1234</idno>
    </bibl>
    <bibl xml:id="id-gregorien" type="database">
      <title>gregorien.info</title>
      <idno type="gregorien.info">ant/1234</idno>
      <ptr target="https://gregorien.info/chant/id/1234/0/en"/>
    </bibl>
    <bibl xml:id="id-gregobase" type="database">
      <title>Gregobase</title>
      <idno type="gregobase">1234</idno>
      <ptr target="https://gregobase.selapa.net/chant.php?id=1234"/>
    </bibl>
    <bibl xml:id="id-antiphonale-synopticum" type="database">
      <title>Antiphonale Synopticum</title>
      <idno type="antiphonale-synopticum">AS-1234</idno>
    </bibl>
  </listBibl>
</sourceDesc>
```

### `profileDesc`: Klassifikation

`profileDesc` beschreibt, was die Antiphon ist: Gattung, liturgische Zeit,
thematische Stichworte, ggf. Sprache und Entstehungskontext.

```xml
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
  <bibl corresp="#src-ps-2-7">Psalmus 2:7</bibl>

  <quote xml:lang="la" source="#src-vulgata">
    Dóminus dixit ad me: Fílius meus es tu; ego hódie génui te.
  </quote>

  <quote xml:lang="grc" source="#src-lxx">
    Κύριος εἶπεν πρός με· υἱός μου εἶ σύ, ἐγὼ σήμερον γεγέννηκά σε.
  </quote>

  <quote xml:lang="he" source="#src-mt" rend="rtl">
    יהוה אמר אלי בני אתה אני היום ילדתיך
  </quote>

  <note type="source-relation">
    Die Antiphon uebernimmt den Vulgatatext fast woertlich und setzt den
    liturgischen Asteriskus nach dem ersten Verbalkomplex.
  </note>
</div>
```

Bei patristischen Quellen kann dasselbe Muster verwendet werden:

```xml
<bibl xml:id="src-aug-sermo-185" type="patristic">
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

GABC kann entweder eingebettet oder extern referenziert werden. Fuer eine
wissenschaftliche Edition ist beides sinnvoll: eingebetteter kanonischer Stand
plus optionaler Link auf die Quelldatei.

```xml
<div type="notation" xml:id="ant-dominus-dixit-ad-me.music">
  <notatedMusic xml:id="ant-dominus-dixit-ad-me.gabc.01"
                type="gabc"
                corresp="#ant-dominus-dixit-ad-me.text">
    <head>GABC edition</head>
    <ptr type="source-file" target="../../gabc/ant-dominus-dixit-ad-me.gabc"/>
    <ab type="gabc"><![CDATA[
name:Dominus dixit ad me;
office-part:an;
mode:2;
%%
Dó(f)mi(g)nus(h) di(g)xit(f) *(,) ad(g) me:(h) Fí(h)li(g)us(f) me(g)us(h) es(g) tu,(f) (::)
    ]]></ab>
  </notatedMusic>
</div>
```

Wenn mehrere Melodietraditionen vorliegen:

```xml
<notatedMusic xml:id="ant-dominus-dixit-ad-me.gabc.ar" type="gabc"
              source="#w-ar1960"/>
<notatedMusic xml:id="ant-dominus-dixit-ad-me.gabc.ms-paris" type="gabc"
              source="#w-ms-paris-lat-12044"
              facs="#zone-paris-lat-12044-045r-ant"/>
```

## Externe Identifikatoren

Externe IDs sollten nicht als freie Notizen verstreut werden. Empfohlen ist
ein normierter Block im `sourceDesc`, ergaenzt durch `idno/@type`.

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
<idno type="usuale">ant-dominus-dixit-ad-me</idno>
<idno type="cantus">001234</idno>
<idno type="cao">1234</idno>
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
          <witness xml:id="w-ar1912">
            <bibl>
              <title>Antiphonale Romanum</title>
              <date when="1912">1912</date>
            </bibl>
          </witness>
          <witness xml:id="w-ms-paris-lat-12044">
            <msDesc>
              <msIdentifier>
                <settlement>Paris</settlement>
                <repository>Bibliothèque nationale de France</repository>
                <idno>lat. 12044</idno>
              </msIdentifier>
            </msDesc>
          </witness>
        </listWit>

        <listBibl type="text-sources">
          <bibl xml:id="src-ps-2-7" type="biblical">
            <title>Psalmus 2</title>
            <biblScope unit="verse">7</biblScope>
          </bibl>
        </listBibl>

        <listBibl type="external-identifiers">
          <bibl type="database">
            <title>Cantus Index</title>
            <idno type="cantus">001234</idno>
            <ptr target="https://cantusindex.org/id/001234"/>
          </bibl>
          <bibl type="database">
            <title>Corpus Antiphonalium Officii</title>
            <idno type="cao">1234</idno>
          </bibl>
        </listBibl>
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
          <quote xml:lang="la" source="#src-ps-2-7">
            Dóminus dixit ad me: Fílius meus es tu; ego hódie génui te.
          </quote>
          <quote xml:lang="grc" source="#src-ps-2-7">
            Κύριος εἶπεν πρός με· υἱός μου εἶ σύ, ἐγὼ σήμερον γεγέννηκά σε.
          </quote>
          <quote xml:lang="he" source="#src-ps-2-7" rend="rtl">
            יהוה אמר אלי בני אתה אני היום ילדתיך
          </quote>
        </div>

        <div type="notation" xml:id="ant-dominus-dixit-ad-me.music">
          <notatedMusic xml:id="ant-dominus-dixit-ad-me.gabc.01"
                        type="gabc"
                        corresp="#ant-dominus-dixit-ad-me.text">
            <head>GABC edition</head>
            <ptr type="source-file" target="../../gabc/ant-dominus-dixit-ad-me.gabc"/>
            <ab type="gabc"><![CDATA[
name:Dominus dixit ad me;
office-part:an;
mode:2;
%%
Dó(f)mi(g)nus(h) di(g)xit(f) *(,) ad(g) me:(h) Fí(h)li(g)us(f) me(g)us(h) es(g) tu,(f) (::)
            ]]></ab>
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
- `sourceDesc/listWit` ist optional, aber wenn Variantenapparat vorhanden ist,
  muessen alle `@wit`-Verweise auf existierende `witness/@xml:id` zeigen.
- Externe IDs werden nur als `idno` mit kontrolliertem `@type` kodiert.
- GABC steht in `notatedMusic[@type='gabc']`.
- Der liturgische Asteriskus wird als `caesura[@type='asteriscus']`, nicht als
  rohes Sternchen im Haupttext, kodiert.
- Bildausschnitte werden als `facsimile/surface/zone` modelliert und aus Text,
  Lesart oder Notation mit `@facs` referenziert.

## Empfehlungen

1. **Antiphon als Werk-/Editionsobjekt behandeln**: Text, Quellen und Musik
   gehoeren in die Antiphon-Datei; Kalender- und Rubrikenlogik gehoeren in
   Office-/YAML-Dateien.
2. **Psalmzuordnung nicht in den Text einbetten**: Das alte `;;109` wird als
   Beziehung modelliert, nicht als Teil der Antiphon.
3. **Quellenangabe zweistufig halten**: kurze `source-summary` fuer Anzeige,
   ausfuehrliche `source-context` fuer Forschung.
4. **Datenbank-IDs normalisieren**: alle externen IDs ueber `idno/@type`, damit
   spaeter Konkordanzen und Dublettenabgleich einfach bleiben.
5. **GABC nah an der Antiphon speichern**: die kanonische GABC-Edition sollte
   in der TEI-Datei enthalten sein; externe `.gabc`-Dateien koennen daraus
   generiert oder zusaetzlich gepflegt werden.
6. **Facsimile-Zonen frueh einplanen**: auch wenn noch keine Bildausschnitte
   vorhanden sind, sollte die Struktur dafuer von Anfang an im Schema erlaubt
   sein.
