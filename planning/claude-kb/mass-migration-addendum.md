# Mass (Missa) Migration - Addendum to Main Proposal

## Executive Summary

This document extends the main migration proposal to explicitly cover the **Mass (Missa)** component of Divinum Officium. While the main proposal focused on the Divine Office (Horas), the project also includes a comprehensive Mass module with similar data structures and migration needs.

**Key Finding**: The Mass migration can follow the same architectural approach as the Divine Office, with specific adaptations for Mass structure and propers.

---

## Current Mass Implementation

### Directory Structure

```
web/www/missa/
├── Latin/
│   ├── Tempora/          # Temporal cycle Masses (Sundays, seasons)
│   ├── Sancti/           # Sanctoral cycle Masses (Saints' feasts)
│   ├── Commune/          # Common Masses (martyrs, virgins, etc.)
│   └── Ordo/             # Mass structure and ordinary
│       ├── Ordo.txt      # Standard Roman Rite
│       ├── Ordo67.txt    # 1967 modifications
│       ├── OrdoM.txt     # Monastic
│       ├── OrdoOP.txt    # Dominican
│       ├── Prefationes.txt
│       ├── Prayers.txt
│       └── Propers.txt
├── English/
├── Francais/
└── ... (other languages)

web/cgi-bin/missa/
├── missa.pl              # Main Mass script
├── Cmissa.pl             # Common functions
├── Emissa.pl             # Additional functions
├── ordo.pl               # Ordo handling
└── propers.pl            # Propers selection
```

### Mass File Structure Example

```
[Rank]
In Nativitate Domini;;Duplex I Classis;;6.5

[Rule]
celebranda aut missa prima aut missa secunda aut missa tertia

[Introitus]
Puer natus est nobis, et fílius datus est nobis...

[Graduale]
Viderunt omnes fines terræ salutare Dei nostri...

[Alleluia]
Alleluia, alleluia. V. Dominus regnavit...

[Tractus]
(Lent only - replaces Alleluia)

[Sequentia]
(Special sequences like Dies Irae, Stabat Mater)

[Offertorium]
Tui sunt cæli, et tua est terra...

[Secreta]
Oblata, Domine, munera...

[Communio]
Viderunt omnes fines terræ...

[Postcommunio]
Præsta, quæsumus, omnipotens Deus...

[Lectio]
(Epistle reading)

[Evangelium]
(Gospel reading)
```

### Similarities with Divine Office

Both Mass and Divine Office share:
- Similar file structure (Tempora, Sancti, Commune)
- Same special characters (@, $, #, !, ~)
- Same precedence/ranking system
- Same version/rubric variants (1570, 1960, etc.)
- Same multi-language support
- Similar cross-referencing mechanisms

### Differences from Divine Office

Mass-specific features:
- **Multiple Masses per day**: Christmas has three Masses (midnight, dawn, day)
- **Propers vs. Ordinary**:
  - Ordinary (Kyrie, Gloria, Credo, Sanctus, Agnus Dei) - fixed
  - Propers (Introit, Gradual, Offertory, Communion) - vary by day
- **Lectionary**: Epistles and Gospels
- **Prefaces**: Special prefaces for different seasons/feasts
- **Votive Masses**: Masses for special intentions
- **Requiem Masses**: Funeral and memorial Masses
- **Ordo structure**: More complex ceremonial directions

---

## TEI Data Model for Mass

### Overall Mass Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="missa-12-25">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title type="main" xml:lang="la">Missa in Nativitate Domini</title>
        <title type="sub" xml:lang="en">Mass of the Nativity of Our Lord</title>
      </titleStmt>
      <!-- Similar header structure to Divine Office -->
    </fileDesc>

    <profileDesc>
      <textClass>
        <keywords scheme="#liturgical-rank">
          <term ref="#rank-duplex-i">Duplex I classis</term>
        </keywords>
        <keywords scheme="#liturgical-type">
          <term>Festive Mass</term>
          <term>Mass of the Lord</term>
        </keywords>
      </textClass>
    </profileDesc>
  </teiHeader>

  <text xml:lang="la">
    <body>
      <div type="mass" xml:id="mass-nativity">
        <head>In Nativitate Domini</head>

        <!-- Metadata -->
        <div type="metadata">
          <ab type="rank" n="6.5">
            <seg type="class">Duplex I Classis</seg>
          </ab>

          <ab type="rule">
            <list>
              <item>celebranda aut missa prima aut missa secunda aut missa tertia</item>
              <item>Gloria</item>
              <item>Credo</item>
            </list>
          </ab>
        </div>

        <!-- Multiple Masses (Christmas special case) -->
        <div type="mass-celebration" n="1" xml:id="mass-midnight">
          <head>Missa in Nocte (Ad Galli Cantum)</head>
          <note type="time">At Midnight</note>

          <!-- Mass Propers -->
          <div type="propers">
            <!-- Introit, Collect, Epistle, Gospel, etc. -->
          </div>
        </div>

        <div type="mass-celebration" n="2" xml:id="mass-dawn">
          <head>Missa in Aurora</head>
          <note type="time">At Dawn</note>

          <div type="propers">
            <!-- Different propers -->
          </div>
        </div>

        <div type="mass-celebration" n="3" xml:id="mass-day">
          <head>Missa in Die</head>
          <note type="time">During the Day</note>

          <div type="propers">
            <!-- Different propers -->
          </div>
        </div>

      </div>
    </body>
  </text>
</TEI>
```

### Mass Propers Encoding

```xml
<div type="propers">

  <!-- Introit -->
  <div type="introit" xml:id="introit-nativity">
    <head>Introitus</head>

    <div type="source">
      <bibl>
        <ref target="bible:is9:6">Isaias 9:6</ref>
      </bibl>
    </div>

    <div type="antiphon">
      <p>
        Puer natus est nobis, et fílius datus est nobis:
        cuius impérium super húmerum eius:
        et vocábitur nomen eius, magni consílii Angelus.
      </p>
    </div>

    <div type="psalm" n="97">
      <head>Ps. 97:1</head>
      <lg type="verse">
        <l>Cantáte Dómino cánticum novum: *</l>
        <l>quia mirabília fecit.</l>
      </lg>
    </div>

    <div type="gloria-patri">
      <lg>
        <l>Glória Patri, et Fílio, *</l>
        <l>et Spirítui Sancto.</l>
        <l>Sicut erat in princípio, et nunc, et semper, *</l>
        <l>et in sǽcula sæculórum. Amen.</l>
      </lg>
    </div>

    <!-- Repeat antiphon -->
    <div type="antiphon" corresp="#introit-antiphon">
      <p>Puer natus est nobis...</p>
    </div>
  </div>

  <!-- Collect (Oratio) -->
  <div type="collect" xml:id="collect-nativity">
    <head>Oratio</head>

    <p>
      <label>℣.</label>
      Dóminus vobíscum.
    </p>
    <p>
      <label>℟.</label>
      Et cum spíritu tuo.
    </p>
    <p>
      <label>℣.</label>
      Orémus.
    </p>

    <p type="prayer">
      Deus, qui hanc sacratíssimam noctem
      veri lúminis fecísti illustratióne claréscere:
      da, quǽsumus; ut, cuius lucis mystéria in terra cognóvimus,
      eius quoque gáudiis in cælo perfruámur:
    </p>

    <p type="conclusion">
      Qui tecum vivit et regnat in unitáte Spíritus Sancti, Deus,
      per ómnia sǽcula sæculórum.
    </p>

    <p>
      <label>℟.</label>
      Amen.
    </p>
  </div>

  <!-- Epistle -->
  <div type="epistle" xml:id="epistle-nativity">
    <head>Epistola</head>

    <div type="source">
      <bibl>
        <title>Epistola beati Pauli Apostoli ad Titum</title>
        <biblScope unit="chapter" from="2" to="2">2</biblScope>
        <biblScope unit="verse" from="11" to="15">11-15</biblScope>
      </bibl>
    </div>

    <p>
      <seg type="rubric">Caríssime:</seg>
      <quote>
        Appáruit grátia Dei Salvatóris nostri ómnibus homínibus,
        erúdiens nos, ut, abnegántes impietátem et sæculária desidéria,
        sóbrie et iuste et pie vivámus in hoc sǽculo,
        exspectántes beátam spem et advéntum glóriæ magni Dei
        et Salvatóris nostri Jesu Christi:
        qui dedit semetípsum pro nobis:
        ut nos redímeret ab omni iniquitáte,
        et mundáret sibi pópulum acceptábilem, sectatórem bonórum óperum.
      </quote>
    </p>

    <p>
      <label>℟.</label>
      Deo grátias.
    </p>
  </div>

  <!-- Gradual -->
  <div type="gradual" xml:id="gradual-nativity">
    <head>Graduale</head>

    <div type="source">
      <bibl>
        <ref target="bible:ps97:3-2">Ps. 97:3, 2</ref>
      </bibl>
    </div>

    <div type="response">
      <p>
        Vidérunt omnes fines terræ salutáre Dei nostri:
        iubiláte Deo, omnis terra.
      </p>
    </div>

    <div type="verse">
      <label>℣.</label>
      <p>
        Notum fecit Dóminus salutáre suum:
        ante conspéctum géntium revelávit iustítiam suam.
      </p>
    </div>
  </div>

  <!-- Alleluia -->
  <div type="alleluia" xml:id="alleluia-nativity">
    <head>Alleluia</head>

    <div type="response">
      <p>Alleluia, alleluia.</p>
    </div>

    <div type="verse">
      <label>℣.</label>
      <bibl>
        <ref target="bible:ps2:7">Ps. 2:7</ref>
      </bibl>
      <p>
        Dóminus dixit ad me: Fílius meus es tu,
        ego hódie génui te.
      </p>
    </div>

    <div type="response">
      <p>Alleluia.</p>
    </div>
  </div>

  <!-- Gospel -->
  <div type="gospel" xml:id="gospel-nativity">
    <head>Evangelium</head>

    <div type="introduction">
      <p>
        <label>℣.</label>
        Dóminus vobíscum.
      </p>
      <p>
        <label>℟.</label>
        Et cum spíritu tuo.
      </p>
    </div>

    <div type="source">
      <p>
        <label>℣.</label>
        Inítium sancti Evangélii secúndum Joánnem.
      </p>
      <bibl>
        <title>Evangelium secundum Joannem</title>
        <biblScope unit="chapter" from="1" to="1">1</biblScope>
        <biblScope unit="verse" from="1" to="14">1-14</biblScope>
      </bibl>
      <p>
        <label>℟.</label>
        Glória tibi, Dómine.
      </p>
    </div>

    <div type="text">
      <p>
        <seg type="rubric">In illo témpore:</seg>
        <quote>
          In princípio erat Verbum, et Verbum erat apud Deum,
          et Deus erat Verbum.
          Hoc erat in princípio apud Deum.
          Omnia per ipsum facta sunt:
          et sine ipso factum est nihil, quod factum est:
          in ipso vita erat, et vita erat lux hóminum:
          et lux in ténebris lucet, et ténebræ eam non comprehendérunt.
        </quote>
        <!-- More verses -->
        <quote>
          <seg type="genuflection">Et Verbum caro factum est,</seg>
          et habitávit in nobis:
          et vídimus glóriam eius, glóriam quasi Unigéniti a Patre,
          plenum grátiæ et veritátis.
        </quote>
      </p>
    </div>

    <p>
      <label>℟.</label>
      Laus tibi, Christe.
    </p>
  </div>

  <!-- Offertory -->
  <div type="offertory" xml:id="offertory-nativity">
    <head>Offertorium</head>

    <div type="source">
      <bibl>
        <ref target="bible:ps88:12-15">Ps. 88:12, 15</ref>
      </bibl>
    </div>

    <p>
      Tui sunt cæli, et tua est terra,
      orbem terrárum et plenitúdinem eius tu fundásti:
      iustítia et iudícium præparátio sedis tuæ.
    </p>
  </div>

  <!-- Secret -->
  <div type="secret" xml:id="secret-nativity">
    <head>Secreta</head>

    <p>
      Oblata, Dómine, múnera, nova Unigéniti tui Nativitáte sanctífica:
      nosque a peccatórum nostrórum máculis emúnda.
    </p>

    <p type="conclusion">
      Per eúndem Dóminum nostrum Jesum Christum, Fílium tuum:
      qui tecum vivit et regnat in unitáte Spíritus Sancti, Deus,
      per ómnia sǽcula sæculórum.
    </p>

    <p>
      <label>℟.</label>
      Amen.
    </p>
  </div>

  <!-- Preface -->
  <div type="preface" xml:id="preface-nativity">
    <head>Præfatio</head>

    <ref target="ordinarium:preface-nativity">
      Præfatio de Nativitate Domini
    </ref>

    <!-- Or include full text -->
    <div type="dialogue">
      <p>
        <label>℣.</label>
        Dóminus vobíscum.
      </p>
      <p>
        <label>℟.</label>
        Et cum spíritu tuo.
      </p>
      <p>
        <label>℣.</label>
        Sursum corda.
      </p>
      <p>
        <label>℟.</label>
        Habémus ad Dóminum.
      </p>
      <p>
        <label>℣.</label>
        Grátias agámus Dómino Deo nostro.
      </p>
      <p>
        <label>℟.</label>
        Dignum et iustum est.
      </p>
    </div>

    <div type="text">
      <p>
        Vere dignum et iustum est, æquum et salutáre,
        nos tibi semper et ubíque grátias ágere:
        Dómine sancte, Pater omnípotens, ætérne Deus:
        Quia per incarnáti Verbi mystérium
        nova mentis nostræ óculis lux tuæ claritátis infúlsit:
        ut, dum visibíliter Deum cognóscimus,
        per hunc in invisibílium amórem rapiámur.
        Et ídeo cum Angelis et Archángelis,
        cum Thronis et Dominatiónibus,
        cumque omni milítia cæléstis exércitus,
        hymnum glóriæ tuæ cánimus, sine fine dicéntes:
      </p>
    </div>
  </div>

  <!-- Communion -->
  <div type="communion" xml:id="communion-nativity">
    <head>Communio</head>

    <div type="source">
      <bibl>
        <ref target="bible:ps97:3">Ps. 97:3</ref>
      </bibl>
    </div>

    <p>
      Vidérunt omnes fines terræ salutáre Dei nostri.
    </p>
  </div>

  <!-- Postcommunion -->
  <div type="postcommunion" xml:id="postcommunion-nativity">
    <head>Postcommunio</head>

    <p>
      Præsta, quǽsumus, omnípotens Deus:
      ut natus hódie Salvátor mundi,
      sicut divínæ nobis generatiónis est auctor;
      ita et immortalitátis sit ipse largítor:
    </p>

    <p type="conclusion">
      Qui tecum vivit et regnat in unitáte Spíritus Sancti, Deus,
      per ómnia sǽcula sæculórum.
    </p>

    <p>
      <label>℟.</label>
      Amen.
    </p>
  </div>

</div>
```

### Mass Ordinary Elements

The Ordinary of the Mass (fixed parts) would be stored separately:

```xml
<!-- ordinarium/mass-ordinary.xml -->
<div type="ordinary">

  <div type="kyrie" xml:id="kyrie">
    <head>Kyrie</head>
    <p>Kýrie, eléison. (3x)</p>
    <p>Christe, eléison. (3x)</p>
    <p>Kýrie, eléison. (3x)</p>
  </div>

  <div type="gloria" xml:id="gloria">
    <head>Gloria</head>
    <p>
      Glória in excélsis Deo.
      Et in terra pax homínibus bonæ voluntátis.
      Laudámus te. Benedícimus te.
      Adorámus te. Glorificámus te.
      Grátias ágimus tibi propter magnam glóriam tuam.
      <!-- Full Gloria text -->
    </p>
  </div>

  <div type="credo" xml:id="credo">
    <head>Credo</head>
    <p>
      Credo in unum Deum,
      Patrem omnipoténtem,
      factórem cæli et terræ,
      visibílium ómnium et invisibílium.
      <!-- Full Nicene Creed -->
    </p>
  </div>

  <div type="sanctus" xml:id="sanctus">
    <head>Sanctus</head>
    <p>
      Sanctus, Sanctus, Sanctus
      Dóminus Deus Sábaoth.
      Pleni sunt cæli et terra glória tua.
      Hosánna in excélsis.
      Benedíctus qui venit in nómine Dómini.
      Hosánna in excélsis.
    </p>
  </div>

  <div type="agnus-dei" xml:id="agnus-dei">
    <head>Agnus Dei</head>
    <p>Agnus Dei, qui tollis peccáta mundi: miserére nobis.</p>
    <p>Agnus Dei, qui tollis peccáta mundi: miserére nobis.</p>
    <p>Agnus Dei, qui tollis peccáta mundi: dona nobis pacem.</p>
  </div>

</div>
```

### Votive Masses

```xml
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="missa-votive-spiritu-sancto">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>Missa Votiva de Spiritu Sancto</title>
        <title type="vernacular" xml:lang="en">Votive Mass of the Holy Spirit</title>
      </titleStmt>
      <!-- ... -->
    </fileDesc>

    <profileDesc>
      <textClass>
        <keywords>
          <term>Votive Mass</term>
          <term>Holy Spirit</term>
        </keywords>
      </textClass>
    </profileDesc>
  </teiHeader>

  <text xml:lang="la">
    <body>
      <div type="mass" subtype="votive">
        <head>Missa Votiva de Spiritu Sancto</head>
        <!-- Mass propers -->
      </div>
    </body>
  </text>
</TEI>
```

### Requiem Mass

```xml
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:id="missa-defunctorum">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>Missa pro Defunctis (Requiem)</title>
      </titleStmt>
      <!-- ... -->
    </fileDesc>
  </teiHeader>

  <text xml:lang="la">
    <body>
      <div type="mass" subtype="requiem">
        <head>Missa pro Defunctis</head>

        <div type="propers">
          <div type="introit">
            <p>
              Réquiem ætérnam dona eis, Dómine:
              et lux perpétua lúceat eis.
            </p>
            <!-- ... -->
          </div>

          <!-- Special sequence: Dies Irae -->
          <div type="sequence" xml:id="dies-irae">
            <head>Sequentia</head>
            <lg type="stanza" n="1">
              <l>Dies iræ, dies illa,</l>
              <l>Solvet sǽclum in favílla:</l>
              <l>Teste David cum Sibýlla.</l>
            </lg>
            <!-- More stanzas -->
          </div>

          <!-- No Gloria, no Alleluia, special prayers -->
        </div>
      </div>
    </body>
  </text>
</TEI>
```

---

## Migration Strategy for Mass

### Phase-by-Phase Approach

The Mass migration should be **integrated into the existing phases** of the main proposal:

#### Phase 1: Data Conversion (Months 1-3)
**Add Mass Conversion Tasks**:
- Design TEI schema for Mass propers
- Build Mass-specific conversion tools
- Convert Latin Sanctoral Masses (parallel to Office)
- Convert Latin Temporal Masses
- Convert Commune Masses
- Convert Votive and Requiem Masses

**Deliverables**:
- TEI XML for all Latin Masses
- Mass-specific JSON metadata
- Updated conversion scripts

#### Phase 2: Rule Engine (Months 3-6)
**Add Mass Logic**:
- Mass precedence rules (similar to Office but simpler)
- Lectionary selection
- Preface determination
- Multiple Mass handling (Christmas, All Souls)
- Votive Mass rules

**Note**: Mass precedence is generally simpler than Office precedence

#### Phase 3: Flask Application (Months 6-9)
**Add Mass Interface**:
- Mass display pages
- Separate routes for Mass (/mass/ vs. /office/)
- Mass calendar view
- Lectionary browser
- API endpoints for Mass

**API Examples**:
```
GET /api/mass/{date}
GET /api/mass/{date}/propers
GET /api/lectionary/{year}/{cycle}
```

#### Phase 4-5: Validation & Launch (Months 9-18)
**Include Mass Testing**:
- Validate Mass outputs against Perl version
- Test all Mass types (festive, votive, requiem)
- User testing of Mass interface
- Parallel deployment with Office

### Resource Impact

**Additional Development Time**: +20-30%
- Mass is structurally simpler than Office
- Fewer canonical hours to handle
- Similar data structures enable code reuse

**Estimated Timeline Adjustment**:
- **Original**: 18 months for Office only
- **Revised**: 21-24 months for Office + Mass
- **Alternative**: Can be done in parallel if sufficient resources

---

## Shared Infrastructure

### Code Reuse Between Office and Mass

Much of the infrastructure can be shared:

```python
# Shared base classes
class LiturgicalDocument:
    """Base class for both Office and Mass"""
    def __init__(self, office_key, version):
        self.office_key = office_key
        self.version = version

    def load_tei(self):
        """Load TEI file"""
        pass

    def render_html(self):
        """Render to HTML"""
        pass

class Office(LiturgicalDocument):
    """Divine Office specific"""
    def get_hour(self, canonical_hour):
        pass

class Mass(LiturgicalDocument):
    """Mass specific"""
    def get_propers(self):
        pass

    def get_ordinary(self):
        pass
```

### Shared Components

✅ **Data Loader**: Same JSON/TEI loading mechanism
✅ **Date Calculations**: Easter, liturgical calendar
✅ **Transfer Resolution**: Same transfer rules apply
✅ **Version Management**: Same rubrical versions
✅ **Multi-Language**: Same translation infrastructure
✅ **Caching**: Same SQLite cache strategy
✅ **API Framework**: Same Flask application
✅ **Frontend**: Shared CSS/JavaScript

### Mass-Specific Components

🔹 **Propers Selection**: Unique to Mass
🔹 **Lectionary**: Epistle/Gospel assignment
🔹 **Preface Selection**: Seasonal prefaces
🔹 **Ordo Handling**: Mass ceremonial directions
🔹 **Multiple Celebrations**: Christmas three Masses, etc.

---

## Updated Migration Proposal Summary

### Revised Scope

**Original Scope**: Divine Office only
**Revised Scope**: Divine Office + Mass

### Revised Timeline

**Conservative Estimate**: 24 months (18 + 6)
**Optimistic with Parallel Work**: 21 months
**With Full Team**: 18 months (both in parallel)

### Revised Phase Breakdown

| Phase | Duration | Office Tasks | Mass Tasks |
|-------|----------|-------------|------------|
| **Phase 1** | 3 months | Latin Office TEI conversion | Latin Mass TEI conversion |
| **Phase 2** | 3 months | Office precedence engine | Mass propers engine |
| **Phase 3** | 3 months | Office web interface | Mass web interface |
| **Phase 4** | 3 months | Office validation | Mass validation |
| **Phase 5** | 6 months | Office beta & launch | Mass beta & launch |
| **Total** | **18-24 months** | | |

### Priority Options

**Option A: Sequential** (24 months)
1. Complete Office migration (18 months)
2. Then Mass migration (6 months)
3. Lower risk, easier to manage
4. Users get Office improvements first

**Option B: Parallel** (18-21 months)
1. Office and Mass together
2. Requires larger team
3. Faster delivery
4. Higher coordination complexity

**Option C: Office First, Mass Later** (18+ months)
1. Complete Office migration
2. Mass migration as separate project
3. Most conservative approach
4. Allows learning from Office migration

---

## Recommendation

### Recommended Approach

**Include Mass in Migration from Day One**

**Rationale**:
1. **Shared Infrastructure**: 70% of code can be reused
2. **User Expectation**: Users expect both Office and Mass
3. **Efficiency**: Easier to build together than retrofit
4. **Data Consistency**: Same TEI/JSON approach for both
5. **Testing**: Can validate both simultaneously

**Timeline**: Plan for **21 months** with Mass included
- Optimistic: 18 months with adequate resources
- Conservative: 24 months with limited resources
- Realistic: 21 months with part-time team

### Phasing Strategy

**Phase 1-2**: Build infrastructure supporting both
**Phase 3**: Develop Office interface first (primary use case)
**Phase 3.5**: Add Mass interface (leverages Office work)
**Phase 4-5**: Validate and launch both together

### Resource Adjustment

**Minimum Team** (24 months):
- 1 Python developer (20 hrs/week)
- 1 TEI specialist (5 hrs/week)
- 1 QA tester (10 hrs/week)

**Recommended Team** (21 months):
- 1.5 Python developers (30 hrs/week total)
- 1 TEI specialist (5 hrs/week)
- 1 QA tester (10 hrs/week)

**Ideal Team** (18 months):
- 2 Python developers (40 hrs/week total)
- 1 TEI specialist (10 hrs/week)
- 1 Frontend developer (10 hrs/week)
- 1 QA tester (15 hrs/week)

---

## Updated Decision Points

### Key Question for Stakeholders

**Should Mass be included in the migration scope?**

**Recommendation**: **YES**

**Reasons**:
✅ Shared infrastructure reduces incremental work
✅ Users expect complete solution (Office + Mass)
✅ Data model and architecture support both
✅ Easier to build together than add later
✅ Only adds 15-30% to timeline

**Trade-off**:
⚠️ Extends timeline by 3-6 months
⚠️ Requires slightly more resources
⚠️ Increases scope complexity

**Alternative**:
If resources are very limited, complete Office first (18 months), then Mass separately (6 months later). This reduces risk but delays Mass improvements.

---

## Conclusion

The migration proposal **should explicitly include the Mass** alongside the Divine Office:

1. **Feasibility**: Mass migration uses same architecture as Office
2. **Efficiency**: Shared infrastructure reduces incremental cost
3. **Completeness**: Users expect both Office and Mass
4. **Timeline**: Adds only 15-30% to overall duration
5. **Recommendation**: Include from Day One with realistic 21-month timeline

**Updated Main Proposal**: Should be amended to explicitly include Mass throughout all phases with appropriate timeline adjustments.

---

**Document Version**: 1.0
**Date**: 2025-12-28
**Status**: Addendum to Main Migration Proposal
**Recommendation**: Incorporate into main proposal as revised scope
