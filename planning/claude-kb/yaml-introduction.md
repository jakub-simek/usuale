---
title: "YAML: A Human-Friendly Data Format"
author: "Claude AI"
date: "2025-12-29"
theme: "serif"
---

# YAML
## A Human-Friendly Data Format

**YAML Ain't Markup Language**

Understanding YAML for the Divinum Officium Project

---

## Agenda

1. What is YAML?
2. Basic Syntax
3. Data Types
4. Advanced Features
5. YAML vs JSON
6. Why YAML for Precedence Rules?
7. Real Examples from Our Project
8. Tools and Best Practices

---

# Part 1: What is YAML?

---

## What is YAML?

**YAML** = **Y**AML **A**in't **M**arkup **L**anguage

**Purpose**: Human-readable data serialization format

**Common Uses**:
- Configuration files (Docker, Kubernetes, GitHub Actions)
- Data exchange between programs
- Structured documentation
- Rule definitions

**Philosophy**: Optimized for human readability over machine efficiency

---

## Why Was YAML Created?

**Problems with existing formats:**

❌ **XML**: Too verbose, hard to read
```xml
<person>
  <name>John Smith</name>
  <age>42</age>
</person>
```

❌ **JSON**: Requires quotes, no comments, rigid syntax
```json
{
  "name": "John Smith",
  "age": 42
}
```

✅ **YAML**: Clean, readable, flexible
```yaml
name: John Smith
age: 42
```

---

## YAML History

**Timeline**:
- **2001**: First released by Clark Evans
- **2004**: YAML 1.0 specification
- **2009**: YAML 1.2 (current standard)

**Adoption**:
- Docker Compose
- Kubernetes configurations
- Ansible playbooks
- GitHub Actions
- Many programming language configs

**Fact**: YAML is a superset of JSON (all valid JSON is valid YAML)

---

# Part 2: Basic Syntax

---

## Key-Value Pairs

The most basic YAML structure:

```yaml
# Simple key-value pairs
name: John Smith
age: 42
city: Rome
occupation: Liturgist
```

**Rules**:
- Key and value separated by colon and space (`: `)
- No quotes needed for simple strings
- Indentation matters!
- `#` starts a comment (ignored by parser)

---

## Strings

**Simple strings** (no quotes needed):
```yaml
name: John Smith
title: Duplex I classis
```

**Strings with special characters** (quotes needed):
```yaml
message: "Hello, World!"
path: 'C:\Users\John'
```

**Multi-line strings**:
```yaml
# Literal block (preserves newlines)
description: |
  This is a long description
  that spans multiple lines
  and preserves line breaks.

# Folded block (folds into single line)
summary: >
  This text will be folded
  into a single line when
  parsed by the program.
```

---

## Numbers and Booleans

**Numbers**:
```yaml
# Integers
age: 42
year: 1960

# Floats
priority: 1.5
temperature: -3.14

# Scientific notation
large_number: 1.23e+10
```

**Booleans**:
```yaml
enabled: true
disabled: false

# Also valid (case-insensitive)
flag1: True
flag2: FALSE
flag3: yes
flag4: no
```

---

## Lists (Arrays)

**Block style** (recommended):
```yaml
# List of strings
feasts:
  - Christmas
  - Easter
  - Pentecost
  - Epiphany

# List of numbers
priorities:
  - 1.0
  - 1.5
  - 2.0
```

**Flow style** (compact):
```yaml
feasts: [Christmas, Easter, Pentecost]
priorities: [1.0, 1.5, 2.0]
```

**Note**: Flow style is like JSON arrays

---

## Nested Lists

```yaml
# List of lists
calendar:
  - [January, February, March]
  - [April, May, June]
  - [July, August, September]
  - [October, November, December]

# Or in block style
calendar:
  -
    - January
    - February
    - March
  -
    - April
    - May
    - June
```

---

## Dictionaries (Objects)

**Simple dictionary**:
```yaml
person:
  name: John Smith
  age: 42
  city: Rome
```

**Nested dictionaries**:
```yaml
liturgy:
  office:
    name: Vespers
    time: 18:00
  feast:
    name: Christmas
    rank: Duplex I classis
    date: 12-25
```

---

## Combining Lists and Dictionaries

**List of dictionaries** (very common):
```yaml
feasts:
  - name: Christmas
    date: 12-25
    rank: Duplex I classis

  - name: Epiphany
    date: 01-06
    rank: Duplex I classis

  - name: Easter
    rank: Duplex I classis
    moveable: true
```

---

# Part 3: Data Types

---

## Null Values

**Representing null/empty**:
```yaml
# All these represent null
unknown: null
missing: ~
empty:

# In a list
values:
  - 1
  - null
  - 3
  - ~
```

**Use case**: Optional fields that may not have values

---

## Dates and Timestamps

**ISO 8601 format** (automatically parsed):
```yaml
# Dates
christmas: 2025-12-25
epiphany: 2025-01-06

# Timestamps
created: 2025-12-29T14:30:00Z
updated: 2025-12-29 14:30:00

# Alternative format
event_date: !!timestamp 2025-12-25 00:00:00
```

**Note**: Different YAML parsers may handle dates differently

---

## Type Casting

**Explicit types** using `!!`:
```yaml
# Force string (even though it looks like number)
version: !!str 1960

# Force integer
rank: !!int "42"

# Force float
priority: !!float 1

# Binary data
image: !!binary |
  R0lGODlhDAAMAIQAAP//9/X
  17unp5WZmZgAAAOfn515eXv
```

**Usually not needed** - YAML infers types correctly

---

# Part 4: Advanced Features

---

## Anchors and Aliases

**Problem**: Repeating the same data
```yaml
# Without anchors - repetitive
feast1:
  rank: Duplex I classis
  priority: 1.0

feast2:
  rank: Duplex I classis
  priority: 1.0
```

**Solution**: Anchors (`&`) and aliases (`*`)
```yaml
# Define once with anchor
default_rank: &high_rank
  rank: Duplex I classis
  priority: 1.0

# Reuse with alias
feast1: *high_rank
feast2: *high_rank
```

---

## Anchors - Detailed Example

```yaml
# Define base configuration
base_office: &base
  language: Latin
  version: 1960
  rubrics: true

# Reuse in multiple places
vespers:
  <<: *base  # Merge base settings
  hour: Vespers
  time: 18:00

lauds:
  <<: *base  # Merge base settings
  hour: Lauds
  time: 06:00
```

**Result**: DRY (Don't Repeat Yourself) principle

---

## Merging with `<<`

**Merge keys** to combine dictionaries:
```yaml
defaults: &defaults
  language: Latin
  version: 1960
  rubrics: true

christmas:
  <<: *defaults      # Merge defaults
  name: Christmas    # Add specific fields
  rank: Duplex I classis

result_is:
  language: Latin
  version: 1960
  rubrics: true
  name: Christmas
  rank: Duplex I classis
```

---

## Multiple Documents in One File

**Separate documents** with `---`:
```yaml
---
# Document 1: Metadata
title: Precedence Rules
version: 1960

---
# Document 2: Actual rules
rules:
  - id: rule1
    description: First rule

  - id: rule2
    description: Second rule

---
# Document 3: Examples
examples:
  - case: advent_sunday
    result: displaces
```

**Use case**: Organizing related data

---

## Comments

```yaml
# Single-line comment

feasts:  # Inline comment
  - Christmas  # Born of Mary
  - Easter     # Resurrection
  - Pentecost  # Holy Spirit

# Multi-line comment block
# This can explain complex rules
# in as many lines as needed
rule:
  id: advent_precedence
```

**Power**: Explain liturgical reasoning alongside data

---

# Part 5: YAML vs JSON

---

## Side-by-Side Comparison

**JSON**:
```json
{
  "feast": {
    "name": "Christmas",
    "rank": "Duplex I classis",
    "date": "12-25",
    "commemorations": ["St. Anastasia"]
  }
}
```

**YAML**:
```yaml
feast:
  name: Christmas
  rank: Duplex I classis
  date: 12-25
  commemorations:
    - St. Anastasia
```

**Difference**: ~30% less characters, more readable

---

## YAML vs JSON: Features

| Feature | JSON | YAML |
|---------|------|------|
| **Comments** | ❌ No | ✅ Yes (`#`) |
| **Quotes required** | ✅ Always | ❌ Optional |
| **Multi-line strings** | ❌ Escape only | ✅ `\|` and `>` |
| **Trailing commas** | ❌ Error | ✅ Allowed |
| **Anchors/Aliases** | ❌ No | ✅ Yes |
| **Human readable** | ⚠️ OK | ✅ Excellent |
| **Machine speed** | ✅ Faster | ⚠️ Slower |
| **Strict syntax** | ✅ Yes | ⚠️ Flexible |

---

## When to Use YAML vs JSON

**Use YAML when**:
✅ Humans need to read/edit frequently
✅ Comments are important
✅ Configuration files
✅ Documentation with data
✅ Git-tracked files (clean diffs)

**Use JSON when**:
✅ APIs (web services)
✅ Maximum parsing speed
✅ JavaScript integration
✅ Strict validation needed
✅ No human editing

---

## YAML is a Superset of JSON

**Any valid JSON is valid YAML**:
```yaml
# This is valid YAML (it's JSON!)
{
  "name": "John",
  "age": 42,
  "hobbies": ["reading", "music"]
}
```

**Can mix styles**:
```yaml
person:
  name: John
  age: 42
  hobbies: ["reading", "music"]  # Flow style for list
```

---

# Part 6: Why YAML for Precedence Rules?

---

## Current Perl Code Problem

```perl
if ($srank[2] > $trank[2]) {
    $sanctoraloffice = 1;
} elsif ($trank[0] =~ /Dominica/i && $dayname[0] !~ /Nat1/i) {
    if ($version =~ /196/) {
        if ($trank[2] <= 5 &&
             ($srank[2] >= 5 && $saint{Rule} =~ /Festum Domini/i))) {
            $sanctoraloffice = 1;
        }
    }
}
```

**Problems**:
- Rules hidden in code
- Non-programmers can't verify
- Hard to modify
- No documentation alongside rules

---

## YAML Solution: Readable Rules

```yaml
# Precedence rule for Advent Sundays
- id: advent_sunday_precedence
  description: |
    Advent Sundays (I classis) displace all feasts
    except Duplex I classis of the Lord.
    Reference: Codex Rubricarum §102

  version: "1960"

  conditions:
    rank: Dominica I classis
    season: Advent
    opponent_not:
      rank: Duplex I classis
      type: festum_domini

  action: displace
  priority: 1.5
```

---

## Benefit 1: Human Readability

**Liturgists can verify** without programming:
```yaml
transfer_rules:
  # Epiphany transfer rule for 1570-1955
  - feast: Epiphany
    versions: ["1570", "1955"]

    condition: not_on_sunday

    transfer_to: first_sunday_after_jan_6

    explanation: |
      Before Divino afflatu (1911), Epiphany was
      transferred if it fell on a weekday.
```

**Anyone** familiar with liturgy can read this!

---

## Benefit 2: Inline Documentation

```yaml
ranks:
  duplex_i_classis:
    name: "Duplex I classis"
    priority: 1.0
    latin: "Duplex primae classis"

    # Historical note
    notes: |
      Highest rank in pre-1960 rubrics.
      Reserved for greatest solemnities:
      - Christmas, Easter, Pentecost
      - Epiphany, Ascension
      - Major Marian feasts

    # Rubrical references
    references:
      - "Divino afflatu (1911)"
      - "Codex Rubricarum (1960) §93"
```

---

## Benefit 3: Version Inheritance

```yaml
# Base rules (1570)
---
version: "1570"
ranks:
  duplex_i: &duplex1
    priority: 1.0

---
# 1960 extends 1570
version: "1960"
inherits_from: "1570"

# Add 1960-specific rules
ranks:
  dominica_i:
    priority: 1.5  # New in 1960

# Can still reference 1570 definitions
default_rank: *duplex1
```

---

## Benefit 4: Git-Friendly Changes

**Clean diffs** when rules change:
```diff
 precedence_rules:
   - id: advent_sunday
     rank: Dominica I classis
-    priority: 2.0
+    priority: 1.5
     action: displace
+    # Added reference
+    reference: "Codex Rubricarum §102"
```

**Easy to review** what changed and why

---

## Benefit 5: Multilingual Support

```yaml
feasts:
  christmas:
    id: nat01

    names:
      latin: "In Nativitate Domini"
      english: "The Nativity of Our Lord"
      deutsch: "Weihnachten"
      italiano: "Natale del Signore"
      francais: "Noël"

    rank: Duplex I classis
    date:
      month: 12
      day: 25
```

---

# Part 7: Real Examples from Our Project

---

## Example 1: Rank Definitions

```yaml
# ranks/1960-ranks.yaml
version: "1960"
description: "Rank system per Codex Rubricarum (1960)"

ranks:
  duplex_i_classis:
    name: "Duplex I classis"
    name_latin: "Duplex primae classis"
    priority: 1.0
    color_code: red
    always_displaces:
      - duplex_ii_classis
      - duplex_majus
      - semiduplex
      - simplex

  dominica_i_classis:
    name: "Dominica I classis"
    name_latin: "Dominica primae classis"
    priority: 1.5
    applies_to: [Advent, Lent, Easter_season]
```

---

## Example 2: Precedence Rule

```yaml
# rules/1960-precedence.yaml
precedence_rules:

  - id: P001
    name: "Basic rank precedence"
    enabled: true

    description: |
      Higher priority ranks (lower numbers) always
      displace lower priority ranks.

    logic:
      if: priority_a < priority_b
      then: office_a_displaces_office_b

    exceptions: []

    test_cases:
      - case: "Duplex I vs Duplex II"
        a_rank: duplex_i_classis
        b_rank: duplex_ii_classis
        expected: a_displaces
```

---

## Example 3: Transfer Rules

```yaml
# rules/1960-transfers.yaml
transfer_rules:

  - feast_id: epiphany
    feast_name: "Epiphany"

    rule_version_1960:
      condition: never
      action: no_transfer
      reason: "Divino afflatu (1911) fixed to Jan 6"

    rule_version_1570:
      condition:
        type: falls_on
        days: [monday, tuesday, wednesday,
               thursday, friday, saturday]
      action: transfer
      transfer_to:
        type: following_sunday
        limit: within_octave
      reason: "Pre-1911 Epiphany could be transferred"
```

---

## Example 4: Commemorations

```yaml
# rules/1960-commemorations.yaml
commemoration_rules:

  - context: vespers

    primary_office:
      rank: duplex_i_classis

    can_commemorate:
      - rank: duplex_ii_classis
        parts: [antiphon, versicle, oration]
        position: after_primary_oration

      - rank: dominica
        parts: [antiphon, oration]
        position: privileged  # Before other commemorations

    max_commemorations: 3

    note: |
      Per Rubricae Generales, Vespers may have
      up to 3 commemorations of displaced offices.
```

---

## Example 5: Special Cases

```yaml
# rules/1960-special-cases.yaml
special_rules:

  # Christmas to Epiphany period
  - period: christmas_to_epiphany
    dates:
      from: 12-25
      to: 01-06

    modifications:
      # Sundays in this period are special
      - type: sunday
        rank_override: duplex_ii_classis
        reason: "Sundays in Christmas Octave"

      # Ferias take texts from Christmas

      - type: feria
        office_source: christmas
        parts: [antiphons, psalms]

    references:
      - "Divino afflatu §8"
      - "Rubricae Generales, Tit. II"
```

---

## Example 6: Complete Rule with Tests

```yaml
- id: advent_sunday_special
  name: "Advent Sunday precedence (1960)"
  version: "1960"

  # Rule definition
  rule:
    subject:
      rank: dominica_i_classis
      season: advent

    opponent:
      rank: any
      except:
        rank: duplex_i_classis
        type: festum_domini

    resolution: subject_displaces

  # Inline documentation
  explanation: |
    Advent Sundays are Dominica I classis and
    displace all feasts except Duplex I classis
    of the Lord (e.g., Immaculate Conception).

  references:
    - source: "Codex Rubricarum"
      section: "§102"

  # Test cases
  test_cases:
    - name: "Advent II vs St. Nicholas"
      date: 1960-12-04  # Advent II Sunday
      subject:
        rank: dominica_i_classis
        name: "Dominica II Adventus"
      opponent:
        rank: duplex_majus
        name: "St. Nicholas"
      expected: subject_displaces

    - name: "Advent II vs Immaculate Conception"
      date: 1960-12-08  # If falls on Advent Sunday
      subject:
        rank: dominica_i_classis
      opponent:
        rank: duplex_i_classis
        type: festum_domini
      expected: opponent_displaces
```

---

# Part 8: Tools and Best Practices

---

## YAML Tools

**Editors with YAML support**:
- **VS Code**: Built-in syntax highlighting + extensions
- **IntelliJ IDEA**: YAML plugin
- **Sublime Text**: YAML syntax package
- **Vim/Neovim**: YAML plugins

**Online tools**:
- **YAML Lint**: http://www.yamllint.com/
- **JSON ↔ YAML converter**: https://www.json2yaml.com/
- **YAML validator**: https://codebeautify.org/yaml-validator

---

## VS Code YAML Extension

**Recommended extension**: "YAML" by Red Hat

**Features**:
- Syntax validation
- Auto-completion
- Schema validation (JSON Schema)
- Hover documentation
- Error highlighting

**Install**:
```bash
code --install-extension redhat.vscode-yaml
```

---

## Python YAML Libraries

**PyYAML** (most common):
```python
import yaml

# Read YAML
with open('rules.yaml') as f:
    data = yaml.safe_load(f)

# Write YAML
with open('output.yaml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False)
```

**ruamel.yaml** (preserves comments):
```python
from ruamel.yaml import YAML

yaml = YAML()
with open('rules.yaml') as f:
    data = yaml.load(f)
```

---

## YAML Best Practices

**1. Use consistent indentation** (2 or 4 spaces):
```yaml
# Good - 2 spaces
feasts:
  - name: Christmas
    rank: Duplex I

# Bad - mixed indentation
feasts:
    - name: Christmas
      rank: Duplex I
```

**2. Prefer block style over flow style**:
```yaml
# Good (readable)
ranks:
  - Duplex I
  - Duplex II

# Avoid (compact but less clear)
ranks: [Duplex I, Duplex II]
```

---

## More Best Practices

**3. Use comments liberally**:
```yaml
# Rule for Advent Sundays
# Reference: Codex Rubricarum §102
advent_rule:
  rank: dominica_i_classis
```

**4. Quote strings when ambiguous**:
```yaml
# Good
version: "1960"  # Could be interpreted as number

# Bad
version: 1960  # Parsed as integer
```

**5. Use meaningful key names**:
```yaml
# Good
feast_rank: Duplex I classis

# Bad
r: Duplex I classis
```

---

## YAML Gotchas to Avoid

**1. Indentation is critical**:
```yaml
# Wrong - misaligned
feasts:
 - Christmas
  - Easter  # Error!

# Right
feasts:
  - Christmas
  - Easter
```

**2. Tabs vs Spaces**:
```yaml
# NEVER use tabs - use spaces only!
# Tabs will cause parsing errors
```

---

## More Gotchas

**3. Norway problem**:
```yaml
# Bad - "no" is interpreted as false!
country: no  # Becomes: country: false

# Good - quote it
country: "no"  # Stays as string "no"
```

**4. Colons in strings**:
```yaml
# Bad - colon confuses parser
title: Office: Vespers  # Error!

# Good - quote it
title: "Office: Vespers"
```

---

## YAML Schema Validation

**JSON Schema** can validate YAML:

```yaml
# schema.yaml
type: object
properties:
  version:
    type: string
    pattern: "^[0-9]{4}$"
  ranks:
    type: array
    items:
      type: object
      required: [name, priority]
```

**Validation** in Python:
```python
import yaml
from jsonschema import validate

with open('schema.yaml') as f:
    schema = yaml.safe_load(f)

with open('rules.yaml') as f:
    data = yaml.safe_load(f)

validate(instance=data, schema=schema)
```

---

## File Organization

**Recommended structure**:
```
rules/
  ├── metadata.yaml           # Overall metadata
  ├── ranks/
  │   ├── 1570-ranks.yaml
  │   ├── 1960-ranks.yaml
  │   └── cistercian-ranks.yaml
  ├── precedence/
  │   ├── 1570-precedence.yaml
  │   └── 1960-precedence.yaml
  ├── transfers/
  │   ├── 1570-transfers.yaml
  │   └── 1960-transfers.yaml
  └── commemorations/
      ├── 1570-commemorations.yaml
      └── 1960-commemorations.yaml
```

**Benefit**: Modular, easy to navigate

---

## Version Control Best Practices

**1. One logical rule per commit**:
```bash
git commit -m "Add Advent Sunday precedence rule for 1960"
```

**2. Use meaningful commit messages**:
```bash
# Good
git commit -m "Fix Epiphany transfer rule for 1570 version"

# Bad
git commit -m "Update rules.yaml"
```

**3. Review diffs before committing**:
```bash
git diff rules/1960-precedence.yaml
```

---

## Documentation in YAML

**Use YAML to document itself**:
```yaml
# metadata.yaml
project: Divinum Officium Precedence Rules
version: 2.0
format: YAML

documentation:
  description: |
    This directory contains precedence rules for
    various liturgical versions in YAML format.

  how_to_read: |
    Each rule file is organized by version.
    Rules use anchors (&) and aliases (*) to
    avoid repetition.

  conventions:
    indentation: 2 spaces
    string_quoting: "only when necessary"
    comments: "required for complex rules"
```

---

# Summary

---

## YAML Key Takeaways

**Syntax**:
✅ Key-value pairs with `: `
✅ Lists with `- `
✅ Indentation matters (spaces only!)
✅ Comments with `#`
✅ Quotes optional for simple strings

**Advanced Features**:
✅ Anchors (`&`) and aliases (`*`) for reuse
✅ Multi-line strings with `|` and `>`
✅ Type casting with `!!`
✅ Multi-document files with `---`

---

## YAML for Precedence Rules

**Why YAML is ideal**:
1. **Human-readable** - liturgists can verify
2. **Commentable** - document rubrical reasoning
3. **Structured** - enforce consistency
4. **Git-friendly** - track changes clearly
5. **Flexible** - handle complex inheritance
6. **Well-supported** - excellent Python libraries

**Trade-off**: Slightly slower parsing than JSON (but negligible for our use case)

---

## Comparison Summary

| Format | Readable | Comments | Flexible | Speed | Best For |
|--------|----------|----------|----------|-------|----------|
| **YAML** | ✅ Excellent | ✅ Yes | ✅ Very | ⚠️ OK | Config files |
| **JSON** | ⚠️ OK | ❌ No | ⚠️ OK | ✅ Fast | APIs |
| **XML** | ❌ Poor | ✅ Yes | ✅ Very | ⚠️ OK | Complex docs |
| **Perl** | ❌ Poor | ⚠️ Yes | ✅ Very | ✅ Fast | Scripts |

**Winner for rules**: YAML

---

## Next Steps

**For Divinum Officium project**:

1. ✅ **You now understand YAML**
2. 📝 **Next**: Review YAML-based precedence proposal
3. 🔧 **Then**: Prototype rule engine
4. ✅ **Finally**: Migrate Perl rules to YAML

**Resources**:
- YAML official site: https://yaml.org/
- YAML 1.2 spec: https://yaml.org/spec/1.2/spec.html
- Learn YAML in Y minutes: https://learnxinyminutes.com/docs/yaml/

---

## Questions to Consider

**Before adopting YAML, ask**:

1. Will non-programmers need to edit rules?
   - **If yes**: YAML is better than JSON

2. Do we need inline documentation?
   - **If yes**: YAML is essential

3. Is Git history important?
   - **If yes**: YAML gives cleaner diffs

4. Do we need maximum parsing speed?
   - **If no**: YAML is fine (speed difference negligible)

5. Will rules be complex with inheritance?
   - **If yes**: YAML anchors are powerful

---

## Thank You!

**Questions?**

**Resources**:
- This presentation: `yaml-introduction.html`
- YAML official: https://yaml.org/
- PyYAML docs: https://pyyaml.org/

**Next Steps**:
- Review YAML-based precedence proposal
- Experiment with YAML files
- Provide feedback on approach

---

# Appendix: Quick Reference

---

## YAML Cheat Sheet - Basics

```yaml
# Comments start with #

# Key-value pairs
key: value
number: 42
float: 3.14
boolean: true
null_value: null

# Strings
simple: Hello World
quoted: "Hello: World"
single: 'Single quotes'

# Multi-line
literal: |
  Preserves
  newlines
folded: >
  Folds into
  single line
```

---

## YAML Cheat Sheet - Collections

```yaml
# Lists (block style)
list:
  - item1
  - item2
  - item3

# Lists (flow style)
list: [item1, item2, item3]

# Dictionaries
dict:
  key1: value1
  key2: value2

# Nested
nested:
  level1:
    level2:
      - item1
      - item2
```

---

## YAML Cheat Sheet - Advanced

```yaml
# Anchors and aliases
base: &base
  name: Default
  value: 42

derived1: *base  # Copy entire base
derived2:
  <<: *base      # Merge base
  extra: field   # Add more

# Type casting
string: !!str 1960
integer: !!int "42"

# Multiple documents
---
document: 1
---
document: 2
```

---

## Common Patterns for Rules

```yaml
# Rule template
- id: unique_id
  name: "Human readable name"
  description: |
    Multi-line explanation

  version: "1960"

  conditions:
    field1: value1
    field2: value2

  actions:
    primary: action_name

  references:
    - "Source citation"

  test_cases:
    - input: test_input
      expected: test_output
```

---

## End of Presentation

**YAML**: Simple, powerful, human-friendly

**Perfect for**: Precedence rules in Divinum Officium

**Next**: Apply this knowledge to our project!
