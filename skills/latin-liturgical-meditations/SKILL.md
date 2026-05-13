---
name: latin-liturgical-meditations
description: Use this skill when creating, revising, reviewing, or adding metadata for Usuale's traditional Catholic Latin meditations in data/meditations. It applies the repository's meditation guidelines, links meditations to celebrations.xml, checks liturgical context, citation style, source verifiability, and ecclesiastical Latin quality.
---

# Latin Liturgical Meditations

## Source of Truth

Do not duplicate the meditation rules in this skill. Before working on a
meditation, read:

- `planning/meditations-guidelines.md`

Use the following supporting files as needed:

- `data/indexes/celebrations.xml` for `celebration` IDs
- `data/meditations/` for existing meditations on the same liturgical day
- `sources/divinum-officium/` for current DO source witnesses and liturgical context

## Workflow

1. Identify the primary liturgical text and its liturgical day.
2. Read the relevant source file in `sources/divinum-officium/` when a DO witness is used.
3. Find the matching `celebratio` in `data/indexes/celebrations.xml`.
4. Check `data/meditations/` for existing meditations on the same celebration.
5. Write or revise the meditation according to `planning/meditations-guidelines.md`.
6. Add or preserve YAML front matter with the required metadata.
7. Verify citations, direct quotations, `cf.` references, and liturgical references.
8. Make a final Latin correction pass, especially for agreement, government, mood, and consistency of address to the soul.

## Markdown Location

Meditation files belong in:

```text
data/meditations/
```

Planning notes, style rules, and summaries remain in:

```text
planning/
```

## Required Front Matter

Every meditation must begin with YAML front matter in this form:

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

Use the actual DO section name in `primary_section` when linking to a DO source
file, e.g. `Lectio` for the Mass Epistle if that is the section name in DO.

## Review Checklist

Before finishing, verify:

- The `celebration` ID exists in `data/indexes/celebrations.xml`.
- The meditation keeps its primary liturgical text at the center.
- The Mass or Office context is used organically, not as a second theme.
- Required sources from the guidelines are present and not forced.
- Direct quotations are real, traceable, italicized, and cited immediately.
- Paraphrases use `cf.`.
- Alphonsus quotations preserve original language and orthography.
- The Marian component is integrated organically.
- The Latin has received a final grammatical and stylistic pass.
