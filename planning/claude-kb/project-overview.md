# Divinum Officium - Project Overview

## Table of Contents
1. [Introduction](#introduction)
2. [Technical Architecture](#technical-architecture)
3. [Directory Structure](#directory-structure)
4. [Data Organization](#data-organization)
5. [File Format Specification](#file-format-specification)
6. [Special Characters and Markup](#special-characters-and-markup)
7. [Ranking System](#ranking-system)
8. [Rubrical Versions](#rubrical-versions)
9. [Key Perl Scripts](#key-perl-scripts)
10. [Gregorian Chant Integration](#gregorian-chant-integration)
11. [Multi-Language Support](#multi-language-support)
12. [Development Setup](#development-setup)

---

## Introduction

**Divinum Officium** is a web-based application for praying the traditional Divine Office (Liturgy of the Hours) and Mass according to various historical rubrics of the Roman Catholic Church.

- **Website**: https://www.divinumofficium.com/
- **Repository**: https://github.com/DivinumOfficium/divinum-officium
- **License**: MIT License
- **Primary Language**: Perl 5.6+
- **Data Format**: UTF-8 encoded text files

### Project Philosophy
The project emphasizes open documentation and encourages developers to understand and potentially create their own implementations. All code and data are freely available for modification and distribution.

---

## Technical Architecture

### Core Technologies
- **Backend**: Perl 5.6+ (CGI scripts)
- **Frontend**: HTML generation with JavaScript enhancements
- **Encoding**: UTF-8 (legacy Windows-1252 support deprecated)
- **Chant Display**: GABC notation processed via exsurge JavaScript library

### Main Scripts

#### For Divine Office (Horas)
- `officium.pl` - Desktop version entry point
- `Pofficium.pl` - Mobile interface entry point
- `horas.pl` - Core office generation logic
- `horascommon.pl` - Date handling and precedence rules
- `specials.pl` - Special character processing and content expansion
- `webdia.pl` - Web dialog handling

#### For Mass (Missa)
- `missa.pl` - Main Mass script
- `Cmissa.pl` - Common Mass functions
- `Emissa.pl` - Additional Mass functionality

### Processing Pipeline
1. User selects date, language, version (rubric)
2. `horascommon.pl` determines precedence (Tempora vs Sancti)
3. `horas.pl` retrieves appropriate Ordinarium skeleton
4. `specials.pl` populates skeleton with specific content
5. Special characters (@, $, #, ~, !) are resolved
6. HTML output is generated and displayed

---

## Directory Structure

```
divinum-officium-master/
├── web/                          # Main web application
│   ├── cgi-bin/                  # Perl CGI scripts
│   │   ├── horas/                # Divine Office scripts
│   │   │   ├── officium.pl       # Desktop version
│   │   │   ├── Pofficium.pl      # Mobile version
│   │   │   ├── horas.pl          # Main office logic
│   │   │   ├── horascommon.pl    # Date/precedence logic
│   │   │   ├── specials.pl       # Content processing
│   │   │   ├── webdia.pl         # Dialog handling
│   │   │   └── kalendar/         # Calendar utilities
│   │   └── missa/                # Mass scripts
│   │       ├── missa.pl
│   │       ├── Cmissa.pl
│   │       └── ordo.pl
│   └── www/                      # Static files and data
│       ├── horas/                # Divine Office data
│       │   ├── Latin/            # Latin texts (primary)
│       │   ├── English/          # English translations
│       │   ├── Francais/         # French
│       │   ├── Italiano/         # Italian
│       │   ├── Espanol/          # Spanish
│       │   ├── Polski/           # Polish
│       │   ├── Magyar/           # Hungarian
│       │   ├── Deutsch/          # German
│       │   ├── Help/             # Documentation
│       │   └── Ordinarium/       # Hour structures
│       ├── missa/                # Mass data (similar structure)
│       ├── Tabulae/              # Transfer tables
│       ├── js/                   # JavaScript libraries
│       └── style/                # CSS styles
├── admin/                        # Administrative tools
├── standalone/                   # eBook generation tools
├── docker/                       # Docker configurations
├── regress/                      # Regression tests
├── obsolete/                     # Deprecated files
└── claude-kb/                    # Claude knowledge base
```

---

## Data Organization

Each language folder (e.g., `web/www/horas/Latin/`) contains identical subfolder structures:

### Main Data Categories

#### 1. **Psalterium**
- Contains 150 biblical psalms plus canticles
- Common prayers and responses
- Doxologies and blessings
- Invitatory texts
- Organized in subdirectories:
  - `Psalmi/` - Individual psalm files
  - `Common/` - Shared elements
  - `Special/` - Special variations

#### 2. **Tempora** (Temporal/Seasonal Cycle)
- Liturgical seasons and their offices
- Naming convention: `Season##-#.txt`
  - Examples:
    - `Adv1-0.txt` - First Sunday of Advent
    - `Quad3-2.txt` - Tuesday of Third Week of Lent
    - `Pasc1-0.txt` - Easter Sunday
    - `Pent05-4.txt` - Thursday of Fifth Week after Pentecost
- Covers entire liturgical year
- Includes special seasons:
  - Advent (Adv)
  - Christmas (Nat)
  - Epiphany (Epi)
  - Lent (Quad, Quadp for Passiontide)
  - Easter (Pasc)
  - Pentecost (Pent)

#### 3. **Sancti** (Sanctoral Cycle - Saints' Feasts)
- Saints' feast days and solemnities
- Naming convention: `MM-DD.txt` (month-day)
  - Examples:
    - `01-01.txt` - Circumcision/Octave of Christmas (January 1)
    - `03-25.txt` - Annunciation (March 25)
    - `12-25.txt` - Christmas (December 25)
- Special suffixes:
  - `MM-DDv.txt` - Vigil
  - `MM-DDn.txt` - Additional commemorations
- Variants for different rubrics:
  - `SanctiM/` - Monastic version
  - `SanctiCist/` - Cistercian version
  - `SanctiOP/` - Dominican (Order of Preachers)

#### 4. **Commune** (Common Offices)
- Templates for classes of saints
- Used when specific saint lacks proper office
- Files named C1-C12 with variants:
  - `C1.txt` - Apostles
  - `C2.txt` - One Martyr (not Bishop)
  - `C3.txt` - Several Martyrs
  - `C4.txt` - Confessor Bishop
  - `C5.txt` - Confessor not Bishop
  - `C6.txt` - Virgins
  - `C7.txt` - Holy Women
  - `C10.txt` - Dedication of a Church
  - Variants with suffixes (a, b, p, etc.) for different options

#### 5. **Martyrologium**
- Daily martyrology readings
- Multiple versions:
  - `Martyrologium/` - Standard
  - `Martyrologium1570/` - 1570 edition
  - `Martyrologium1955R/` - 1955 revised
  - `Martyrologium1960/` - 1960 edition
- One file per day of year (366 files)

#### 6. **Ordinarium**
- Structural templates for each canonical hour
- Files like `Matutinum.txt`, `Laudes.txt`, `Vespera.txt`
- Define the order and flow of each hour

---

## File Format Specification

### Section-Based Structure
Files use sections denoted by square brackets containing liturgical elements:

```
[Rank]
Rank designation;;Class;;Numerical rank;;References

[Rule]
Processing directives

[Ant Vespera]
Antiphon text for Vespers;;Psalm number

[Hymnus Matutinum]
Hymn text for Matins

[Lectio4]
Fourth reading text

[Responsory3]
R. Response text
V. Verse text
R. Repeated response
&Gloria
R. Final response
```

### Common Section Names

#### Structural Sections
- `[Rank]` - Feast rank and classification
- `[Rule]` - Processing rules and directives
- `[Officium]` - Name of the office/feast

#### Vespers (Evening Prayer)
- `[Ant Vespera]` - Vespers antiphons
- `[Hymnus Vespera]` - Vespers hymn
- `[Versum 1]` - Vespers verse
- `[Oratio]` - Collect prayer

#### Matins (Night Office)
- `[Ant Matutinum]` - Matins antiphons
- `[Invitatorium]` - Invitatory
- `[Hymnus Matutinum]` - Matins hymn
- `[Lectio1]` through `[Lectio9]` - Nine readings
- `[Responsory1]` through `[Responsory9]` - Responsories

#### Lauds (Morning Prayer)
- `[Ant Laudes]` - Lauds antiphons
- `[Hymnus Laudes]` - Lauds hymn
- `[Versum 2]` - Lauds verse
- `[Ant Benedictus]` - Benedictus antiphon

#### Little Hours
- `[Ant Prima]`, `[Ant Tertia]`, `[Ant Sexta]`, `[Ant Nona]`
- `[Capitulum Prima]` - Chapter reading
- `[Responsory Breve Prima]` - Short responsory

#### Compline (Night Prayer)
- `[Ant Completorium]` - Compline antiphon
- `[Hymnus Completorium]` - Compline hymn

### Conditional Sections
Sections can have conditional suffixes in parentheses:

```
[Rank] (rubrica 1960)
Content for 1960 rubrics only

[Ant Vespera] (rubrica cisterciensis)
Content for Cistercian version

[Hymnus] (sed rubrica tridentina)
Content except for Tridentine rubrics

[Oratio] (nisi rubrica praedicatorum)
Content unless Dominican rubrics
```

---

## Special Characters and Markup

### Cross-References: `@`
References content from other files:

```
@Tempora/Nat1-0
```
Includes content from `Tempora/Nat1-0.txt`

```
@Sancti/12-25:Versum 2
```
Includes the `[Versum 2]` section from `Sancti/12-25.txt`

### Prayer References: `$`
References standard prayers:

```
$Qui tecum
```
Expands to standard ending: "Qui tecum vivit et regnat..."

```
$Per Dominum
```
Standard conclusion

```
$Deo gratias
```
"Thanks be to God" response

### Chapter Labels: `#`
Marks headings and labels, often used for rubrical directions:

```
#Lectio i
```

### Red Text (Rubrics): `!`
Text that should appear in red (liturgical directions):

```
!Psalmi 109, 110, 111
!Post Benedictus non dicitur Fidelium animae
```

### Line Contractions: `~`
Indicates abbreviated text:

```
Deus in adjutorium~
```

### Psalm Numbers
Appended to antiphons with `;;`:

```
Allelúja, allelúja, allelúja.;;109
```
Uses Psalm 109 with this antiphon

### Formatting Markers
- `_` - Line break within hymn stanzas
- `v.` - Verse marker
- `&Gloria` - Insert Gloria Patri
- `*` - Indicates pause or asterisk in chant notation

---

## Ranking System

Feasts are assigned numerical ranks determining precedence and liturgical treatment:

### Rank Scale (1.0 to 7.0)

#### Highest Ranks
- **7.0** - Supreme solemnities (Easter, Christmas in octave)
- **6.5** - Major solemnities (Trinity Sunday)
- **6.0** - First class doubles (major feasts)
- **5.9** - Second class doubles (1570 system)
- **5.0** - Second class doubles

#### Middle Ranks
- **4.0** - Third class doubles (lesser major feasts)
- **3.0** - Major doubles
- **2.0** - Minor doubles / Semidoubles
- **1.5** - Semidoubles

#### Lower Ranks
- **1.0** - Simples and commemorations

### Rank Format in Files
```
[Rank]
Feast Name;;Double I class;;6.0;;ex Sancti/12-25
```

Components:
1. Feast name
2. Liturgical classification
3. Numerical rank
4. Optional reference (`ex` = derives from)

### Precedence Rules
- Higher numerical rank takes precedence
- On conflicts, system determines:
  - Primary office (winner)
  - Commemorations (commemoratio)
  - Vespers handling (vespera)
- Transfer rules apply when higher feast displaces lower
- Special rules for Sundays, octaves, and vigils

---

## Rubrical Versions

The system supports multiple historical and religious order versions:

### Historical Rubrics

#### Tridentine (1570)
- `(rubrica tridentina)` or `(rubrica 1570)`
- Post-Trent reform by Pope Pius V
- Most traditional form

#### 1955 Revision
- `(rubrica 1955)`
- Simplified rubrics under Pope Pius XII
- Reduced octaves and doubles

#### 1960 Code
- `(rubrica 1960)` or `(rubrica 196)`
- Last pre-Vatican II revision
- Further simplifications

### Religious Order Variants

#### Monastic
- `(rubrica monastic)` or `TemporaM/`, `SanctiM/`
- Benedictine monastic breviary
- Different psalm distribution

#### Cistercian
- `(rubrica cisterciensis)` or `CommuneCist/`, `SanctiCist/`
- Cistercian Order variations
- Simplified office structure

#### Dominican (Order of Preachers)
- `(rubrica praedicatorum)` or `SanctiOP/`, `TemporaOP/`
- Dominican rite
- Unique proper feasts

### Conditional Logic Keywords
Used in `[Rule]` sections to handle variations:

- `si` - if
- `deinde` - then
- `vero` - but/however
- `sed` - except
- `atque` - and also
- `attamen` - nevertheless
- `nisi` - unless

Example:
```
[Hymnus] (nisi rubrica praedicatorum)
Standard hymn unless Dominican rite
```

---

## Key Perl Scripts

### horas.pl
**Purpose**: Main office generation engine

**Key Functions**:
- `horas($hora)` - Generates complete office for specified hour
- `resolve_refs()` - Resolves @ and $ references
- `adhoram()` - Formats hour headings

**Responsibilities**:
- Collects appropriate scripts for each hour
- Handles GABC chant suppression during Triduum
- Manages dual-column display (two languages)
- Calls specials.pl for content expansion

**Special Variables**:
- `$hora` - Current canonical hour (Matutinum, Laudes, etc.)
- `$lang1`, `$lang2` - Display languages
- `$version` - Active rubrical version
- `$only` - Single column mode flag

### horascommon.pl
**Purpose**: Date handling and precedence logic

**Key Functions**:
- `occurrence()` - Determines winning office for a date
- `getweek()` - Calculates liturgical week
- `get_sday()` - Gets sanctoral day string (MM-DD)
- `precedence()` - Resolves conflicts between Tempora/Sancti

**Responsibilities**:
- Reads from Directorium (transfer tables)
- Handles transfers of feasts
- Calculates Easter and movable feasts
- Determines commemorations
- Manages Vespers precedence

**Key Variables**:
- `$winner` - Winning office file
- `$rank` - Rank of winning office
- `$commemoratio` - Commemoration office
- `%tempora` - Temporal cycle data
- `%saint` - Sanctoral cycle data

### specials.pl
**Purpose**: Content expansion and special character processing

**Responsibilities**:
- Processes `#` chapter markers
- Expands skeleton structures
- Handles conditional logic (si, deinde, vero)
- Psalm distribution
- Manages "Building Script" display
- Processes rubrical variations

**Functions**:
- `specials(\@script, $lang)` - Main processing entry point
- Dispatches to specialized handlers based on content type

### webdia.pl
**Purpose**: Web interface and HTML generation

**Responsibilities**:
- Dialog handling (date selection, options)
- HTML output formatting
- CSS and JavaScript integration
- User preference management
- Dual-column layout generation

### officium.pl vs Pofficium.pl
- `officium.pl` - Desktop/full web interface
- `Pofficium.pl` - Mobile-optimized interface
- Both call same underlying horas.pl logic
- Differ in presentation and UI elements

### DivinumOfficium Modules
Located in `web/cgi-bin/DivinumOfficium/`:

- `LanguageTextTools.pm` - Text processing utilities
- `Date.pm` - Date calculation functions
- `Directorium.pm` - Transfer and precedence tables
- `Scripting.pm` - Script parsing and execution

---

## Gregorian Chant Integration

### GABC Notation
- **Format**: Text-based chant notation
- **Library**: exsurge JavaScript library renders GABC to visual notation
- **File Extension**: `.gabc` or embedded in text files

### Latin-gabc Language
- Special language variant: `Latin-gabc`
- Contains GABC notation alongside Latin text
- Automatically rendered when selected

### Chant Sections
Special section names for chant:

```
[Ant Vespera GABC]
name: Antiphon name;
%%
(c4) An(f)ti(g)phon(h) text(g) with(f) notes(e)
```

### Tone Adjustments
- System automatically selects appropriate psalm tones
- Based on:
  - Liturgical hour (Vespers, Lauds, etc.)
  - Mode of antiphon
  - Rubrical requirements

### Suppression Rules
Chant automatically suppressed for:
- Triduum little hours (Prima, Tertia, Sexta, Nona, Completorium)
- Cistercian version (currently)
- Dominican version (currently)

### Integration in horas.pl
```perl
if ($version =~ /Cisterciensis|Praedicatorum/
  || (triduum_gloria_omitted() && $hora =~ /Prima|Tertia|Sexta|Nona|Completorium/i))
{
  $lang1 =~ s/\-gabc//;  # Remove -gabc from Language
  $lang2 =~ s/\-gabc//;
}
```

---

## Multi-Language Support

### Available Languages
Based on directories in `web/www/horas/`:

1. **Latin** - Primary reference language
2. **English** - Complete translation
3. **Français** (French)
4. **Italiano** (Italian)
5. **Español** (Spanish)
6. **Polski** (Polish)
7. **Magyar** (Hungarian)
8. **Deutsch** (German)
9. **Nederlands** (Dutch)
10. **Português** (Portuguese)
11. **Bohemice** (Czech/Bohemian)
12. **Cesky-Schaller** (Czech variant)
13. **Dansk** (Danish)
14. **Ukrainian**
15. **Vietnamice** (Vietnamese)

### Special Language Variants
- `Latin-gabc` - Latin with GABC chant notation
- `Latin-Bea` - Bea psalter variant

### Fallback Mechanism
From technical documentation:
> "If a file is missing for a specific modern language, the program automatically selects the language text from the English."

Fallback order:
1. Requested language
2. English
3. Latin (always present)

### Dual-Column Display
- Users can display two languages simultaneously
- Controlled by `$lang1` and `$lang2` variables
- `$only` flag determines single vs dual column mode

### File Completeness
Not all languages have complete translations:
- Latin: 100% (reference)
- English: Near complete
- Other languages: Varying degrees of completion
- Missing files automatically fall back

### Translation Structure
Each language maintains identical folder structure:
```
Language/
├── Psalterium/
├── Tempora/
├── Sancti/
├── Commune/
└── Martyrologium/
```

This ensures consistent file referencing across languages.

---

## Development Setup

### Docker (Recommended)

#### Production
```bash
# Pull pre-built container
docker pull ghcr.io/divinumofficium/divinum-officium:master

# Or use docker-compose
wget https://raw.githubusercontent.com/DivinumOfficium/divinum-officium/master/docker-compose-prod.yml
docker-compose -f docker-compose-prod.yml up -d

# Access at http://localhost:80
```

#### Development
```bash
# In repository root
docker-compose up

# Access at http://localhost:8080
# Changes to files are live-mounted (no restart needed)
```

### Manual Setup

#### Requirements
- Perl 5.6 or higher
- CGI-capable web server (Apache recommended)
- UTF-8 support

#### Configuration
1. Point web server document root to `web/www/`
2. Configure CGI execution for `web/cgi-bin/`
3. Ensure Perl modules are accessible
4. Set proper permissions on directories

#### Testing
```bash
# Run regression tests
cd regress/
# (test scripts available here)
```

### File Editing

#### Encoding
- **REQUIRED**: UTF-8 encoding
- Windows-1252 deprecated but still supported
- Configure editor for UTF-8 without BOM

#### EditorConfig
Project includes `.editorconfig`:
```
# Ensures consistent formatting
# Supported by most modern editors
```

#### Perl Tidy
Use provided `.perltidyrc` for code formatting:
```bash
./perltidy.sh
```

### Version Control

#### Git Workflow
1. Fork repository on GitHub
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

#### Small Changes
- Can edit directly in GitHub web interface
- Automatic pull request creation
- Useful for typo fixes and minor corrections

### Contributing Guidelines

#### Data Files
- Location: `web/www/horas/` and `web/www/missa/`
- Format: UTF-8 text with section markers `[Section Name]`
- Browse existing files for examples
- Maintain consistent structure across languages

#### Code Changes
- Follow existing Perl style
- Use `perltidy` for formatting
- Test with multiple rubrics/languages
- Document complex logic

#### Documentation
- Technical docs: `web/www/horas/Help/`
- This knowledge base: `claude-kb/`
- Keep documentation synchronized with code

---

## Additional Resources

### Official Documentation
- Website: https://www.divinumofficium.com/
- Technical Help: https://www.divinumofficium.com/www/horas/Help/technical.html
- Repository: https://github.com/DivinumOfficium/divinum-officium

### Key Directories for Reference
- Examples of data files: `web/www/horas/Latin/Sancti/`
- Script examples: `web/cgi-bin/horas/`
- Help files: `web/www/horas/Help/`
- Transfer tables: `web/www/Tabulae/`

### Testing
- Regression tests: `regress/`
- Test with different dates to verify precedence
- Test with different languages for fallback
- Test with different rubrics for conditionals

---

## Common Tasks Reference

### Adding a New Saint
1. Create file in `web/www/horas/Latin/Sancti/MM-DD.txt`
2. Add `[Rank]` section with appropriate class
3. Add liturgical texts in appropriate sections
4. Add translations in other language folders
5. Update transfer tables if needed (in `Tabulae/`)

### Modifying Existing Office
1. Locate file (Sancti/MM-DD.txt or Tempora/XXX.txt)
2. Edit appropriate section `[Section Name]`
3. Test with multiple rubrics if using conditionals
4. Verify cross-references (@) still work

### Adding Translation
1. Create language folder if not exists
2. Mirror Latin folder structure
3. Translate section by section
4. Missing files will fall back to English/Latin

### Debugging
1. Check `$error` variable output in page
2. Verify file paths and cross-references
3. Check rank and precedence calculations
4. Test special character resolution (@, $, #)
5. Verify conditional logic (rubrica statements)

---

**Document Version**: 1.0
**Last Updated**: 2025-12-28
**Maintained for**: Claude AI Knowledge Base
