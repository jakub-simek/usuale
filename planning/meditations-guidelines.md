# Usuale Meditation Guidelines

These are the project-specific rules for Usuale meditations. They supplement
the shared Latin meditation guidelines in:

```text
shared/latin-meditations-guidelines/guidelines/
```

Read the shared guidelines first. These Usuale rules override or specialize
them for liturgical meditations based on the traditional Roman liturgy and the
current Divinum Officium source witnesses.

## Scope

- Usuale meditations are traditional Catholic Latin meditations following the
  Roman liturgy in the usus antiquior.
- The primary text is normally a Mass or Office section: for example Introitus,
  Lectio, Evangelium, Offertorium, Communio, an Office antiphon, responsory,
  hymn, or reading.
- The chosen liturgical text remains the center. Other Mass or Office texts
  illuminate it; they do not replace it or become a parallel theme.
- Meditation files belong in `data/meditations/`.

## Source Order

Before writing or revising a meditation:

1. Identify the primary liturgical text and its liturgical day.
2. Read the relevant Divinum Officium source witness in `sources/divinum-officium/`.
3. Find the matching `celebratio` in `data/indexes/celebrations.xml`.
4. Check `data/meditations/` for existing meditations on the same celebration.
5. Compose or revise according to the shared guidelines plus this Usuale overlay.
6. Verify citations, direct quotations, `cf.` references, metadata, and Latin.

## Liturgical Context

Attend to the immediate Mass or Office context when it clarifies the primary
text:

- Epistle and Gospel
- Collect, Secret, Postcommunion, and other Mass orations
- Gradual, Alleluia or Tract, Offertory, Communion
- Office antiphons, responsories, hymns, readings, and capitula

References to this wider context must be organic. Do not append liturgical
parallels as external commentary, and do not allow the context to displace the
primary text.

If another meditation already exists for the same liturgical day:

- read it before composing the new meditation
- avoid repeating the same argument, image, quotation, or source chain unless
  deliberate resonance is useful
- harmonize with the existing meditation while keeping the new primary text
  distinct

## Local Citation Rules

- Psalm references follow the Vulgate numbering used by the traditional Roman
  liturgy.
- In the `Textus fundamentalis`, cite both the biblical locus and the liturgical
  use when the text is biblical, e.g. `(Act 1,1-11; Lectio Missae In Ascensione
  Domini)`.
- Later quotations from the same primary text normally cite only the biblical
  locus, e.g. `(Act 1,7)`, unless the liturgical context would otherwise be
  unclear.
- Keep the full liturgical reference when quoting another Mass or Office text
  that is not the primary meditation text.
- Divinum Officium data may be searched to identify other liturgical uses of a
  biblical text. Include such uses only when real and contextually relevant.

## Required Source Families

Each Usuale meditation should normally include:

- Scripture and the immediate liturgical text
- 3-5 patristic references where the theme allows
- medieval or scholastic deepening
- at least one reference to the Catechismus Romanus
- at least one reference to St. Alphonsus Maria de Liguori
- an organic Marian component

Preferred patristic authors include Augustine, Gregory the Great, Jerome,
Ambrose, and John Chrysostom. For Gospel meditations, Thomas Aquinas's
`Catena aurea` is a useful witness when it organically gathers patristic voices;
cite the original Father when identifiable and Thomas as the transmitting
source.

For the Catechismus Romanus, use the structured TEI/XML version of the 1761
Mainz edition available through UB Tuebingen OpenDigi as the normal working
text. Direct quotations should still be checked against the page image or a
reliable printed edition when feasible. Cite by Pars and caput, adding a more
precise division when available.

For St. Alphonsus, preserve the original language and orthography in direct
quotations. Italian quotations remain in Italian and should use typographic
apostrophes.

## Metadata

Every Usuale meditation begins with YAML front matter:

```yaml
---
id: meditatio-vocem-iucunditatis
title: "Meditatio de Introitu Dominicae V post Pascha"
celebration: celebratio-temporale-dominica-5-post-pascha
celebration_ref: ../indexes/celebrations.xml#celebratio-temporale-dominica-5-post-pascha
liturgical_form: missa
primary_section: Introitus
primary_source: ../../sources/divinum-officium/web/www/missa/Latin/Tempora/Pasc5-0.txt#Introitus
primary_incipit: "Vocem iucunditatis"
status: draft
---
```

Field meanings:

- `id`: stable identifier, normally matching the filename without `.md`
- `title`: displayed meditation title
- `celebration`: `xml:id` of the relevant item in `data/indexes/celebrations.xml`
- `celebration_ref`: relative link to that celebration entry
- `liturgical_form`: usually `missa` or `officium`
- `primary_section`: actual source section name, e.g. `Introitus`, `Lectio`,
  `Evangelium`, `Communio`
- `primary_source`: relative link to the current source witness and section
  anchor
- `primary_incipit`: short human-readable incipit
- `status`: editorial status, e.g. `draft`, `reviewed`, `final`

Use the actual Divinum Officium section name in `primary_section`. For example,
a Mass Epistle is currently linked as `Lectio`, because that is the source
section in the DO file.

Do not replace `celebration` with a date or DO filename. The meditation points
to the normalized liturgical celebration; source files remain evidence for the
current witness.

## Usuale Review Checklist

Before finishing, verify:

- the `celebration` ID exists in `data/indexes/celebrations.xml`
- `primary_section` and `primary_source` match the Divinum Officium witness
- the primary liturgical text remains central
- Mass or Office context is organic and not a second theme
- existing meditations for the same celebration have been considered
- required Usuale source families are present and not forced
- primary-text citations follow the concise repeat-reference rule
- the final Latin pass required by the shared guidelines has been made
