---
name: latin-liturgical-meditations
description: Use this skill when creating, revising, reviewing, or adding metadata for Usuale's traditional Catholic Latin meditations in data/meditations. It applies the repository's meditation guidelines, links meditations to celebrations.xml, checks liturgical context, citation style, source verifiability, and ecclesiastical Latin quality.
---

# Latin Liturgical Meditations

## Source of Truth

This is a Usuale project adapter for the shared Latin meditation guidelines.
Before working on a meditation, read the shared core and then the local overlay:

- `../../shared/latin-meditations-guidelines/skills/latin-meditations-core/SKILL.md`
- relevant files in `../../shared/latin-meditations-guidelines/guidelines/`
- `../../planning/meditations-guidelines.md`

Local Usuale rules override the shared guidelines when they are stricter or
more concrete.

Use the following supporting files as needed. Paths are relative to this skill
directory:

- `../../data/indexes/celebrations.xml` for `celebration` IDs
- `../../data/meditations/` for existing meditations on the same liturgical day
- `../../sources/divinum-officium/` for current DO source witnesses and liturgical context

## Workflow

1. Identify the primary liturgical text and its liturgical day.
2. Read the relevant source file in `../../sources/divinum-officium/` when a DO witness is used.
3. Find the matching `celebratio` in `../../data/indexes/celebrations.xml`.
4. Check `../../data/meditations/` for existing meditations on the same celebration.
5. Write or revise the meditation according to the shared guidelines and Usuale overlay.
6. Add or preserve YAML front matter with the required Usuale metadata.
7. Verify citations, direct quotations, `cf.` references, and liturgical references.
8. Check whether the chosen Alphonsus quotation or locator has already become
   repetitive in `../../data/meditations/`; choose another passage unless reuse
   is deliberately required.
9. Make a final Latin correction pass, especially for agreement, government, mood, and consistency of address to the soul.

## Markdown Location

Meditation files belong in:

```text
../../data/meditations/
```

Planning notes, style rules, and summaries remain in:

```text
../../planning/
```

See `../../planning/meditations-guidelines.md` for the required Usuale front matter
schema and Divinum Officium source-linking conventions.

## Review Checklist

Before finishing, verify:

- The `celebration` ID exists in `../../data/indexes/celebrations.xml`.
- The meditation keeps its primary liturgical text at the center.
- The Mass or Office context is used organically, not as a second theme.
- Required sources from the guidelines are present and not forced.
- Direct quotations are real, traceable, italicized, and cited immediately.
- Paraphrases use `cf.`.
- Alphonsus quotations preserve original language and orthography.
- Alphonsus references have been checked against existing meditations so the
  same quote or locator is not used as a stock conclusion.
- The Marian component is integrated organically.
- The Latin has received a final grammatical and stylistic pass.
