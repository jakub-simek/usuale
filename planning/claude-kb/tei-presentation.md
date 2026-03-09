---
title: TEI Data Model for Divinum Officium
subtitle: Modernizing Liturgical Text Encoding
author: Divinum Officium Project
date: December 28, 2025
theme: serif
---

# TEI Data Model for Divinum Officium

**Modernizing Liturgical Text Encoding**

A Proposal for Migration to TEI XML

---

## Agenda

1. Current State & Challenges
2. What is TEI?
3. Why TEI for Divinum Officium?
4. Proposed TEI Structure
5. Migration Strategy
6. Benefits & Impact
7. Timeline & Resources
8. Decision Points

---

# Part 1: Current State

---

## The Divinum Officium Project

**Mission**: Provide traditional Roman Catholic liturgy online

**Current Implementation**:
- Perl-based web application
- Plain text data files
- 15+ languages supported
- Multiple historical rubrics (1570, 1960, etc.)

**Users**: Thousands worldwide praying the Divine Office and Mass daily

---

## Current Data Format

```
[Rank]
In Nativitate Domini;;Duplex I classis;;7.0

[Ant Vespera]
O admirábile commércium: * Creátor géneris humáni...;;109

[Hymnus Vespera]
v. Jesu, Redémptor ómnium,
Quem lucis ante oríginem
_
Te mane laudum cármine...

[Lectio4]
Sermo sancti Leónis Papæ
!Sermo 7 de Nativitate Domini
Festivitátis hodiérnæ, dilectíssimi...
```

**Convention-based structure with special characters**

---

## Current Challenges

### Data Structure Issues

❌ **No Formal Schema**
- Structure enforced by convention only
- Easy to introduce errors
- No automatic validation

❌ **Special Characters**
- `@` = cross-reference
- `$` = prayer reference
- `#` = chapter label
- `!` = red text (rubric)
- `~` = line contraction

**Meaning defined in code, not in data**

---

## Current Challenges (continued)

### Technical Limitations

❌ **Hard to Query**
- Can't easily search across offices
- No structured data analysis
- Difficult to extract information programmatically

❌ **No Semantic Markup**
- Formatting mixed with content
- Meaning implicit, not explicit
- Lost scholarly context

❌ **Maintenance Burden**
- Perl expertise scarce
- Complex parsing logic scattered
- Difficult for new contributors

---

# Part 2: What is TEI?

---

## Text Encoding Initiative (TEI)

**Industry Standard for Digital Texts**

- **Established**: 1987 (35+ years)
- **Current Version**: TEI P5 (Version 4.7.0)
- **Maintained**: TEI Consortium
- **Used By**: Libraries, archives, digital humanities projects worldwide

**Website**: https://tei-c.org/

---

## TEI Core Principles

### 1. **Descriptive, Not Prescriptive**
Describe what text **is**, not how it **looks**

### 2. **Semantic Markup**
Capture **meaning** and **structure**

### 3. **Standards-Based**
XML with documented schema

### 4. **Extensible**
Customize for specific domains (like liturgy)

---

## TEI in Action: Example

**Plain Text**:
```
Ant. O admirábile commércium: Creátor géneris humáni
```

**TEI XML**:
```xml
<div type="antiphon" n="1" xml:id="ant-vesp-1">
  <label>Ant.</label>
  <p>
    O admirábile commércium: *
    <seg type="emphasis">Creátor géneris humáni</seg>,
    animátum corpus sumens,
    de Vírgine nasci dignátus est.
  </p>
  <note type="psalm-link">
    <ref target="#ps-109">With Psalm 109</ref>
  </note>
</div>
```

**Semantic structure is explicit**

---

## TEI Success Stories

### Digital Projects Using TEI

- **Perseus Digital Library** - Ancient Greek/Latin texts
- **Oxford Text Archive** - Literary works
- **Women Writers Project** - Pre-Victorian women's writing
- **Digital Vulgate Project** - Latin Bible
- **Electronic Beowulf** - Old English manuscript

### Liturgical Applications

- **Corpus Corporum** - Medieval Latin texts including liturgy
- **Monumenta Germaniae Historica** - Historical sources
- Various digital breviaries and missals

---

# Part 3: Why TEI for Divinum Officium?

---

## Scholarly Benefits

✅ **Academic Legitimacy**
- Recognized standard in liturgical studies
- Enables scholarly citation
- Interoperable with other liturgical databases

✅ **Semantic Encoding**
- Distinguish antiphons, psalms, readings, responses
- Preserve liturgical structure
- Document sources and variants

✅ **Long-Term Preservation**
- Vendor-neutral format
- Will outlast current technologies
- Archival quality

---

## Technical Benefits

✅ **Validation**
- XML Schema ensures structural correctness
- Catches errors automatically
- Enforces consistency across 1000s of files

✅ **Queryability**
- XPath for precise searching
- XQuery for complex analysis
- Find all Duplex I classis feasts
- Extract all readings from St. Leo
- Analyze psalm usage patterns

---

## Technical Benefits (continued)

✅ **Flexibility**
- Extensible for project needs
- Customizable via TEI ODD
- Supports multiple versions (1570, 1960, etc.)
- Handles variants and annotations

✅ **Tool Ecosystem**
- XML editors with validation (Oxygen, VS Code)
- Processing libraries (lxml, Saxon, BaseX)
- Version control friendly (git diff)
- Transform to multiple formats

---

## Practical Benefits

✅ **Multiple Output Formats**

**From Single TEI Source**:
- HTML for web display
- PDF via XSL-FO for printing
- ePub for e-readers
- LaTeX for scholarly editions
- JSON for APIs
- Plain text for accessibility

✅ **Future-Proof**
- Format will remain readable for decades
- Not tied to specific software
- Human-readable XML

---

## Comparison: Current vs. TEI

| Aspect | Current Format | TEI XML |
|--------|---------------|---------|
| **Validation** | Manual checking | Automatic schema |
| **Semantics** | Implicit | Explicit markup |
| **Queries** | Text search only | XPath/XQuery |
| **Standards** | Project-specific | International standard |
| **Tools** | Custom Perl | Industry standard |
| **Preservation** | Uncertain | Archival quality |
| **Interoperability** | Limited | High |

---

# Part 4: Proposed TEI Structure

---

## Overall Document Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0"
     xml:id="sancti-12-25">

  <teiHeader>
    <!-- Metadata: title, source, edition, etc. -->
  </teiHeader>

  <text xml:lang="la">
    <body>
      <!-- The actual liturgical content -->
    </body>
  </text>

</TEI>
```

**Two main parts**: Header (metadata) + Body (content)

---

## TEI Header: Metadata

```xml
<teiHeader>
  <fileDesc>
    <titleStmt>
      <title xml:lang="la">In Nativitate Domini</title>
      <title xml:lang="en">The Nativity of Our Lord</title>
    </titleStmt>

    <publicationStmt>
      <publisher>Divinum Officium Project</publisher>
      <availability>
        <licence target="https://opensource.org/licenses/MIT">
          MIT License
        </licence>
      </availability>
    </publicationStmt>

    <sourceDesc>
      <bibl>Breviarium Romanum 1962</bibl>
    </sourceDesc>
  </fileDesc>

  <profileDesc>
    <textClass>
      <keywords>
        <term>Duplex I classis</term>
        <term>Christmas</term>
        <term>Feast of the Lord</term>
      </keywords>
    </textClass>
  </profileDesc>
</teiHeader>
```

---

## Body: Liturgical Structure

```xml
<body>
  <div type="office" xml:id="office-12-25">
    <head>In Nativitate Domini</head>

    <!-- Metadata section -->
    <div type="metadata">
      <ab type="rank" n="7.0">
        <seg type="class">Duplex I classis</seg>
      </ab>
    </div>

    <!-- Canonical Hours -->
    <div type="hour" subtype="matins">...</div>
    <div type="hour" subtype="lauds">...</div>
    <div type="hour" subtype="vespers">...</div>
    <!-- etc. -->
  </div>
</body>
```

---

## Example: Matins Structure

```xml
<div type="hour" subtype="matins" xml:id="matins">
  <head>Ad Matutinum</head>

  <!-- Invitatory -->
  <div type="invitatory">
    <div type="antiphon">
      <p>Christus natus est nobis: * Veníte, adorémus.</p>
    </div>
    <div type="psalm" xml:id="ps-94">
      <ref target="psalterium:ps-94">Venite</ref>
    </div>
  </div>

  <!-- Hymn -->
  <div type="hymn">
    <lg type="stanza" n="1">
      <l>Jesu, Redémptor ómnium,</l>
      <l>Quem lucis ante oríginem</l>
    </lg>
  </div>

  <!-- Nocturns -->
  <div type="nocturn" n="1">...</div>
  <div type="nocturn" n="2">...</div>
  <div type="nocturn" n="3">...</div>
</div>
```

---

## Example: Antiphon Encoding

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

  <note type="psalm-link">
    <ref target="#ps-109">With Psalm 109</ref>
  </note>
</div>
```

**Clear semantic structure**:
- `type="antiphon"` - What it is
- `n="1"` - Which one
- `xml:id` - Unique identifier
- `<seg type="emphasis">` - Emphasized text

---

## Example: Reading (Lectio)

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
    Paris enim perículi malum est...
  </p>
</div>
```

**Source attribution**: Clear bibliographic information

---

## Example: Responsory

```xml
<div type="responsory" n="1" xml:id="resp1">

  <div type="response" subtype="initial">
    <label>℟.</label>
    <p>
      Hodie nobis cælórum Rex
      de Vírgine nasci dignátus est,
      <seg type="asterisk">*</seg>
      Gaudet exércitus Angelórum.
    </p>
  </div>

  <div type="verse">
    <label>℣.</label>
    <p>Glória in excélsis Deo...</p>
  </div>

  <div type="response" subtype="repetition">
    <label>℟.</label>
    <p>Gaudet exércitus Angelórum.</p>
  </div>

</div>
```

**Structure clear**: Response, verse, repetition

---

## Handling Multiple Versions

**Version-Specific Content**:

```xml
<div type="reading" n="1" source="#brev1962">
  <p>Reading for 1962 rubrics...</p>
</div>

<div type="reading" n="1" source="#brev1570">
  <p>Different reading for 1570 rubrics...</p>
</div>
```

**Or using `<choice>`**:

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

---

## Cross-References

**Current Format**:
```
@Tempora/Nat1-0:Hymnus Vespera
```

**TEI Equivalent**:
```xml
<div type="hymn">
  <ref target="tempora:Nat1-0:hymn-vesp">
    Same as First Vespers of Christmas
  </ref>
</div>
```

**Benefits**:
- Explicit relationship
- Can validate target exists
- Tools can follow links
- Generate dependency graphs

---

## Chant Integration (GABC)

```xml
<div type="antiphon" n="1">
  <!-- Text -->
  <p xml:id="ant-text-1">
    Dóminus dixit ad me: Fílius meus es tu,
    ego hódie génui te.
  </p>

  <!-- Musical notation -->
  <notatedMusic xml:id="ant-gabc-1">
    <ab type="gabc">
      name: Dominus dixit;
      mode: 8;
      %%
      (c4) Dó(f)mi(g)nus(h) di(g)xit(f)...
    </ab>
  </notatedMusic>
</div>
```

**Preserves both text and music**

---

## Mass Structure

```xml
<div type="mass" xml:id="mass-nativity">
  <head>Missa in Nativitate Domini</head>

  <div type="propers">
    <div type="introit">...</div>
    <div type="collect">...</div>
    <div type="epistle">...</div>
    <div type="gospel">...</div>
    <div type="gradual">...</div>
    <div type="alleluia">...</div>
    <div type="offertory">...</div>
    <div type="secret">...</div>
    <div type="communion">...</div>
    <div type="postcommunion">...</div>
  </div>
</div>
```

**Clear Mass structure**: All propers explicitly marked

---

# Part 5: Migration Strategy

---

## Migration Approach

### Gradual Parallel Migration

**Keep existing system running while**:
1. Converting data to TEI
2. Building new system
3. Validating equivalence
4. Transitioning users

**No disruption to current users**

---

## Phase 1: Data Conversion (3 months)

**Tasks**:
1. Design TEI schema
2. Build automated conversion tools
3. Convert Latin offices to TEI
4. Convert Latin Masses to TEI
5. Quality assurance & validation

**Deliverables**:
- TEI XML for all Latin texts
- JSON metadata files
- Conversion scripts
- Validation reports

**Success**: 100% of Latin content in valid TEI

---

## Conversion Process

```
┌─────────────────┐
│  Current Text   │
│     Files       │
│  (Rank, Ant,    │
│   Hymnus, etc.) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Conversion    │
│      Tool       │
│   (Python)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   TEI XML       │
│    Files        │
│ + JSON Metadata │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Validation    │
│   (RelaxNG      │
│    Schema)      │
└────────┬────────┘
         │
         ▼
    ✅ Valid TEI
```

---

## Example: Converting an Antiphon

**Input** (Current Format):
```
[Ant Vespera]
O admirábile commércium: * Creátor géneris humáni...;;109
```

**Output** (TEI):
```xml
<div type="antiphon" n="1">
  <label>Ant.</label>
  <p>
    O admirábile commércium: *
    Creátor géneris humáni...
  </p>
  <note type="psalm">
    <ref target="#ps-109">Psalm 109</ref>
  </note>
</div>
```

**Automated with quality checks**

---

## Phase 2-3: New System (6 months)

**Phase 2**: Python engine for reading TEI
**Phase 3**: Web interface

**Built in parallel with Office-focused work**:
- TEI/XML parsing (lxml)
- Flask web application
- HTML rendering from TEI
- API endpoints
- Mobile-responsive interface

**Leverages same infrastructure as Office**

---

## Phase 4-5: Validation & Launch (9 months)

**Phase 4**: Parallel validation
- Compare outputs (old vs. new)
- Fix discrepancies
- Beta testing with users

**Phase 5**: Gradual transition
- Soft launch at beta subdomain
- User feedback & fixes
- Full cutover
- Archive old system

**Total Timeline**: 18-24 months

---

# Part 6: Benefits & Impact

---

## Data Quality Improvements

### Before TEI
```
[Ant Vespra]  ← Typo!
O admirabile commercium...;;109

[Hymnus]
v. Jesu, Redemptor omnium  ← Missing line break
Quem lucis ante originem
```

**Errors caught manually (or not at all)**

### After TEI
```xml
<div type="antiphon">  ← Schema validates type
  <label>Ant.</label>
  <p>O admirábile commércium...</p>
  <note type="psalm">
    <ref target="#ps-109"/>  ← Link validated
  </note>
</div>
```

**Schema catches errors automatically**

---

## Query Capabilities

### Find All Duplex I Classis Feasts

```xpath
//div[@type='metadata']/ab[@type='rank' and @n >= 6.0]
```

**Returns**:
- Christmas
- Easter
- Pentecost
- Epiphany
- etc.

### Get All Readings from St. Leo

```xpath
//div[@type='reading']//bibl[contains(author, 'Leo')]
```

**Enables scholarly analysis**

---

## Transformation Capabilities

### One Source, Multiple Outputs

```
                    ┌──────────────┐
                    │   TEI XML    │
                    │  (one file)  │
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────┐      ┌──────────┐      ┌──────────┐
   │  HTML   │      │   PDF    │      │   ePub   │
   │  (Web)  │      │ (Print)  │      │ (eReader)│
   └─────────┘      └──────────┘      └──────────┘
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────┐      ┌──────────┐      ┌──────────┐
   │  JSON   │      │  LaTeX   │      │  Plain   │
   │  (API)  │      │(Scholarly)│     │  Text    │
   └─────────┘      └──────────┘      └──────────┘
```

**Single authoritative source**

---

## Scholarly Benefits

✅ **Citability**
- Standard format for academic citation
- Persistent identifiers
- Version tracking

✅ **Interoperability**
- Share data with other projects
- Digital Vulgate Project
- Medieval Latin databases
- Liturgical research projects

✅ **Critical Editions**
- Document textual variants
- Note editorial decisions
- Track sources

---

## Developer Benefits

### For Contributors

✅ **Easier to Understand**
- XML is self-documenting
- Clear structure visible
- Standard tools available

✅ **Better Tooling**
- XML editors with autocomplete
- Validation in real-time
- Git-friendly diffs

✅ **Lower Barrier to Entry**
- No need to learn Perl
- XML/TEI documentation abundant
- Examples and tutorials available

---

## User Benefits

### Enhanced Features

✅ **Better Search**
- Find all offices for a saint
- Search by rank, season, type
- Full-text search with context

✅ **API Access**
- Third-party apps can integrate
- Mobile apps
- Personal prayer tools
- Research tools

✅ **Multiple Formats**
- Read online
- Download PDF
- ePub for e-readers
- Print-optimized layouts

---

## Long-Term Preservation

### Archival Quality

**TEI files will be readable in 50+ years**

- Not dependent on specific software
- XML parsers will always exist
- Human-readable text format
- Well-documented standard
- Maintained by TEI Consortium

**vs. Proprietary Formats**:
- WordPerfect files from 1990s?
- Microsoft Works documents?
- PageMaker files?

**TEI = Future-proof**

---

# Part 7: Timeline & Resources

---

## Proposed Timeline

### 24-Month Plan (Conservative)

| Quarter | Phase | Deliverable |
|---------|-------|-------------|
| **Q1** | Data Conversion | Latin TEI complete |
| **Q2** | Schema & Tools | Conversion validated |
| **Q3** | Python Engine | TEI processing working |
| **Q4** | Web Interface | Beta site live |
| **Q5** | Testing | User feedback |
| **Q6** | Launch | Production cutover |

**Can be done in 18 months with adequate resources**

---

## Resource Requirements

### Minimum Team (24 months)

- **1 Python Developer** (20 hrs/week)
  - TEI processing
  - Web development

- **1 TEI Specialist** (5 hrs/week)
  - Schema design
  - Quality review

- **1 QA Tester** (10 hrs/week)
  - Validation
  - User testing

**Total**: ~35 hours/week

---

## Resource Requirements (continued)

### Ideal Team (18 months)

- **2 Python Developers** (40 hrs/week total)
- **1 TEI Specialist** (10 hrs/week)
- **1 Frontend Developer** (10 hrs/week)
- **1 QA Tester** (15 hrs/week)

**Total**: ~75 hours/week

### Infrastructure

- Git repository (existing)
- CI/CD pipeline (GitHub Actions - free)
- Development/staging server ($20/month)
- Production hosting (scales with usage)

**Monthly Cost**: $20-50 during development

---

## Risk Management

### Technical Risks

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Data loss in conversion | Low | Automated + manual validation |
| Performance issues | Medium | Caching, optimization |
| Schema complexity | Medium | TEI expert consultation |

### Project Risks

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Insufficient resources | Medium | Phased approach, extend timeline |
| Community resistance | Low | Clear communication, beta period |
| Scope creep | High | Strict phase definitions |

---

# Part 8: Decision Points

---

## Key Questions

### 1. Should we modernize the data format?

**Status Quo**: Keep current text files
- Works today
- Familiar to current maintainers
- But: technical debt growing

**TEI Migration**: Adopt scholarly standard
- Future-proof
- Better quality
- Enables new features
- But: requires investment

---

## Key Questions (continued)

### 2. What timeline is realistic?

**Options**:
- **18 months** - Full-time dedicated team
- **21 months** - Part-time volunteers (realistic)
- **24 months** - Conservative estimate
- **36+ months** - Very limited resources

**Recommendation**: Plan for 21-24 months

### 3. Include Mass from Day One?

**Yes** - Recommended
- Same architecture
- User expectation
- Only +15% timeline

**No** - Do Office first
- Lower risk
- Simpler scope
- Mass later as separate project

---

## Success Criteria

### Phase 1 Success
✅ 100% of Latin content in valid TEI
✅ All files validate against schema
✅ No content loss verified
✅ Conversion process documented

### Overall Success
✅ New system matches old system output
✅ User satisfaction maintained/improved
✅ Contributor growth
✅ Codebase more maintainable
✅ Data quality improved

---

## Next Steps

### If Approved

**Month 1**:
1. Form development team
2. Set up infrastructure
3. Design TEI schema (draft)
4. Build proof-of-concept conversion

**Month 2-3**:
1. Refine schema based on POC
2. Convert sample offices
3. Validate approach
4. Adjust plan as needed

**Month 4+**:
1. Full conversion
2. Engine development
3. Web interface
4. Testing and launch

---

# Conclusion

---

## Summary: Why TEI?

### ✅ Scholarly Standard
Industry-recognized format for liturgical texts

### ✅ Data Quality
Validation prevents errors, ensures consistency

### ✅ Future-Proof
Will be readable and usable for decades

### ✅ Powerful
Enables queries, analysis, transformations

### ✅ Practical
Multiple output formats from single source

---

## The Vision

### From This...

```
[Ant Vespera]
O admirábile commércium: * Creátor...;;109

[Hymnus Vespera]
v. Jesu, Redémptor ómnium,
```

### To This...

```xml
<div type="antiphon" xml:id="ant-vesp-1">
  <label>Ant.</label>
  <p>O admirábile commércium: *
     <seg type="emphasis">Creátor géneris humáni</seg>...
  </p>
  <note type="psalm"><ref target="#ps-109"/></note>
</div>
```

**Semantic, validated, queryable, preservable**

---

## The Impact

### For Scholars
- Citeable, analyzable liturgical texts
- Interoperable with other projects
- Critical edition capabilities

### For Developers
- Modern, maintainable codebase
- Standard tools and libraries
- Lower barrier to contribution

### For Users
- Same trusted content
- Better search and navigation
- Multiple formats (web, PDF, ePub)
- API for integrations

---

## The Ask

### Decision Needed

**Approve TEI migration as part of modernization?**

**Commitment Required**:
- 21-24 months development
- Development team (2-3 people, part-time)
- ~$1,000-2,000 infrastructure cost
- Community support and patience

**Value Delivered**:
- Future-proof liturgical database
- Improved data quality
- Enhanced capabilities
- Scholarly legitimacy
- Sustainable long-term maintenance

---

## Timeline Summary

```
┌──────────────────────────────────────────────────────┐
│                   24 Month Plan                       │
├────────┬────────┬────────┬────────┬────────┬─────────┤
│   Q1   │   Q2   │   Q3   │   Q4   │   Q5   │   Q6   │
├────────┼────────┼────────┼────────┼────────┼─────────┤
│ Schema │Convert │ Engine │  Web   │ Test   │ Launch │
│ Design │  Data  │  Build │  Build │ & Fix  │& Cutover│
├────────┴────────┴────────┴────────┴────────┴─────────┤
│  ✓ TEI XML      ✓ Python     ✓ Beta    ✓ Production │
│  ✓ Validated    ✓ Rendering  ✓ Tested  ✓ Archived  │
└──────────────────────────────────────────────────────┘
```

**Start**: Q1 2026
**Beta**: Q4 2026
**Launch**: Q2 2027

---

# Questions & Discussion

---

## Discussion Topics

1. **Scope**: Office + Mass together, or sequential?

2. **Timeline**: 18, 21, or 24 months?

3. **Resources**: Who can contribute? Funding available?

4. **Priorities**: What matters most?
   - Speed of delivery?
   - Risk minimization?
   - Feature completeness?

5. **Concerns**: What worries you about this proposal?

---

## Contact & Resources

### Documentation

- **Full Proposal**: `claude-kb/migration-proposal.md`
- **TEI Specification**: `claude-kb/tei-data-model.md`
- **Mass Addendum**: `claude-kb/mass-migration-addendum.md`

### TEI Resources

- **TEI Guidelines**: https://tei-c.org/guidelines/
- **TEI by Example**: https://teibyexample.org/
- **TEI Consortium**: https://tei-c.org/

### Project

- **Repository**: https://github.com/DivinumOfficium/divinum-officium
- **Website**: https://divinumofficium.com/

---

# Thank You

**Questions?**

---

## Appendix: Technical Details

(Additional slides for reference)

---

## Appendix A: XML Schema Example

```xml
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
      <element name="label"><text/></element>
    </optional>

    <oneOrMore>
      <element name="p">
        <ref name="textContent"/>
      </element>
    </oneOrMore>
  </element>
</define>
```

---

## Appendix B: Conversion Script

```python
def convert_antiphon(section_text):
    """Convert [Ant Vespera] to TEI"""
    lines = section_text.strip().split('\n')
    antiphons = []

    for i, line in enumerate(lines, 1):
        # Parse: "Text;;Psalm"
        parts = line.split(';;')
        text = parts[0]
        psalm = parts[1] if len(parts) > 1 else None

        # Create TEI element
        ant_div = etree.Element('div',
                                type='antiphon',
                                n=str(i))

        label = etree.SubElement(ant_div, 'label')
        label.text = f"Ant. {i}"

        p = etree.SubElement(ant_div, 'p')
        p.text = text

        if psalm:
            note = etree.SubElement(ant_div, 'note',
                                   type='psalm')
            ref = etree.SubElement(note, 'ref',
                                  target=f"#ps-{psalm}")
            ref.text = f"Psalm {psalm}"

        antiphons.append(ant_div)

    return antiphons
```

---

## Appendix C: XPath Query Examples

**Find all Christmas offices**:
```xpath
//TEI[contains(head, 'Nativitate')]
```

**Get Vespers antiphons for a date**:
```xpath
//TEI[@xml:id='sancti-12-25']
  //div[@subtype='vespers']
  //div[@type='antiphon']
```

**Count readings per office**:
```xpath
for $office in //TEI
return <count id="{$office/@xml:id}">
  {count($office//div[@type='reading'])}
</count>
```

**Find offices with Te Deum**:
```xpath
//div[@type='canticle'][@subtype='te-deum']
  /ancestor::TEI/@xml:id
```

---

## Appendix D: Migration Phases Detail

### Phase 1: Data Conversion (3 months)

**Week 1-2**: Schema design
- Draft RelaxNG schema
- Review with TEI expert
- Finalize structure

**Week 3-4**: Build converter
- Parse current format
- Generate TEI
- Handle special characters

**Week 5-8**: Convert Sanctoral
- All saint feast days
- Quality checks
- Manual review of samples

**Week 9-12**: Convert Temporal & Commune
- Seasonal offices
- Common offices
- Final validation

---

## Appendix E: Technology Stack

### Development
- **Python 3.11+**: Main language
- **lxml**: XML/TEI processing
- **Flask**: Web framework
- **Jinja2**: Templating
- **pytest**: Testing

### Validation
- **RelaxNG**: Schema validation
- **Oxygen XML**: Editor (commercial)
- **VS Code**: Free alternative

### Deployment
- **Docker**: Containerization
- **GitHub Actions**: CI/CD
- **SQLite**: Caching
- **Nginx**: Web server

---

## Appendix F: Comparison with Alternatives

| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|
| **Status Quo** | Works today, no effort | Technical debt grows | ❌ Not sustainable |
| **Improve Current** | Less disruption | Still custom format | ⚠️ Partial solution |
| **Custom XML** | Full control | Reinventing wheel | ❌ Not recommended |
| **JSON** | Modern, simple | Not scholarly std | ⚠️ Good for rules |
| **TEI XML** | Standard, validated | Learning curve | ✅ **Recommended** |

---

## Appendix G: Success Stories

### Similar Projects

**Digital Vulgate Project**
- Medieval Latin Bible in TEI
- Multiple manuscript witnesses
- Critical apparatus
- Successfully serving scholars since 2010

**Corpus Corporum**
- 200M+ words of Latin texts
- Includes liturgical materials
- TEI-based
- Powerful search capabilities

**Oxford Text Archive**
- 2,500+ TEI texts
- Long-term preservation
- Academic standard

---

## Appendix H: Glossary

**TEI**: Text Encoding Initiative - XML standard for texts

**XML**: Extensible Markup Language - structured data format

**Schema**: Formal definition of valid structure

**XPath**: Query language for XML

**XQuery**: Advanced query language for XML databases

**XSLT**: Transformation language (XML to HTML, etc.)

**RelaxNG**: Schema language (alternative to XML Schema)

**ODD**: One Document Does-it-all (TEI customization)

**Nocturn**: Division of Matins (3 per night)

**Propers**: Variable parts of Mass/Office

---

# End of Presentation

**Questions? Discussion?**

Contact: [Project Team Contact Info]

Repository: https://github.com/DivinumOfficium/divinum-officium
