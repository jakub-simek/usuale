# TEI Data Model for Liturgical Texts - Detailed Proposal

## Executive Summary

This document proposes a comprehensive Text Encoding Initiative (TEI) data model for encoding the liturgical texts of the Divinum Officium project. The model balances scholarly rigor with practical usability, ensuring long-term preservation while maintaining compatibility with the project's needs.

**Key Principles**:
1. **Standards-Based**: Follows TEI P5 guidelines for liturgical texts
2. **Semantic Richness**: Captures liturgical structure, not just formatting
3. **Validation-Ready**: XML schema ensures consistency
4. **Queryable**: XPath/XQuery enables complex searches
5. **Backwards-Compatible**: Maps cleanly from current text format
6. **Multi-Lingual**: Supports parallel texts in multiple languages

---

## Table of Contents

1. [TEI Basics and Rationale](#tei-basics-and-rationale)
2. [Overall Document Structure](#overall-document-structure)
3. [Header Specification](#header-specification)
4. [Body Structure for Divine Office](#body-structure-for-divine-office)
5. [Liturgical Elements Encoding](#liturgical-elements-encoding)
6. [Special Features](#special-features)
7. [Complete Examples](#complete-examples)
8. [XML Schema (RelaxNG)](#xml-schema-relaxng)
9. [Migration Mapping](#migration-mapping)
10. [Query Examples](#query-examples)

---

## TEI Basics and Rationale

### What is TEI?

The **Text Encoding Initiative (TEI)** is an international standard for representing texts in digital form, widely used in:
- Digital humanities projects
- Historical text preservation
- Liturgical and biblical studies
- Scholarly editions

**Website**: https://tei-c.org/
**Current Version**: TEI P5 (Version 4.7.0, 2023)

### Why TEI for Divinum Officium?

#### Scholarly Advantages

✅ **Academic Legitimacy**
- Recognized standard in liturgical studies
- Enables scholarly citation and reference
- Interoperable with other liturgical databases
- Suitable for critical editions

✅ **Semantic Encoding**
- Captures **meaning**, not just **appearance**
- Distinguishes antiphons, psalms, readings, responses
- Preserves liturgical structure
- Documents sources and variants

✅ **Long-Term Preservation**
- Vendor-neutral XML format
- Documented standard that will outlast technologies
- Readable by both humans and machines
- Archival quality

#### Technical Advantages

✅ **Validation**
- XML Schema ensures structural correctness
- Prevents malformed data
- Catches errors early
- Enforces consistency

✅ **Queryability**
- XPath for precise searching
- XQuery for complex analysis
- XSLT for transformations
- Standard tools available

✅ **Flexibility**
- Extensible for project-specific needs
- Customizable via TEI ODD
- Supports metadata
- Handles variants and annotations

#### Practical Advantages

✅ **Multiple Output Formats**
- Transform to HTML for web display
- Generate PDF via XSL-FO
- Create ePub for e-readers
- Export to LaTeX for printing
- Generate JSON for APIs

✅ **Tool Ecosystem**
- XML editors with validation (Oxygen XML, VS Code)
- Processing libraries (lxml, Saxon, BaseX)
- Version control friendly (git diff)
- Many existing tools and libraries

### TEI Customization for Liturgy

TEI provides a base framework that we customize for liturgical texts using:

1. **TEI Module**: `textstructure`, `core`, `header`, `namesdates`, `verse`
2. **Custom Elements**: Defined via TEI ODD (One Document Does-it-all)
3. **Attributes**: Standard TEI plus project-specific
4. **Constraints**: RelaxNG schema for validation

---

## Overall Document Structure

### Root Element

Every TEI document has this basic structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0"
     xmlns:xi="http://www.w3.org/2001/XInclude"
     xml:id="sancti-12-25">

  <teiHeader>
    <!-- Metadata about the document -->
  </teiHeader>

  <text xml:lang="la">
    <body>
      <!-- The actual liturgical content -->
    </body>
  </text>

</TEI>
```

**Key Attributes**:
- `xml:id`: Unique identifier (office key: "sancti-12-25", "tempora-Pent01-0")
- `xml:lang`: Primary language (ISO 639-1: "la", "en", "fr", "it", etc.)
- `xmlns`: TEI namespace
- `xmlns:xi`: XInclude for modular structure

---

## Header Specification

### Complete teiHeader Example

```xml
<teiHeader>
  <fileDesc>
    <titleStmt>
      <title type="main" xml:lang="la">In Nativitate Domini</title>
      <title type="sub" xml:lang="en">The Nativity of Our Lord</title>
      <title type="liturgical">Officium de Nativitate Domini</title>

      <author>
        <orgName>Roman Catholic Church</orgName>
      </author>

      <editor role="encoder">Divinum Officium Project</editor>

      <respStmt>
        <resp>TEI encoding</resp>
        <name>Divinum Officium Contributors</name>
      </respStmt>

      <respStmt>
        <resp>Original transcription</resp>
        <name ref="#lk">Laszlo Kiss</name>
      </respStmt>
    </titleStmt>

    <editionStmt>
      <edition n="2.0">TEI Edition</edition>
      <date when="2025-12-28">2025-12-28</date>
    </editionStmt>

    <publicationStmt>
      <publisher>Divinum Officium Project</publisher>
      <pubPlace>Online</pubPlace>
      <availability status="free">
        <licence target="https://opensource.org/licenses/MIT">
          <p>MIT License - freely available for use, modification, and distribution</p>
        </licence>
      </availability>
      <date when="2025">2025</date>
    </publicationStmt>

    <sourceDesc>
      <biblStruct>
        <monogr>
          <title>Breviarium Romanum</title>
          <edition>Editio Typica 1962</edition>
          <imprint>
            <pubPlace>Vatican City</pubPlace>
            <publisher>Typis Polyglottis Vaticanis</publisher>
            <date when="1962">1962</date>
          </imprint>
        </monogr>
      </biblStruct>

      <listBibl>
        <bibl xml:id="brev1962">Breviarium Romanum 1962</bibl>
        <bibl xml:id="brev1955">Breviarium Romanum 1955</bibl>
        <bibl xml:id="brev1570">Breviarium Romanum 1570</bibl>
      </listBibl>
    </sourceDesc>
  </fileDesc>

  <encodingDesc>
    <projectDesc>
      <p>Digital edition of the traditional Roman Catholic Divine Office
         for various historical rubrics (1570, 1955, 1960, etc.)</p>
    </projectDesc>

    <editorialDecl>
      <punctuation marks="all">
        <p>Original punctuation preserved</p>
      </punctuation>
      <normalization>
        <p>Spelling follows the source editions</p>
      </normalization>
    </editorialDecl>

    <classDecl>
      <taxonomy xml:id="liturgical-rank">
        <category xml:id="rank-duplex-i">
          <catDesc>Duplex I classis (Double of the First Class)</catDesc>
        </category>
        <category xml:id="rank-duplex-ii">
          <catDesc>Duplex II classis (Double of the Second Class)</catDesc>
        </category>
        <!-- etc. -->
      </taxonomy>

      <taxonomy xml:id="liturgical-season">
        <category xml:id="season-advent">
          <catDesc>Advent</catDesc>
        </category>
        <category xml:id="season-christmas">
          <catDesc>Christmas</catDesc>
        </category>
        <!-- etc. -->
      </taxonomy>
    </classDecl>
  </encodingDesc>

  <profileDesc>
    <creation>
      <date when="1962">Based on 1962 Typical Edition</date>
    </creation>

    <langUsage>
      <language ident="la">Latin</language>
    </langUsage>

    <textClass>
      <keywords scheme="#liturgical-rank">
        <term ref="#rank-duplex-i">Duplex I classis</term>
      </keywords>

      <keywords scheme="#liturgical-season">
        <term ref="#season-christmas">Christmas</term>
      </keywords>

      <keywords>
        <term>Sanctoral Cycle</term>
        <term>Feast of the Lord</term>
        <term>Christmas</term>
        <term>Nativity</term>
      </keywords>
    </textClass>
  </profileDesc>

  <revisionDesc>
    <change when="2025-12-28" who="#editor1">Initial TEI encoding</change>
    <change when="2025-11-15" who="#editor2">Converted from text format</change>
  </revisionDesc>
</teiHeader>
```

### Header Components Explained

**fileDesc** - File description
- `titleStmt`: Titles in multiple languages
- `editionStmt`: Edition information
- `publicationStmt`: Publishing details, license
- `sourceDesc`: Source texts (Breviary editions)

**encodingDesc** - Encoding details
- `projectDesc`: Project description
- `editorialDecl`: Editorial practices
- `classDecl`: Taxonomies (ranks, seasons)

**profileDesc** - Text profile
- `creation`: When text was created
- `langUsage`: Languages used
- `textClass`: Classifications and keywords

**revisionDesc** - Change history
- Track modifications over time

---

## Body Structure for Divine Office

### Overall Office Structure

```xml
<text xml:lang="la">
  <body>
    <div type="office" xml:id="office-12-25">

      <!-- Office metadata -->
      <head>In Nativitate Domini</head>

      <div type="metadata">
        <ab type="rank" n="7.0">
          <label>Rank:</label>
          <seg type="class">Duplex I classis</seg>
          <seg type="octave">cum Octava privilegiata</seg>
        </ab>

        <ab type="rules">
          <label>Rule:</label>
          <list>
            <item>9 lectiones</item>
            <item>Psalmi Dominica</item>
            <item>Antiphonas Horas</item>
          </list>
        </ab>

        <ab type="reference">
          <label>Commune:</label>
          <ref target="commune:C1">Ex Communi Apostolorum</ref>
        </ab>
      </div>

      <!-- Canonical Hours -->
      <div type="hour" subtype="matins" xml:id="matins">
        <!-- Matins content -->
      </div>

      <div type="hour" subtype="lauds" xml:id="lauds">
        <!-- Lauds content -->
      </div>

      <div type="hour" subtype="prime" xml:id="prime">
        <!-- Prime content -->
      </div>

      <div type="hour" subtype="terce" xml:id="terce">
        <!-- Terce content -->
      </div>

      <div type="hour" subtype="sext" xml:id="sext">
        <!-- Sext content -->
      </div>

      <div type="hour" subtype="none" xml:id="none">
        <!-- None content -->
      </div>

      <div type="hour" subtype="vespers" xml:id="vespers">
        <!-- Vespers content -->
      </div>

      <div type="hour" subtype="compline" xml:id="compline">
        <!-- Compline content -->
      </div>

    </div>
  </body>
</text>
```

### Matins Structure

```xml
<div type="hour" subtype="matins" xml:id="matins">
  <head>Ad Matutinum</head>

  <!-- Invitatory -->
  <div type="invitatory" xml:id="invit">
    <head>Invitatorium</head>

    <div type="antiphon" n="invit">
      <label>Ant.</label>
      <p xml:id="ant-invit">
        Christus natus est nobis: * Veníte, adorémus.
      </p>
    </div>

    <div type="psalm" xml:id="ps-94">
      <head>Psalmus 94</head>
      <ref target="psalterium:ps-94">Venite, exsultemus Domino</ref>
    </div>
  </div>

  <!-- Hymn -->
  <div type="hymn" xml:id="hymn-mat">
    <head>Hymnus</head>
    <lg type="stanza" n="1">
      <l>Jesu, Redémptor ómnium,</l>
      <l>Quem lucis ante oríginem</l>
      <l>Parem patérnæ glóriæ</l>
      <l>Pater suprémæ éxtulit.</l>
    </lg>

    <lg type="stanza" n="2">
      <l>Tu lumen, tu splendor Patris,</l>
      <l>Tu spes perénnis ómnium,</l>
      <l>Inténde quas fundunt preces</l>
      <l>Tui per orbem sérvuli.</l>
    </lg>

    <!-- More stanzas -->

    <lg type="doxology">
      <l>Glória tibi, Dómine,</l>
      <l>Qui natus es de Vírgine,</l>
      <l>Cum Patre et Sancto Spíritu,</l>
      <l>In sempitérna sǽcula.</l>
      <l>Amen.</l>
    </lg>
  </div>

  <!-- Nocturn I -->
  <div type="nocturn" n="1" xml:id="noct1">
    <head>In I Nocturno</head>

    <!-- Antiphons and Psalms -->
    <div type="psalmody">
      <div type="antiphon" n="1">
        <label>Ant. 1</label>
        <p xml:id="ant-mat-1">
          Dóminus dixit ad me: * Fílius meus es tu,
          ego hódie génui te.
        </p>
      </div>

      <div type="psalm" n="2" xml:id="ps-2">
        <head>Psalmus 2</head>
        <ref target="psalterium:ps-2"/>
        <!-- Or include full psalm text -->
        <lg type="verse" n="1">
          <l>Quare fremuérunt gentes: *</l>
          <l>et pópuli meditáti sunt inánia?</l>
        </lg>
        <lg type="verse" n="2">
          <l>Astitérunt reges terræ, et príncipes convenérunt in unum *</l>
          <l>advérsus Dóminum, et advérsus Christum ejus.</l>
        </lg>
        <!-- More verses -->
        <lg type="doxology">
          <l>Glória Patri, et Fílio, * et Spirítui Sancto.</l>
          <l>Sicut erat in princípio, et nunc, et semper, *
             et in sǽcula sæculórum. Amen.</l>
        </lg>
      </div>

      <!-- Repeat antiphon -->
      <div type="antiphon" n="1" corresp="#ant-mat-1">
        <label>Ant.</label>
        <p>Dóminus dixit ad me: Fílius meus es tu,
           ego hódie génui te.</p>
      </div>

      <!-- Antiphons 2 and 3 with their psalms -->
      <!-- ... -->

    </div>

    <!-- Verse -->
    <div type="versicle">
      <label>℣.</label>
      <p>Tamquam sponsus Dóminus procédens de thálamo suo.</p>
      <label>℟.</label>
      <p>Exsultávit ut gigas ad curréndam viam.</p>
    </div>

    <!-- Readings -->
    <div type="reading" n="1" xml:id="lect1">
      <head>Lectio i</head>

      <div type="source">
        <bibl>
          <title>Liber Isaiae Prophetae</title>
          <biblScope unit="chapter" from="9" to="9">Cap. 9</biblScope>
        </bibl>
      </div>

      <p>
        <seg type="rubric">In illo témpore:</seg>
        Pópulus, qui ambulábat in ténebris, vidit lucem magnam;
        habitántibus in regióne umbræ mortis, lux orta est eis.
        Multiplicásti gentem, et non magnificásti lætítiam.
      </p>
      <p>
        Lætabúntur coram te, sicut qui lætántur in messe,
        sicut exsúltant victóres capta præda, quando dívidunt spólia.
      </p>
    </div>

    <div type="responsory" n="1" xml:id="resp1">
      <div type="response">
        <label>℟.</label>
        <p>
          Hodie nobis cælórum Rex de Vírgine nasci dignátus est,
          ut hóminem pérditum ad cæléstia regna revocáret:
          * Gaudet exércitus Angelórum:
          quia salus ætérna humáno géneri appáruit.
        </p>
      </div>

      <div type="verse">
        <label>℣.</label>
        <p>
          Glória in excélsis Deo, et in terra pax homínibus bonæ voluntátis.
        </p>
      </div>

      <div type="response">
        <label>℟.</label>
        <p>Gaudet exércitus Angelórum:
           quia salus ætérna humáno géneri appáruit.</p>
      </div>
    </div>

    <!-- Lectio 2, Responsory 2, Lectio 3, Responsory 3 -->

  </div>

  <!-- Nocturn II -->
  <div type="nocturn" n="2" xml:id="noct2">
    <!-- Similar structure -->
  </div>

  <!-- Nocturn III -->
  <div type="nocturn" n="3" xml:id="noct3">
    <!-- Similar structure -->
  </div>

  <!-- Te Deum -->
  <div type="canticle" subtype="te-deum" xml:id="tedeum">
    <head>Te Deum</head>
    <ref target="psalterium:te-deum"/>
  </div>

</div>
```

### Lauds Structure

```xml
<div type="hour" subtype="lauds" xml:id="lauds">
  <head>Ad Laudes</head>

  <!-- Antiphons and Psalms -->
  <div type="psalmody">
    <div type="antiphon" n="1">
      <label>Ant. 1</label>
      <p xml:id="ant-laud-1">
        Dóminus dixit ad me: * Fílius meus es tu,
        ego hódie génui te.
      </p>
    </div>

    <div type="psalm" n="92" xml:id="ps-92">
      <head>Psalmus 92</head>
      <ref target="psalterium:ps-92"/>
    </div>

    <!-- Repeat antiphon -->
    <div type="antiphon" n="1" corresp="#ant-laud-1">
      <label>Ant.</label>
      <p>Dóminus dixit ad me: Fílius meus es tu,
         ego hódie génui te.</p>
    </div>

    <!-- Antiphons 2-4 with psalms -->

    <!-- Canticle from Old Testament -->
    <div type="antiphon" n="5">
      <label>Ant. 5</label>
      <p xml:id="ant-laud-5">
        Notum fecit Dóminus, * allelúja,
        salutáre suum, allelúja.
      </p>
    </div>

    <div type="canticle" subtype="old-testament" xml:id="cant-is45">
      <head>Canticum Isaiæ</head>
      <ref target="psalterium:cant-is45"/>
    </div>

    <div type="antiphon" n="5" corresp="#ant-laud-5">
      <label>Ant.</label>
      <p>Notum fecit Dóminus, allelúja,
         salutáre suum, allelúja.</p>
    </div>
  </div>

  <!-- Chapter (Capitulum) -->
  <div type="chapter">
    <head>Capitulum</head>
    <div type="source">
      <bibl>
        <ref target="bible:heb1:1-2">Hebr. 1:1-2</ref>
      </bibl>
    </div>
    <p>
      Multifáriæ olim Deus loquens pátribus in Prophétis,
      novíssime diébus istis locútus est nobis in Fílio,
      quem constítuit herédem universórum,
      per quem fecit et sǽcula.
    </p>
    <p>
      <label>℟.</label>
      Deo grátias.
    </p>
  </div>

  <!-- Hymn -->
  <div type="hymn" xml:id="hymn-laud">
    <head>Hymnus</head>
    <lg type="stanza" n="1">
      <l>A solis ortus cárdine</l>
      <l>Et usque terræ límitem,</l>
      <l>Christum canámus Príncipem</l>
      <l>Natum María Vírgine.</l>
    </lg>
    <!-- More stanzas -->
  </div>

  <!-- Verse -->
  <div type="versicle">
    <label>℣.</label>
    <p>Notum fecit Dóminus, allelúja.</p>
    <label>℟.</label>
    <p>Salutáre suum, allelúja.</p>
  </div>

  <!-- Benedictus with antiphon -->
  <div type="canticle" subtype="benedictus">
    <div type="antiphon" xml:id="ant-bened">
      <label>Ant. ad Benedictus</label>
      <p>
        Glória in excélsis Deo, * et in terra pax homínibus bonæ voluntátis,
        allelúja, allelúja.
      </p>
    </div>

    <div type="canticle-text">
      <head>Canticum Zachariæ</head>
      <ref target="psalterium:benedictus"/>
      <!-- Or include full text -->
    </div>

    <div type="antiphon" corresp="#ant-bened">
      <label>Ant.</label>
      <p>Glória in excélsis Deo, et in terra pax homínibus bonæ voluntátis,
         allelúja, allelúja.</p>
    </div>
  </div>

  <!-- Collect (Oratio) -->
  <div type="collect">
    <head>Oratio</head>
    <p>
      <seg type="invocation">Dómine Jesu Christe,</seg>
      qui te pátri Deo fílium unigénitum
      esse voluísti et de Vírgine María nasci,
      concéde propítius: ut, quam nunc fídei consciéntia gerimus,
      ad perpétuam visiónémdelectatiónemque perveniámus.
    </p>
    <p type="conclusion">
      <ref target="psalterium:oratio-conclusion-standard">Qui vivis et regnas...</ref>
    </p>
    <p>
      <label>℟.</label>
      Amen.
    </p>
  </div>

  <!-- Commemorations (if any) -->
  <div type="commemoration">
    <head>Commemoratio</head>
    <!-- Structure similar to main office -->
  </div>

</div>
```

### Little Hours Structure (Prime, Terce, Sext, None)

```xml
<div type="hour" subtype="prime" xml:id="prime">
  <head>Ad Primam</head>

  <!-- Hymn -->
  <div type="hymn" xml:id="hymn-prime">
    <head>Hymnus</head>
    <ref target="ordinarium:hymn-prime-standard"/>
  </div>

  <!-- Antiphon -->
  <div type="antiphon">
    <label>Ant.</label>
    <p xml:id="ant-prime">
      Dóminus dixit ad me: * Fílius meus es tu,
      ego hódie génui te.
    </p>
  </div>

  <!-- Psalms -->
  <div type="psalmody">
    <div type="psalm" n="53" xml:id="ps-53">
      <head>Psalmus 53</head>
      <ref target="psalterium:ps-53"/>
    </div>
    <!-- More psalms -->
  </div>

  <!-- Repeat antiphon -->
  <div type="antiphon" corresp="#ant-prime">
    <label>Ant.</label>
    <p>Dóminus dixit ad me: Fílius meus es tu,
       ego hódie génui te.</p>
  </div>

  <!-- Chapter -->
  <div type="chapter">
    <head>Capitulum</head>
    <p>Brief reading...</p>
  </div>

  <!-- Short Responsory -->
  <div type="responsory" subtype="brief">
    <label>℟. br.</label>
    <p>Christus natus est nobis, * Veníte, adorémus.</p>
    <p>Christus natus est nobis, * Veníte, adorémus.</p>
    <label>℣.</label>
    <p>Deus homo factus est, et in ætérnum pérmanet.</p>
    <label>℟.</label>
    <p>Veníte, adorémus.</p>
    <label>℣.</label>
    <p>Glória Patri, et Fílio, et Spirítui Sancto.</p>
    <label>℟.</label>
    <p>Christus natus est nobis, * Veníte, adorémus.</p>
  </div>

  <!-- Verse -->
  <div type="versicle">
    <label>℣.</label>
    <p>Notum fecit Dóminus, allelúja.</p>
    <label>℟.</label>
    <p>Salutáre suum, allelúja.</p>
  </div>

  <!-- Collect -->
  <div type="collect">
    <ref target="#collect-main"/>
  </div>

</div>
```

### Vespers Structure

```xml
<div type="hour" subtype="vespers" xml:id="vespers">
  <head>Ad Vesperas</head>

  <!-- Structure very similar to Lauds -->
  <!-- Antiphons, Psalms, Chapter, Hymn, Magnificat -->

  <div type="canticle" subtype="magnificat">
    <div type="antiphon" xml:id="ant-magn">
      <label>Ant. ad Magnificat</label>
      <p>
        Hodie Christus natus est: * hodie Salvátor appáruit:
        hodie in terra canunt Angeli, lætántur Archángeli:
        hodie exsúltant justi, dicéntes:
        Glória in excélsis Deo, allelúja.
      </p>
    </div>

    <div type="canticle-text">
      <head>Canticum B. Mariæ Virginis</head>
      <ref target="psalterium:magnificat"/>
    </div>

    <div type="antiphon" corresp="#ant-magn">
      <label>Ant.</label>
      <p>Hodie Christus natus est...</p>
    </div>
  </div>

  <div type="collect">
    <ref target="#collect-main"/>
  </div>

</div>
```

---

## Liturgical Elements Encoding

### Antiphons

```xml
<div type="antiphon" n="1" xml:id="ant-vesp-1">
  <label>Ant. 1</label>
  <p>
    O admirábile commércium: *
    <seg type="emphasis">Creátor géneris humáni,</seg>
    animátum corpus sumens,
    de Vírgine nasci dignátus est;
    et procédens homo sine sémine,
    largítus est nobis suam Deitátem.
  </p>

  <!-- Optional: link to associated psalm -->
  <note type="psalm-link">
    <ref target="#ps-109">With Psalm 109</ref>
  </note>
</div>
```

**Attributes**:
- `n`: Antiphon number within the hour
- `xml:id`: Unique identifier for cross-referencing
- `type="emphasis"`: Marks emphasized portions

### Psalms

**Option 1: Reference to Psalterium**
```xml
<div type="psalm" n="109" xml:id="ps-109">
  <head>Psalmus 109</head>
  <ref target="psalterium:ps-109">Dixit Dominus</ref>
</div>
```

**Option 2: Full Inclusion**
```xml
<div type="psalm" n="109" xml:id="ps-109">
  <head>Psalmus 109</head>
  <head type="incipit">Dixit Dominus</head>

  <lg type="verse" n="1">
    <l>Dixit Dóminus Dómino meo: *</l>
    <l>Sede a dextris meis.</l>
  </lg>

  <lg type="verse" n="2">
    <l>Donec ponam inimícos tuos, *</l>
    <l>scabéllum pedum tuórum.</l>
  </lg>

  <!-- More verses -->

  <lg type="doxology">
    <l>Glória Patri, et Fílio, *</l>
    <l>et Spirítui Sancto.</l>
    <l>Sicut erat in princípio, et nunc, et semper, *</l>
    <l>et in sǽcula sæculórum. Amen.</l>
  </lg>
</div>
```

**Attributes**:
- `n`: Psalm number
- `type="verse"`: Individual verse
- `type="doxology"`: Gloria Patri ending
- `*`: Flex/mediant marker (preserved in text)

### Hymns

```xml
<div type="hymn" xml:id="hymn-vesp">
  <head>Hymnus</head>

  <!-- Optional rubric for tone -->
  <note type="tone">
    <ref target="chant:tone-viii">Tonus VIII</ref>
  </note>

  <lg type="stanza" n="1">
    <l>Jesu, Redémptor ómnium,</l>
    <l>Quem lucis ante oríginem</l>
    <l>Parem patérnæ glóriæ</l>
    <l>Pater suprémæ éxtulit.</l>
  </lg>

  <lg type="stanza" n="2">
    <l>Tu lumen, tu splendor Patris,</l>
    <l>Tu spes perénnis ómnium,</l>
    <l>Inténde quas fundunt preces</l>
    <l>Tui per orbem sérvuli.</l>
  </lg>

  <lg type="stanza" n="3">
    <l>Meménto, rerum Cónditor,</l>
    <l>Nostri quod olim córporis,</l>
    <l>Sacráta ab alvo Vírginis</l>
    <l>Nascéndo formam súmpseris.</l>
  </lg>

  <lg type="doxology">
    <l>Glória tibi, Dómine,</l>
    <l>Qui natus es de Vírgine,</l>
    <l>Cum Patre et Sancto Spíritu,</l>
    <l>In sempitérna sǽcula. Amen.</l>
  </lg>
</div>
```

**Attributes**:
- `type="stanza"`: Regular stanzas
- `type="doxology"`: Final doxological stanza
- `n`: Stanza number

### Readings (Lectiones)

```xml
<div type="reading" n="4" xml:id="lect4">
  <head>Lectio iv</head>

  <div type="source">
    <bibl>
      <author>Sanctus Leo Papa</author>
      <title>Sermo 7 de Nativitate Domini</title>
    </bibl>
  </div>

  <p n="1">
    Festivitátis hodiérnæ, dilectíssimi,
    verus venerátor est, et pius cultor,
    qui nec de Incarnatióne Dómini áliquid falsum,
    nec de Deitáte áliquid sentit indígnum.
  </p>

  <p n="2">
    Paris enim perículi malum est,
    si illi aut natúræ nostræ véritas,
    aut Patérnæ glóriæ negátur æquálitas.
  </p>

  <p n="3">
    Cum ergo ad intellegéndum sacraméntum nativitátis Christi,
    qua de Matre vírgine est ortus, accédimus,
    abigátur procul terrenárum calígo ratiónum,
    et ab illuminátæ fídei óculo mundánæ sapiéntiæ fumus abscédat.
  </p>
</div>
```

**Attributes**:
- `n`: Reading number (1-9)
- `type="source"`: Source citation
- `<bibl>`: Bibliographic information
- `<p n="">`: Paragraph number within reading

**For Scripture Readings**:
```xml
<div type="reading" n="1" xml:id="lect1">
  <head>Lectio i</head>

  <div type="source">
    <bibl>
      <title>Liber Isaiae Prophetae</title>
      <biblScope unit="chapter" from="9" to="9">Cap. 9</biblScope>
      <biblScope unit="verse" from="1" to="6">1-6</biblScope>
    </bibl>
  </div>

  <p>
    <seg type="rubric">In illo témpore:</seg>
    <quote>
      Pópulus, qui ambulábat in ténebris, vidit lucem magnam;
      habitántibus in regióne umbræ mortis, lux orta est eis.
    </quote>
  </p>
</div>
```

### Responsories

```xml
<div type="responsory" n="1" xml:id="resp1">
  <div type="response" subtype="initial">
    <label>℟.</label>
    <p>
      Hodie nobis cælórum Rex
      de Vírgine nasci dignátus est,
      ut hóminem pérditum ad cæléstia regna revocáret:
      <seg type="asterisk">*</seg>
      Gaudet exércitus Angelórum:
      quia salus ætérna humáno géneri appáruit.
    </p>
  </div>

  <div type="verse">
    <label>℣.</label>
    <p>
      Glória in excélsis Deo,
      et in terra pax homínibus bonæ voluntátis.
    </p>
  </div>

  <div type="response" subtype="repetition">
    <label>℟.</label>
    <p>
      Gaudet exércitus Angelórum:
      quia salus ætérna humáno géneri appáruit.
    </p>
  </div>

  <!-- For final responsory of nocturn, add Gloria -->
  <div type="gloria">
    <label>℣.</label>
    <p>Glória Patri, et Fílio, et Spirítui Sancto.</p>
  </div>

  <div type="response" subtype="final">
    <label>℟.</label>
    <p>
      Gaudet exércitus Angelórum:
      quia salus ætérna humáno géneri appáruit.
    </p>
  </div>
</div>
```

**Attributes**:
- `subtype="initial"`: Full first response
- `subtype="repetition"`: Repeated portion after verse
- `subtype="final"`: After Gloria (if present)
- `type="asterisk"`: Marks the repetition point

### Short Responsories (Responsoria Brevia)

```xml
<div type="responsory" subtype="brief" xml:id="resp-br-terce">
  <label>℟. br.</label>

  <p n="1">
    Christus natus est nobis,
    <seg type="asterisk">*</seg>
    Veníte, adorémus.
  </p>

  <p n="2">
    Christus natus est nobis,
    <seg type="asterisk">*</seg>
    Veníte, adorémus.
  </p>

  <div type="verse">
    <label>℣.</label>
    <p>Deus homo factus est, et in ætérnum pérmanet.</p>
  </div>

  <div type="response">
    <label>℟.</label>
    <p>Veníte, adorémus.</p>
  </div>

  <div type="gloria">
    <label>℣.</label>
    <p>Glória Patri, et Fílio, et Spirítui Sancto.</p>
  </div>

  <div type="response">
    <label>℟.</label>
    <p>
      Christus natus est nobis,
      <seg type="asterisk">*</seg>
      Veníte, adorémus.
    </p>
  </div>
</div>
```

### Versicles

```xml
<div type="versicle" xml:id="vers-vesp">
  <label>℣.</label>
  <p>Notum fecit Dóminus, allelúja.</p>

  <label>℟.</label>
  <p>Salutáre suum, allelúja.</p>
</div>
```

### Collects (Orations)

```xml
<div type="collect" xml:id="collect-main">
  <head>Oratio</head>

  <p>
    <seg type="invocation">Deus,</seg>
    qui hanc sacratíssimam noctem
    veri lúminis fecísti illustratióne claréscere:
    da, quǽsumus; ut, cujus lucis mystéria in terra cognóvimus,
    ejus quoque gáudiis in cælo perfruámur:
  </p>

  <p type="conclusion">
    <seg type="mediator">Qui tecum vivit et regnat
    in unitáte Spíritus Sancti, Deus,</seg>
    per ómnia sǽcula sæculórum.
  </p>

  <p>
    <label>℟.</label>
    Amen.
  </p>
</div>
```

**Alternative with Reference**:
```xml
<div type="collect">
  <ref target="commune:C1:collect">
    Same as Commune of Apostles
  </ref>
</div>
```

### Canticles (Benedictus, Magnificat, Nunc Dimittis)

```xml
<div type="canticle" subtype="benedictus" xml:id="cant-bened">
  <div type="antiphon" xml:id="ant-bened">
    <label>Ant.</label>
    <p>
      Glória in excélsis Deo, *
      et in terra pax homínibus bonæ voluntátis,
      allelúja, allelúja.
    </p>
  </div>

  <div type="canticle-text">
    <head>Canticum Zachariæ</head>
    <head type="incipit">Benedictus Dominus Deus Israel</head>

    <!-- Option 1: Reference -->
    <ref target="psalterium:benedictus"/>

    <!-- Option 2: Full text -->
    <lg type="verse" n="1">
      <l>Benedíctus Dóminus, Deus Israël, *</l>
      <l>quia visitávit et fecit redemptiónem plebis suæ:</l>
    </lg>

    <lg type="verse" n="2">
      <l>Et eréxit cornu salútis nobis: *</l>
      <l>in domo David, púeri sui.</l>
    </lg>

    <!-- More verses -->

    <lg type="doxology">
      <l>Glória Patri, et Fílio, *</l>
      <l>et Spirítui Sancto.</l>
      <l>Sicut erat in princípio, et nunc, et semper, *</l>
      <l>et in sǽcula sæculórum. Amen.</l>
    </lg>
  </div>

  <div type="antiphon" corresp="#ant-bened">
    <label>Ant.</label>
    <p>
      Glória in excélsis Deo,
      et in terra pax homínibus bonæ voluntátis,
      allelúja, allelúja.
    </p>
  </div>
</div>
```

---

## Special Features

### Version-Specific Content

Use `@source` attribute to indicate which rubrics the content applies to:

```xml
<div type="reading" n="1" source="#brev1962">
  <head>Lectio i</head>
  <p>Reading text for 1962 rubrics...</p>
</div>

<div type="reading" n="1" source="#brev1570">
  <head>Lectio i</head>
  <p>Different reading text for 1570 rubrics...</p>
</div>
```

**Alternative: Using Choice**:
```xml
<choice>
  <seg source="#brev1962">
    Festivitátis hodiérnæ, dilectíssimi...
  </seg>
  <seg source="#brev1570">
    Hodiérna die, caríssimi...
  </seg>
</choice>
```

### Cross-References

**Reference to Another Office**:
```xml
<div type="hymn">
  <ref target="tempora:Nat1-0:hymn-vesp">
    Same as First Vespers of Christmas
  </ref>
</div>
```

**Reference to Commune**:
```xml
<div type="collect">
  <ref target="commune:C1:collect-main">
    Ex Communi Apostolorum
  </ref>
</div>
```

**Reference to Psalterium**:
```xml
<div type="psalm" n="109">
  <ref target="psalterium:ps-109"/>
</div>
```

### Conditional Content (Alleluia)

```xml
<p>
  Christus natus est nobis
  <seg type="alleluia" source="#season-christmas">
    , allelúja, allelúja
  </seg>
  .
</p>
```

Or using `<choice>`:
```xml
<p>
  Christus natus est nobis
  <choice>
    <seg source="#season-lent"></seg>
    <seg source="#season-easter">, allelúja, allelúja</seg>
  </choice>
  .
</p>
```

### Rubrics (Liturgical Directions)

```xml
<div type="rubric">
  <p>
    <hi rend="red">
      Post Benedictus non dicitur Fidelium animae.
    </hi>
  </p>
</div>
```

Or inline:
```xml
<p>
  <seg type="rubric">In illo témpore:</seg>
  Pópulus, qui ambulábat in ténebris...
</p>
```

### Musical Notation (GABC)

```xml
<div type="antiphon" n="1">
  <label>Ant. 1</label>

  <!-- Text -->
  <p xml:id="ant-text-1">
    Dóminus dixit ad me: Fílius meus es tu,
    ego hódie génui te.
  </p>

  <!-- GABC notation -->
  <notatedMusic xml:id="ant-gabc-1">
    <ptr target="gabc:dominus-dixit"/>
    <desc>GABC notation for this antiphon</desc>

    <!-- Or embed directly -->
    <ab type="gabc">
      name: Dominus dixit;
      mode: 8;
      %%
      (c4) Dó(f)mi(g)nus(h) di(g)xit(f) ad(e) me:(d)
      Fí(f)li(g)us(h) me(g)us(f) es(e) tu,(d)
      e(f)go(g) hó(h)di(g)e(f) gé(e)nu(d)i(c) te.(d)
    </ab>
  </notatedMusic>
</div>
```

### Commemorations

```xml
<div type="commemoration" xml:id="comm-stephen">
  <head>Commemoratio S. Stephani Protomartyris</head>

  <div type="antiphon">
    <label>Ant.</label>
    <p>Stephanus autem plenus grátia et fortitúdine...</p>
  </div>

  <div type="versicle">
    <label>℣.</label>
    <p>Glória et honóre coronásti eum, Dómine.</p>
    <label>℟.</label>
    <p>Et constituísti eum super ópera mánuum tuárum.</p>
  </div>

  <div type="collect">
    <p>Da nobis, quǽsumus, Dómine...</p>
  </div>
</div>
```

### Parallel Texts (Multiple Languages)

**Option 1: Separate Files with Linking**:
```xml
<!-- 12-25.xml (Latin) -->
<TEI xml:id="sancti-12-25-la" xml:lang="la">
  <teiHeader>
    <xenoData>
      <relation type="translation" target="sancti-12-25-en"/>
      <relation type="translation" target="sancti-12-25-fr"/>
    </xenoData>
  </teiHeader>
  <text>...</text>
</TEI>
```

**Option 2: Parallel Text in Single File**:
```xml
<div type="reading" n="1">
  <head>Lectio i</head>

  <div xml:lang="la">
    <p>Festivitátis hodiérnæ, dilectíssimi...</p>
  </div>

  <div xml:lang="en" type="translation">
    <p>The true worshiper and devout celebrant
       of today's feast, beloved...</p>
  </div>
</div>
```

---

## Complete Examples

### Complete Sanctoral Office (Christmas - 12-25.xml)

See separate file: `examples/sancti-12-25.xml` (Due to length, providing structure reference)

**File would include**:
- Complete teiHeader with all metadata
- Matins with 3 Nocturns, 9 lessons, 9 responsories
- Lauds with psalms, canticle, Benedictus
- Little Hours (Prime, Terce, Sext, None)
- Vespers with Magnificat
- Compline
- All antiphons, hymns, versicles, collects

### Complete Temporal Office (Trinity Sunday - Pent01-0.xml)

**Structure**:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="tempora-Pent01-0">
  <teiHeader>
    <!-- Metadata for Trinity Sunday -->
  </teiHeader>

  <text xml:lang="la">
    <body>
      <div type="office">
        <head>Dominica Sanctissimæ Trinitatis</head>

        <!-- Rank and rules -->
        <div type="metadata">
          <ab type="rank" n="6.5">Duplex I classis</ab>
          <ab type="rules">
            <list>
              <item>9 lectiones</item>
              <item>Psalmi Dominica</item>
              <item>Symbolum Athanasium</item>
            </list>
          </ab>
        </div>

        <!-- All canonical hours -->
        <div type="hour" subtype="vespers" n="1">
          <!-- First Vespers -->
        </div>

        <div type="hour" subtype="matins">
          <!-- Matins with Athanasian Creed -->
        </div>

        <div type="hour" subtype="lauds">
          <!-- Lauds -->
        </div>

        <!-- ... other hours ... -->

      </div>
    </body>
  </text>
</TEI>
```

### Commune Office (C1 - Apostles)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="commune-C1">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>Commune Apostolorum</title>
        <title type="vernacular" xml:lang="en">Common of Apostles</title>
      </titleStmt>
      <!-- ... -->
    </fileDesc>
  </teiHeader>

  <text xml:lang="la">
    <body>
      <div type="commune">
        <head>Commune Apostolorum</head>

        <!-- Provide components that can be referenced -->
        <div type="hour" subtype="vespers" xml:id="C1-vespers">
          <!-- Vespers for Apostles -->
        </div>

        <div type="hour" subtype="matins" xml:id="C1-matins">
          <!-- Matins for Apostles -->
        </div>

        <!-- ... -->
      </div>
    </body>
  </text>
</TEI>
```

---

## XML Schema (RelaxNG)

### Schema Definition

```xml
<?xml version="1.0" encoding="UTF-8"?>
<grammar xmlns="http://relaxng.org/ns/structure/1.0"
         xmlns:a="http://relaxng.org/ns/compatibility/annotations/1.0"
         datatypeLibrary="http://www.w3.org/2001/XMLSchema-datatypes"
         ns="http://www.tei-c.org/ns/1.0">

  <start>
    <ref name="TEI"/>
  </start>

  <!-- TEI root element -->
  <define name="TEI">
    <element name="TEI">
      <attribute name="xml:id">
        <data type="ID"/>
      </attribute>
      <optional>
        <attribute name="xml:lang">
          <data type="language"/>
        </attribute>
      </optional>
      <ref name="teiHeader"/>
      <ref name="text"/>
    </element>
  </define>

  <!-- Header -->
  <define name="teiHeader">
    <element name="teiHeader">
      <ref name="fileDesc"/>
      <optional><ref name="encodingDesc"/></optional>
      <optional><ref name="profileDesc"/></optional>
      <optional><ref name="revisionDesc"/></optional>
    </element>
  </define>

  <!-- ... (full schema would be extensive) -->

  <!-- Liturgical Hour -->
  <define name="hour">
    <element name="div">
      <attribute name="type">
        <value>hour</value>
      </attribute>
      <attribute name="subtype">
        <choice>
          <value>matins</value>
          <value>lauds</value>
          <value>prime</value>
          <value>terce</value>
          <value>sext</value>
          <value>none</value>
          <value>vespers</value>
          <value>compline</value>
        </choice>
      </attribute>
      <attribute name="xml:id">
        <data type="ID"/>
      </attribute>

      <element name="head">
        <text/>
      </element>

      <zeroOrMore>
        <choice>
          <ref name="antiphon"/>
          <ref name="psalm"/>
          <ref name="hymn"/>
          <ref name="reading"/>
          <ref name="responsory"/>
          <ref name="versicle"/>
          <ref name="collect"/>
          <ref name="canticle"/>
        </choice>
      </zeroOrMore>
    </element>
  </define>

  <!-- Antiphon -->
  <define name="antiphon">
    <element name="div">
      <attribute name="type">
        <value>antiphon</value>
      </attribute>
      <optional>
        <attribute name="n">
          <data type="positiveInteger"/>
        </attribute>
      </optional>
      <optional>
        <attribute name="xml:id">
          <data type="ID"/>
        </attribute>
      </optional>

      <optional>
        <element name="label">
          <text/>
        </element>
      </optional>

      <oneOrMore>
        <element name="p">
          <ref name="textContent"/>
        </element>
      </oneOrMore>
    </element>
  </define>

  <!-- Text content (mixed content with markup) -->
  <define name="textContent">
    <zeroOrMore>
      <choice>
        <text/>
        <ref name="seg"/>
        <ref name="ref"/>
        <ref name="hi"/>
      </choice>
    </zeroOrMore>
  </define>

  <!-- ... more definitions ... -->

</grammar>
```

### Validation

**Using lxml (Python)**:
```python
from lxml import etree

# Load schema
schema_doc = etree.parse('schema/divinum-officium.rng')
relaxng = etree.RelaxNG(schema_doc)

# Load and validate TEI file
tei_doc = etree.parse('data/offices/sanctoral/12-25.xml')
is_valid = relaxng.validate(tei_doc)

if not is_valid:
    print("Validation errors:")
    print(relaxng.error_log)
else:
    print("Valid TEI document")
```

**Using Oxygen XML Editor**:
1. Open TEI file
2. Associate with RelaxNG schema
3. Automatic validation with error highlighting

---

## Migration Mapping

### From Current Format to TEI

#### Current Text Format

```
[Rank]
In Nativitate Domini;;Duplex I classis;;7.0;;ex Sancti/12-25

[Rule]
9 lectiones
Psalmi Dominica
No Commemoration

[Ant Vespera]
O admirábile commércium: * Creátor géneris humáni...;;109
Quando natus es * ineffabíliter ex Vírgine...;;112

[Hymnus Vespera]
v. Jesu, Redémptor ómnium,
Quem lucis ante oríginem
Parem patérnæ glóriæ
Pater suprémæ éxtulit.
_
Te mane laudum cármine...

[Lectio4]
Sermo sancti Leónis Papæ
!Sermo 7 de Nativitate Domini
Festivitátis hodiérnæ, dilectíssimi...

[Responsory4]
R. Congratulámini mihi, omnes qui dilígitis Dóminum:
* Quia, cum essem párvula, plácui Altíssimo...
V. Beátam me dicent omnes generatiónes...
R. Quia, cum essem párvula...
```

#### TEI Equivalent

```xml
<!-- Rank -->
<div type="metadata">
  <ab type="rank" n="7.0">
    <seg type="class">Duplex I classis</seg>
  </ab>
  <ab type="reference">
    <ref target="sancti:12-25">ex Sancti/12-25</ref>
  </ab>
</div>

<!-- Rule -->
<div type="metadata">
  <ab type="rules">
    <list>
      <item>9 lectiones</item>
      <item>Psalmi Dominica</item>
      <item>No Commemoration</item>
    </list>
  </ab>
</div>

<!-- Antiphons -->
<div type="antiphon" n="1">
  <label>Ant. 1</label>
  <p>O admirábile commércium: * Creátor géneris humáni...</p>
  <note type="psalm"><ref target="#ps-109">Psalm 109</ref></note>
</div>

<div type="antiphon" n="2">
  <label>Ant. 2</label>
  <p>Quando natus es * ineffabíliter ex Vírgine...</p>
  <note type="psalm"><ref target="#ps-112">Psalm 112</ref></note>
</div>

<!-- Hymn -->
<div type="hymn">
  <lg type="stanza" n="1">
    <l>Jesu, Redémptor ómnium,</l>
    <l>Quem lucis ante oríginem</l>
    <l>Parem patérnæ glóriæ</l>
    <l>Pater suprémæ éxtulit.</l>
  </lg>
  <lg type="stanza" n="2">
    <l>Te mane laudum cármine...</l>
  </lg>
</div>

<!-- Reading -->
<div type="reading" n="4">
  <head>Lectio iv</head>
  <div type="source">
    <bibl>
      <author>Sanctus Leo Papa</author>
      <title>Sermo 7 de Nativitate Domini</title>
    </bibl>
  </div>
  <p>Festivitátis hodiérnæ, dilectíssimi...</p>
</div>

<!-- Responsory -->
<div type="responsory" n="4">
  <div type="response" subtype="initial">
    <label>℟.</label>
    <p>Congratulámini mihi, omnes qui dilígitis Dóminum:
       <seg type="asterisk">*</seg>
       Quia, cum essem párvula, plácui Altíssimo...</p>
  </div>
  <div type="verse">
    <label>℣.</label>
    <p>Beátam me dicent omnes generatiónes...</p>
  </div>
  <div type="response" subtype="repetition">
    <label>℟.</label>
    <p>Quia, cum essem párvula...</p>
  </div>
</div>
```

### Conversion Script (Python)

```python
import re
from lxml import etree

def convert_text_to_tei(text_file_path, output_path):
    """Convert old format text file to TEI XML"""

    # Parse text file into sections
    sections = parse_text_file(text_file_path)

    # Create TEI document
    TEI = etree.Element(
        'TEI',
        xmlns="http://www.tei-c.org/ns/1.0",
        attrib={'{http://www.w3.org/XML/1998/namespace}id': extract_office_id(text_file_path)}
    )

    # Build header
    header = build_tei_header(sections)
    TEI.append(header)

    # Build text body
    text = etree.SubElement(TEI, 'text', attrib={'{http://www.w3.org/XML/1998/namespace}lang': 'la'})
    body = etree.SubElement(text, 'body')
    office_div = etree.SubElement(body, 'div', type='office')

    # Convert sections
    if 'Rank' in sections:
        metadata_div = convert_rank(sections['Rank'])
        office_div.append(metadata_div)

    if 'Rule' in sections:
        rules_div = convert_rules(sections['Rule'])
        office_div.append(rules_div)

    # Convert hours
    for hour in ['Vespera', 'Matutinum', 'Laudes', 'Prima', 'Tertia', 'Sexta', 'Nona', 'Completorium']:
        hour_div = convert_hour(sections, hour)
        if hour_div is not None:
            office_div.append(hour_div)

    # Write output
    tree = etree.ElementTree(TEI)
    tree.write(
        output_path,
        encoding='UTF-8',
        xml_declaration=True,
        pretty_print=True
    )

def parse_text_file(file_path):
    """Parse text file into sections"""
    sections = {}
    current_section = None
    current_content = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Section header
            if line.startswith('[') and line.rstrip().endswith(']'):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line.strip()[1:-1]
                current_content = []
            else:
                current_content.append(line.rstrip())

        # Last section
        if current_section:
            sections[current_section] = '\n'.join(current_content)

    return sections

def convert_rank(rank_text):
    """Convert [Rank] section to TEI"""
    # Parse: "Name;;Class;;Numeric;;Reference"
    parts = rank_text.strip().split(';;')

    metadata_div = etree.Element('div', type='metadata')

    rank_ab = etree.SubElement(metadata_div, 'ab', type='rank', n=parts[2] if len(parts) > 2 else '1.0')

    if len(parts) > 1:
        class_seg = etree.SubElement(rank_ab, 'seg', type='class')
        class_seg.text = parts[1]

    if len(parts) > 3 and parts[3]:
        ref_ab = etree.SubElement(metadata_div, 'ab', type='reference')
        ref_elem = etree.SubElement(ref_ab, 'ref', target=parts[3].replace(' ', ':'))
        ref_elem.text = parts[3]

    return metadata_div

def convert_hymn(hymn_text):
    """Convert hymn text to TEI"""
    hymn_div = etree.Element('div', type='hymn')

    stanzas = hymn_text.split('_\n')
    for i, stanza_text in enumerate(stanzas, 1):
        lines = [l.strip() for l in stanza_text.strip().split('\n') if l.strip()]

        # Skip 'v.' prefix
        if lines and lines[0].startswith('v. '):
            lines[0] = lines[0][3:]

        stanza_type = 'doxology' if i == len(stanzas) else 'stanza'
        lg = etree.SubElement(hymn_div, 'lg', type=stanza_type, n=str(i))

        for line in lines:
            l_elem = etree.SubElement(lg, 'l')
            l_elem.text = line

    return hymn_div

# ... more conversion functions ...
```

---

## Query Examples

### XPath Queries

**Find all Duplex I classis feasts**:
```xpath
//div[@type='metadata']/ab[@type='rank' and @n >= 6.0]
```

**Get all antiphons for Vespers**:
```xpath
//div[@type='hour'][@subtype='vespers']//div[@type='antiphon']
```

**Find all readings from St. Leo**:
```xpath
//div[@type='reading']//bibl[author='Sanctus Leo Papa']
```

**Get Christmas office title**:
```xpath
//TEI[@xml:id='sancti-12-25']//head[1]/text()
```

**Find all offices with Te Deum**:
```xpath
//div[@type='canticle'][@subtype='te-deum']/ancestor::TEI/@xml:id
```

### XQuery Examples

**List all feasts by rank**:
```xquery
for $office in //TEI
let $rank := $office//ab[@type='rank']/@n
order by $rank descending
return <feast rank="{$rank}">
  {$office//titleStmt/title[@type='main']/text()}
</feast>
```

**Extract all hymns for a specific hour**:
```xquery
for $hymn in //div[@type='hour'][@subtype='lauds']//div[@type='hymn']
return $hymn
```

**Count readings per office**:
```xquery
for $office in //TEI
return <office id="{$office/@xml:id}">
  <reading-count>
    {count($office//div[@type='reading'])}
  </reading-count>
</office>
```

---

## Conclusion

This TEI data model provides:

✅ **Semantic Structure**: Captures liturgical meaning, not just formatting
✅ **Validation**: XML schema ensures consistency
✅ **Flexibility**: Supports version variants, multiple languages, annotations
✅ **Queryability**: XPath/XQuery enable complex searches
✅ **Preservation**: Long-term archival quality
✅ **Interoperability**: Standard format for liturgical scholarship
✅ **Transformation**: Can generate HTML, PDF, ePub, JSON

**Next Steps**:
1. Review and refine schema
2. Create complete example files
3. Build conversion tools
4. Validate with TEI experts
5. Begin pilot conversion

---

**Document Version**: 1.0
**Last Updated**: 2025-12-28
**Author**: Claude (Sonnet 4.5)
**For**: Divinum Officium TEI Migration
