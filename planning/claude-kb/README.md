# Divinum Officium - Claude Knowledge Base

This directory contains comprehensive documentation and proposals for the Divinum Officium project modernization.

## Contents

### Core Documentation

1. **[project-overview.md](project-overview.md)**
   - Complete technical documentation of current system
   - File formats, directory structure, special characters
   - Perl script architecture
   - Data organization (Temporal, Sanctoral, Commune)
   - Gregorian chant integration
   - Multi-language support
   - **Audience**: Developers, new contributors

2. **[tei-data-model.md](tei-data-model.md)**
   - Comprehensive TEI XML specification for liturgical texts
   - Complete examples for all liturgical elements
   - XML schema definitions
   - Migration mapping from current format
   - XPath query examples
   - **Audience**: Technical team, TEI specialists

3. **[precedence-data-model.md](precedence-data-model.md)**
   - SQL database schema for precedence rules
   - Rule engine architecture
   - Version-specific strategies
   - Transfer resolution mechanisms
   - **Audience**: Backend developers, database designers

4. **[json-vs-sql-analysis.md](json-vs-sql-analysis.md)**
   - Comprehensive comparison of JSON vs SQL approaches
   - JSON directory structure proposal
   - Python implementation examples
   - Hybrid approach (JSON + SQLite cache)
   - **Audience**: Technical decision-makers

5. **[migration-proposal.md](migration-proposal.md)**
   - Complete 18-month migration plan
   - Architecture (TEI + JSON + SQLite + Python/Flask)
   - Phased implementation strategy
   - Risk assessment and mitigation
   - Resource requirements and timeline
   - **Audience**: Project stakeholders, decision-makers

6. **[mass-migration-addendum.md](mass-migration-addendum.md)**
   - Extension of migration proposal to include Mass (Missa)
   - TEI structure for Mass propers
   - Updated timeline (21-24 months)
   - Mass-specific considerations
   - **Audience**: Project planners

### Presentation Materials

7. **[tei-presentation.md](tei-presentation.md)**
   - Markdown source for TEI proposal presentation
   - 60+ slides covering all aspects
   - Can be edited and customized
   - **Format**: Markdown with YAML frontmatter

8. **[tei-presentation.html](tei-presentation.html)** ⭐
   - **Interactive HTML presentation using reveal.js**
   - Fully standalone (no internet required after download)
   - Navigate with arrow keys or click
   - **How to use**: Open in any web browser
   - **URL**: `file:///path/to/tei-presentation.html`

9. **[json-precedence-presentation.md](json-precedence-presentation.md)**
   - Markdown source for JSON precedence solution presentation
   - 80+ slides covering JSON architecture in detail
   - Deep dive into JSON-based rule system
   - **Format**: Markdown with YAML frontmatter

10. **[json-precedence-presentation.html](json-precedence-presentation.html)** ⭐
    - **Interactive HTML presentation using reveal.js**
    - Comprehensive coverage of JSON precedence approach
    - Code examples, rule definitions, migration strategy
    - **How to use**: Open in any web browser
    - **URL**: `file:///path/to/json-precedence-presentation.html`

11. **[convert-presentation.py](convert-presentation.py)**
    - Python script to convert Markdown to HTML presentation
    - Uses reveal.js for slide rendering
    - Accepts command-line arguments for flexible conversion
    - **Usage**: `python3 convert-presentation.py input.md output.html`

## How to Use

### Viewing the Presentations

**Option 1: HTML Version (Recommended)**
```bash
# TEI Data Model presentation (macOS)
open claude-kb/tei-presentation.html

# JSON Precedence presentation (macOS)
open claude-kb/json-precedence-presentation.html

# Open in default browser (Linux)
xdg-open claude-kb/tei-presentation.html
xdg-open claude-kb/json-precedence-presentation.html

# Open in default browser (Windows)
start claude-kb/tei-presentation.html
start claude-kb/json-precedence-presentation.html
```

Or simply double-click the HTML files in your file browser.

**Navigation**:
- **Arrow keys**: Navigate slides (→ next, ← previous, ↓ down, ↑ up)
- **Space**: Next slide
- **ESC**: Overview mode (see all slides)
- **F**: Fullscreen mode
- **S**: Speaker notes (if any)

**Option 2: Markdown Source**
```bash
# View in any Markdown viewer
code tei-presentation.md               # TEI presentation
code json-precedence-presentation.md   # JSON presentation
```

### Converting to PDF

If you need a PDF version:

**Method 1: Print from Browser**
1. Open the HTML presentation in Chrome/Edge
2. Press `Ctrl+P` (Windows/Linux) or `Cmd+P` (macOS)
3. Choose "Save as PDF"
4. Adjust settings:
   - Layout: Landscape
   - Margins: None
   - Background graphics: On

**Method 2: Using decktape (if installed)**
```bash
npm install -g decktape
decktape reveal tei-presentation.html tei-presentation.pdf
decktape reveal json-precedence-presentation.html json-precedence-presentation.pdf
```

### Editing the Presentations

1. **Edit Markdown source**:
   ```bash
   code tei-presentation.md               # For TEI presentation
   code json-precedence-presentation.md   # For JSON presentation
   ```

2. **Regenerate HTML**:
   ```bash
   # Regenerate specific presentation
   python3 convert-presentation.py tei-presentation.md tei-presentation.html
   python3 convert-presentation.py json-precedence-presentation.md json-precedence-presentation.html

   # Or use default (regenerates tei-presentation.html)
   python3 convert-presentation.py
   ```

3. **Refresh browser** to see changes

## Document Status

| Document | Version | Last Updated | Status |
|----------|---------|--------------|--------|
| project-overview.md | 1.0 | 2025-12-28 | Complete |
| tei-data-model.md | 1.0 | 2025-12-28 | Complete |
| precedence-data-model.md | 1.0 | 2025-12-28 | Complete |
| json-vs-sql-analysis.md | 1.0 | 2025-12-28 | Complete |
| migration-proposal.md | 1.0 | 2025-12-28 | Complete |
| mass-migration-addendum.md | 1.0 | 2025-12-28 | Complete |
| tei-presentation.md | 1.0 | 2025-12-28 | Complete |
| tei-presentation.html | 1.0 | 2025-12-28 | Complete |
| json-precedence-presentation.md | 1.0 | 2025-12-29 | Complete |
| json-precedence-presentation.html | 1.0 | 2025-12-29 | Complete |
| convert-presentation.py | 1.1 | 2025-12-29 | Complete |

## Quick Start Guide

### For Project Stakeholders
1. Start with: **[migration-proposal.md](migration-proposal.md)**
2. View presentation: **[tei-presentation.html](tei-presentation.html)**
3. Review addendum: **[mass-migration-addendum.md](mass-migration-addendum.md)**

### For Technical Team
1. Current system: **[project-overview.md](project-overview.md)**
2. TEI specification: **[tei-data-model.md](tei-data-model.md)**
3. Data architecture: **[json-vs-sql-analysis.md](json-vs-sql-analysis.md)**
4. Precedence logic: **[precedence-data-model.md](precedence-data-model.md)**

### For New Contributors
1. Start with: **[project-overview.md](project-overview.md)**
2. Understand proposal: **[migration-proposal.md](migration-proposal.md)**
3. View presentation: **[tei-presentation.html](tei-presentation.html)**

## Key Recommendations

Based on comprehensive analysis:

### ✅ Recommended Approach

**Architecture**: TEI XML + JSON Rules + SQLite Cache + Python/Flask

**Why**:
- TEI: Industry standard for liturgical texts
- JSON: Git-friendly, human-editable rules
- SQLite: Performance cache, queryable
- Python/Flask: Modern, maintainable

**Timeline**: 21-24 months (including Mass)

**Scope**: Divine Office + Mass together

### Benefits

✅ **Scholarly**: TEI standard, citeable, preservable
✅ **Quality**: XML validation prevents errors
✅ **Flexible**: Multiple output formats from single source
✅ **Maintainable**: Modern stack, good tooling
✅ **Future-proof**: Standards-based, long-term preservation

### Trade-offs

⚠️ **Time**: 21-24 months development effort
⚠️ **Learning**: TEI has learning curve
⚠️ **Resources**: Need 2-3 part-time developers
⚠️ **Risk**: Complex migration, needs careful validation

## Next Steps

### If Proceeding with Migration

**Month 1**:
- [ ] Form development team
- [ ] Set up development environment
- [ ] Design TEI schema (draft)
- [ ] Build proof-of-concept

**Month 2-3**:
- [ ] Refine schema
- [ ] Convert sample offices
- [ ] Validate approach
- [ ] Build conversion tools

**Month 4+**:
- [ ] Full data conversion
- [ ] Python engine development
- [ ] Web interface
- [ ] Testing and launch

## Contact & Contributing

- **Repository**: https://github.com/DivinumOfficium/divinum-officium
- **Website**: https://divinumofficium.com/
- **Issues**: https://github.com/DivinumOfficium/divinum-officium/issues

## License

This documentation is part of the Divinum Officium project and is available under the MIT License.

---

**Generated by**: Claude AI (Sonnet 4.5)
**Date**: December 28, 2025
**Purpose**: Migration Planning Documentation
