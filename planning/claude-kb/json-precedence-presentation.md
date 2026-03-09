---
title: JSON-Based Precedence Rules
subtitle: A Modern Approach for Divinum Officium
author: Divinum Officium Project
date: December 28, 2025
theme: serif
---

# JSON-Based Precedence Rules

**A Modern Approach for Divinum Officium**

Flexible, Git-Friendly, Human-Readable

---

## Agenda

1. The Precedence Challenge
2. Why JSON?
3. Proposed JSON Architecture
4. Data Model Deep Dive
5. Rule Engine Design
6. Migration from Perl
7. Benefits & Trade-offs
8. Implementation Roadmap

---

# Part 1: The Precedence Challenge

---

## What is Liturgical Precedence?

**The Problem**: What office should be celebrated on a given day?

**Complexity**:
- Temporal cycle (Sundays, seasons)
- Sanctoral cycle (Saints' feasts)
- Different ranks (Duplex I, Duplex II, Semiduplex, etc.)
- Multiple rubrics (1570, 1960, Cistercian, Dominican)
- Transfers based on Easter date
- Commemorations
- Vespers (1st vs 2nd)

**Result**: Intricate precedence calculations

---

## Current Implementation Issues

### Perl Code Complexity

```perl
if ($srank[2] > $trank[2]) {
    $sanctoraloffice = 1;
} elsif ($trank[0] =~ /Dominica/i && $dayname[0] !~ /Nat1/i) {
    if ($version =~ /196/) {
        if ($trank[2] <= 5 &&
            ($srank[2] >= 6 ||
             ($srank[2] >= 5 && $saint{Rule} =~ /Festum Domini/i))) {
            $sanctoraloffice = 1;
        }
    }
}
```

**Problems**:
- Logic scattered across 2000+ lines
- Version rules embedded in code
- Hard to understand
- Difficult to modify
- No clear separation of rules and logic

---

## Current Challenges

❌ **Maintainability**
- Complex if/else chains
- Version-specific code branches
- Hard to add new rubrics

❌ **Transparency**
- Rules hidden in Perl code
- Non-programmers can't understand
- Difficult to verify correctness

❌ **Testing**
- Hard to test individual rules
- Edge cases buried in code
- No clear rule inventory

❌ **Documentation**
- Rules not self-documenting
- Require code comments
- Expert knowledge needed

---

# Part 2: Why JSON?

---

## JSON Advantages

### 1. **Human-Readable**

```json
{
  "rule": "Duplex I beats Duplex II Sunday",
  "conditions": {
    "sanctoral_rank": {"min": 6.0},
    "temporal_rank": {"max": 5.0},
    "temporal_is_sunday": true
  },
  "result": {
    "winner": "sanctoral"
  }
}
```

**Anyone can read and understand this!**

---

## JSON Advantages (continued)

### 2. **Git-Friendly**

✅ Clear diffs show rule changes
✅ Easy code review
✅ Branching for experimental rules
✅ Version history of rule changes

```diff
  "conditions": {
-   "sanctoral_rank": {"min": 5.0},
+   "sanctoral_rank": {"min": 6.0},
    "temporal_is_sunday": true
  }
```

**See exactly what changed**

---

## JSON Advantages (continued)

### 3. **No Database Server**

✅ Just files in a directory
✅ No PostgreSQL to install/maintain
✅ No connection pooling
✅ No migrations
✅ Simple deployment

```
data/
  versions/
    rubrics-1960.json
    tridentine-1570.json
  calendars/
    ...
  transfers/
    ...
```

**Copy folder = deploy database**

---

## JSON Advantages (continued)

### 4. **Language-Agnostic**

```python
# Python
import json
rules = json.load(open('rules.json'))
```

```javascript
// JavaScript
const rules = require('./rules.json');
```

```ruby
# Ruby
rules = JSON.parse(File.read('rules.json'))
```

**Works with any language**

---

## JSON Advantages (continued)

### 5. **Easy Editing**

- **Any text editor** works
- **VS Code** has JSON schema validation
- **Online editors** available
- **No special tools** required

**Lower barrier for contributors**

---

## When SQL Would Be Better

SQL databases excel at:

❌ Complex ad-hoc queries across versions
❌ High-frequency writes
❌ Concurrent modifications
❌ Referential integrity enforcement
❌ Large-scale analytics

**Reality**: Divinum Officium doesn't need these!

✅ Queries are predictable
✅ Writes are infrequent (content updates)
✅ Few concurrent editors
✅ Integrity validated on load
✅ Limited analytics needs

---

# Part 3: Proposed JSON Architecture

---

## Overall Architecture

```
data/
├── offices/                    # Office content (TEI XML)
│   ├── temporal/
│   ├── sanctoral/
│   └── commune/
│
├── versions/                   # Version rules (JSON)
│   ├── tridentine-1570.json
│   ├── rubrics-1960.json
│   └── cistercian.json
│
├── calendars/                  # Calendars (JSON)
│   └── rubrics-1960/
│       ├── sanctoral.json
│       └── temporal.json
│
├── transfers/                  # Transfer rules (JSON)
│   └── rubrics-1960/
│       ├── easter-a.json
│       └── permanent.json
│
└── metadata/                   # Shared data (JSON)
    └── ranks.json

cache/                          # SQLite cache (generated)
    └── offices.db
```

---

## Three-Layer Approach

### Layer 1: JSON Files (Source of Truth)
- Version definitions
- Rank metadata
- Calendars
- Transfer rules
- Precedence rules

### Layer 2: Python Engine
- Load JSON data
- Apply rules
- Resolve precedence
- Cache results

### Layer 3: SQLite Cache (Optional)
- Store computed results
- Enable fast queries
- Regenerate anytime from JSON

**Best of both worlds!**

---

# Part 4: Data Model Deep Dive

---

## Office Metadata (JSON Sidecar)

```json
{
  "office_key": "12-25",
  "office_type": "sanctoral",
  "names": {
    "latin": "In Nativitate Domini",
    "english": "The Nativity of Our Lord"
  },
  "ranks": {
    "tridentine-1570": {
      "rank_numeric": 7.0,
      "rank_name": "Duplex I classis cum Octava privilegiata",
      "properties": {
        "has_first_vespers": true,
        "has_second_vespers": true,
        "lectiones_count": 9,
        "is_feast_of_lord": true,
        "octave_type": "privileged"
      }
    },
    "rubrics-1960": {
      "rank_numeric": 6.0,
      "rank_name": "Duplex I classis",
      "properties": {
        "has_first_vespers": true,
        "lectiones_count": 9,
        "is_feast_of_lord": true
      }
    }
  },
  "tei_file": "12-25.xml"
}
```

---

## Version Definition

```json
{
  "version": {
    "code": "rubrics-1960",
    "name": "Rubrics of 1960",
    "year": 1960,
    "parent_version": "rubrics-1955"
  },

  "parameters": {
    "vespers": {
      "min_rank_first_vespers": 6.0
    },
    "commemorations": {
      "strategy": "strict_1960",
      "max_per_hour": 1
    },
    "octaves": {
      "suppress_common_octaves": true,
      "privileged_octaves_only": true
    }
  },

  "concurrence_rules": [ ... ],
  "commemoration_rules": [ ... ],
  "vespers_rules": [ ... ]
}
```

**Inheritance**: Loads parent, merges child overrides

---

## Concurrence Rules

```json
{
  "concurrence_rules": [
    {
      "priority": 1,
      "name": "Duplex I feast of Lord beats Duplex II Sunday",
      "conditions": {
        "office1": {
          "type": "sanctoral",
          "rank": {"min": 6.0},
          "properties": {"is_feast_of_lord": true}
        },
        "office2": {
          "type": "temporal",
          "rank": {"max": 5.0},
          "properties": {"is_sunday": true}
        }
      },
      "result": {
        "winner": "office1",
        "commemorate_loser": false
      }
    },

    {
      "priority": 100,
      "name": "Default: higher rank wins",
      "conditions": {},
      "result": {
        "winner": "higher_rank",
        "commemorate_loser": true
      }
    }
  ]
}
```

---

## Commemoration Rules

```json
{
  "commemoration_rules": [
    {
      "canonical_hours": ["matins", "lauds", "prime", "terce", "sext", "none"],
      "conditions": {
        "winner": {
          "properties": {"is_sunday": true},
          "rank": {"max": 5.99}
        },
        "candidate": {
          "type": "sanctoral",
          "rank": {"min": 5.0, "max": 5.99}
        }
      },
      "result": {
        "commemorated": true,
        "type": "full"
      }
    },

    {
      "canonical_hours": ["lauds"],
      "conditions": {
        "winner": {"properties": {"is_sunday": true}},
        "candidate": {"rank": {"min": 5.0, "max": 5.99}}
      },
      "result": {
        "commemorated": true,
        "type": "laudes_only"
      }
    }
  ]
}
```

---

## Vespers Rules

```json
{
  "vespers_rules": [
    {
      "priority": 1,
      "name": "No first Vespers below Duplex I",
      "conditions": {
        "tomorrow": {
          "rank": {"max": 5.99}
        }
      },
      "result": {
        "suppress_first_vespers": true
      }
    },

    {
      "priority": 2,
      "name": "Exception: Feast of Lord on Sunday",
      "conditions": {
        "tomorrow": {
          "rank": {"min": 5.0, "max": 5.99},
          "properties": {"is_feast_of_lord": true},
          "day_of_week": 0
        }
      },
      "result": {
        "suppress_first_vespers": false
      }
    }
  ]
}
```

---

## Calendar Files

### Sanctoral Calendar

```json
{
  "version": "rubrics-1960",
  "calendar_type": "sanctoral",
  "entries": {
    "01-01": [
      {
        "office_key": "01-01",
        "priority": 1,
        "note": "Octave of Christmas"
      }
    ],
    "12-25": [
      {
        "office_key": "12-25",
        "priority": 1,
        "note": "Nativity of Our Lord"
      }
    ]
  }
}
```

---

## Calendar Files (continued)

### Temporal Calendar

```json
{
  "version": "rubrics-1960",
  "calendar_type": "temporal",
  "entries": [
    {
      "office_key": "Pasc0-0",
      "offset_from_easter": 0,
      "name": "Dominica Resurrectionis",
      "season": "easter"
    },
    {
      "office_key": "Pent0-0",
      "offset_from_easter": 49,
      "name": "Dominica Pentecostes",
      "season": "pentecost"
    },
    {
      "office_key": "Quad1-0",
      "offset_from_easter": -42,
      "name": "Dominica I in Quadragesima",
      "season": "lent"
    }
  ]
}
```

---

## Transfer Rules

```json
{
  "version": "rubrics-1960",
  "trigger": {
    "type": "easter_date",
    "easter_month": 3,
    "easter_day": 22,
    "description": "Earliest possible Easter"
  },
  "transfers": [
    {
      "from": {
        "date": "03-19",
        "office_key": "03-19",
        "name": "St. Joseph"
      },
      "to": {
        "date": "04-19",
        "reason": "Falls in Holy Week, transferred after Easter Octave"
      }
    },
    {
      "from": {
        "date": "03-25",
        "office_key": "03-25",
        "name": "Annunciation"
      },
      "to": {
        "date": "04-08",
        "reason": "Falls in Holy Week"
      }
    }
  ]
}
```

---

## Shared Rank Definitions

```json
{
  "rank_classes": {
    "duplex_i": {
      "numeric_range": [6.0, 6.99],
      "name_latin": "Duplex I classis",
      "name_english": "Double of the First Class",
      "properties": {
        "has_first_vespers": true,
        "has_second_vespers": true,
        "default_lectiones": 9
      }
    },
    "duplex_ii": {
      "numeric_range": [5.0, 5.99],
      "name_latin": "Duplex II classis",
      "name_english": "Double of the Second Class",
      "properties": {
        "has_first_vespers": false,
        "has_second_vespers": true,
        "default_lectiones": 9,
        "first_vespers_exceptions": [
          "is_feast_of_lord && day_of_week == 0"
        ]
      }
    }
  }
}
```

---

# Part 5: Rule Engine Design

---

## Python Rule Engine Architecture

```python
class PrecedenceEngine:
    def __init__(self, version_code, target_date):
        self.version_code = version_code
        self.target_date = target_date
        self.loader = DataLoader()
        self.version_data = self.loader.load_version(version_code)
        self.rule_engine = RuleEngine(self.version_data)

    def get_office(self, canonical_hour):
        """Get office for a specific hour"""
        if canonical_hour in ['vespers', 'completorium']:
            return self._resolve_vespers()
        return self._resolve_standard_hour(canonical_hour)

    def _resolve_standard_hour(self, hour):
        temporal = self._get_temporal_office()
        sanctorals = self._get_sanctoral_offices()

        # Apply transfers
        temporal = self._apply_transfer(temporal)
        sanctorals = [self._apply_transfer(s) for s in sanctorals]

        # Resolve concurrence
        winner = self.rule_engine.resolve_concurrence(
            temporal, sanctorals, self._build_context(hour)
        )

        return winner
```

---

## Data Loader

```python
class DataLoader:
    def __init__(self, data_root):
        self.data_root = data_root
        self._cache = {}

    def load_version(self, version_code):
        """Load version with parent inheritance"""
        version_path = self.data_root / "versions" / f"{version_code}.json"

        with open(version_path) as f:
            version_data = json.load(f)

        # Load parent if exists
        parent_code = version_data.get("version", {}).get("parent_version")
        if parent_code:
            parent_data = self.load_version(parent_code)
            version_data = self._merge_versions(parent_data, version_data)

        return version_data

    def _merge_versions(self, parent, child):
        """Deep merge: child overrides parent"""
        result = parent.copy()
        for key, value in child.items():
            if key in result and isinstance(result[key], dict):
                result[key] = self._merge_versions(result[key], value)
            else:
                result[key] = value
        return result
```

---

## Rule Evaluation

```python
class RuleEngine:
    def __init__(self, version_data):
        self.concurrence_rules = version_data.get("concurrence_rules", [])
        self.commemoration_rules = version_data.get("commemoration_rules", [])
        self.vespers_rules = version_data.get("vespers_rules", [])

    def resolve_concurrence(self, temporal, sanctorals, context):
        """Apply concurrence rules to determine winner"""
        if not sanctorals:
            return temporal
        if not temporal:
            return max(sanctorals, key=lambda o: o.rank.numeric)

        best_sanctoral = max(sanctorals, key=lambda o: o.rank.numeric)

        # Apply rules in priority order
        for rule in sorted(self.concurrence_rules,
                          key=lambda r: r.get("priority", 999)):
            if self._matches_rule(rule, temporal, best_sanctoral, context):
                winner_choice = rule["result"]["winner"]

                if winner_choice == "office1":
                    return best_sanctoral
                elif winner_choice == "office2":
                    return temporal
                elif winner_choice == "higher_rank":
                    return (best_sanctoral if best_sanctoral.rank.numeric >
                            temporal.rank.numeric else temporal)

        # Default
        return (best_sanctoral if best_sanctoral.rank.numeric >
                temporal.rank.numeric else temporal)
```

---

## Condition Matching

```python
def _matches_rule(self, rule, office1, office2, context):
    """Check if rule conditions match"""
    conditions = rule.get("conditions", {})

    if not conditions:
        return True  # Default rule

    # Check office1 conditions
    if "office1" in conditions:
        if not self._matches_office_conditions(
            office1, conditions["office1"], context
        ):
            return False

    # Check office2 conditions
    if "office2" in conditions:
        if not self._matches_office_conditions(
            office2, conditions["office2"], context
        ):
            return False

    return True

def _matches_office_conditions(self, office, conditions, context):
    """Check if office matches specific conditions"""
    # Type check
    if "type" in conditions and office.type != conditions["type"]:
        return False

    # Rank range
    if "rank" in conditions:
        rank_cond = conditions["rank"]
        if "min" in rank_cond and office.rank.numeric < rank_cond["min"]:
            return False
        if "max" in rank_cond and office.rank.numeric > rank_cond["max"]:
            return False

    # Properties
    if "properties" in conditions:
        for prop, expected in conditions["properties"].items():
            if getattr(office.rank, prop, None) != expected:
                return False

    return True
```

---

## Transfer Resolution

```python
class TransferResolver:
    def __init__(self, version_code, year, easter_date):
        self.version_code = version_code
        self.year = year
        self.easter_date = easter_date
        self.easter_letter = self._calculate_easter_letter()
        self.transfers = self._load_transfers()

    def get_transfer(self, office_key, office_type, target_date):
        """Check if office is transferred from this date"""
        date_key = f"{target_date.month:02d}-{target_date.day:02d}"

        for transfer in self.transfers:
            if transfer.get("from", {}).get("date") == date_key:
                if transfer.get("from", {}).get("office_key") == office_key:
                    return transfer.get("to", {}).get("date")

        return None

    def _load_transfers(self):
        """Load applicable transfers for this Easter"""
        transfer_dir = Path(f"data/transfers/{self.version_code}")
        transfers = []

        # Permanent transfers
        perm_file = transfer_dir / "permanent.json"
        if perm_file.exists():
            with open(perm_file) as f:
                transfers.extend(json.load(f).get("transfers", []))

        # Easter letter specific
        letter_file = transfer_dir / f"easter-{self.easter_letter}.json"
        if letter_file.exists():
            with open(letter_file) as f:
                transfers.extend(json.load(f).get("transfers", []))

        return transfers
```

---

## Caching with SQLite

```python
class CacheManager:
    def __init__(self, cache_db_path):
        self.db = sqlite3.connect(cache_db_path)
        self._init_schema()

    def _init_schema(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS computed_offices (
                version_code TEXT,
                date TEXT,
                canonical_hour TEXT,
                winner_office_key TEXT,
                winner_office_type TEXT,
                commemorations TEXT,
                computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (version_code, date, canonical_hour)
            )
        """)

    def get_cached(self, version, date, hour):
        """Try to get from cache"""
        cursor = self.db.execute("""
            SELECT winner_office_key, winner_office_type, commemorations
            FROM computed_offices
            WHERE version_code = ? AND date = ? AND canonical_hour = ?
        """, (version, date.isoformat(), hour))

        row = cursor.fetchone()
        if row:
            return {
                "winner": {"key": row[0], "type": row[1]},
                "commemorations": json.loads(row[2])
            }
        return None

    def set_cached(self, version, date, hour, result):
        """Store in cache"""
        self.db.execute("""
            INSERT OR REPLACE INTO computed_offices
            (version_code, date, canonical_hour, winner_office_key,
             winner_office_type, commemorations)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            version, date.isoformat(), hour,
            result["winner"]["key"], result["winner"]["type"],
            json.dumps(result["commemorations"])
        ))
        self.db.commit()
```

---

# Part 6: Migration from Perl

---

## Migration Strategy

### Phase 1: Extract Rules from Perl

**Task**: Analyze current Perl code and extract rules

```perl
# Current Perl
if ($srank[2] >= 6 && $trank[2] <= 5 && $trank[0] =~ /Dominica/i) {
    $sanctoraloffice = 1;
}
```

**Becomes**:

```json
{
  "rule": "Duplex I beats Duplex II Sunday",
  "conditions": {
    "sanctoral_rank": {"min": 6.0},
    "temporal_rank": {"max": 5.0},
    "temporal_is_sunday": true
  },
  "result": {"winner": "sanctoral"}
}
```

---

## Migration Strategy (continued)

### Phase 2: Build Python Engine

**Tasks**:
1. Implement data loader
2. Build rule engine
3. Write transfer resolver
4. Create caching layer

**Timeline**: 2-3 months

### Phase 3: Parallel Validation

**Tasks**:
1. Run both systems on same inputs
2. Compare outputs
3. Fix discrepancies
4. Document differences

**Timeline**: 2-3 months

---

## Validation Example

```python
def validate_precedence():
    """Compare Perl vs Python outputs"""
    test_dates = generate_test_dates(year=2025, count=365)

    discrepancies = []

    for date in test_dates:
        # Get Perl result (call existing system)
        perl_result = call_perl_system(date, "vespers", "rubrics-1960")

        # Get Python result
        engine = PrecedenceEngine("rubrics-1960", date)
        python_result = engine.get_office("vespers")

        # Compare
        if perl_result.office_key != python_result.primary.key:
            discrepancies.append({
                "date": date,
                "perl": perl_result,
                "python": python_result
            })

    if discrepancies:
        print(f"Found {len(discrepancies)} discrepancies")
        analyze_discrepancies(discrepancies)
    else:
        print("✅ Perfect match!")
```

---

## Conversion Tools

```python
def convert_perl_to_json():
    """Semi-automated Perl → JSON conversion"""

    # Parse Perl code
    perl_rules = parse_perl_file("horascommon.pl")

    # Convert to JSON structures
    json_rules = []
    for rule in perl_rules:
        json_rule = {
            "priority": rule.order,
            "name": infer_rule_name(rule),
            "conditions": extract_conditions(rule),
            "result": extract_result(rule)
        }
        json_rules.append(json_rule)

    # Write JSON
    output = {
        "version": {"code": "rubrics-1960"},
        "concurrence_rules": json_rules
    }

    with open("rubrics-1960.json", "w") as f:
        json.dump(output, f, indent=2)
```

---

# Part 7: Benefits & Trade-offs

---

## Benefits: Data Quality

### Before (Perl)

```perl
# Easy to make mistakes
if ($srank[2] > $trank[2]) {  # Typo in variable?
    $sanctoralofice = 1;  # Misspelled!
}
```

**No validation, runtime errors**

### After (JSON)

```json
{
  "conditions": {
    "sanctoral_rank": {"min": 6.0},
    "temporal_rank": {"max": 5.0}
  }
}
```

**JSON schema validates structure**

---

## Benefits: Transparency

### Current State
"What's the rule for Christmas on Sunday?"

**Answer**: Read 200 lines of Perl, trace execution

### With JSON
"What's the rule for Christmas on Sunday?"

**Answer**:
```bash
cat versions/rubrics-1960.json | grep -A10 "Duplex I"
```

Or use a simple web viewer:
```
http://localhost:8080/rules/rubrics-1960
```

**Rules are discoverable and readable**

---

## Benefits: Version Control

### Git History

```bash
$ git log --oneline versions/rubrics-1960.json

abc123 Fix: Feast of Lord on Sunday now has 1st Vespers
def456 Update: Lower commemoration rank threshold to 5.0
789ghi Add: New rule for transferred vigils
```

### Compare Versions

```bash
$ git diff tridentine-1570.json rubrics-1960.json
```

**See exactly how rubrics evolved**

---

## Benefits: Testing

### Rule-Level Tests

```python
def test_duplex_i_beats_sunday():
    """Test: Duplex I feast of Lord beats Duplex II Sunday"""

    # Setup
    sanctoral = create_office(
        key="03-25",
        rank=6.0,
        is_feast_of_lord=True
    )
    temporal = create_office(
        key="Quad4-0",
        rank=5.0,
        is_sunday=True
    )

    engine = RuleEngine(load_version("rubrics-1960"))

    # Execute
    winner = engine.resolve_concurrence(temporal, [sanctoral], {})

    # Assert
    assert winner == sanctoral
    assert winner.key == "03-25"
```

**Test each rule in isolation**

---

## Benefits: Extensibility

### Adding New Rubric

**Steps**:
1. Copy existing JSON (e.g., rubrics-1960.json)
2. Modify rules
3. Save as new-rubric-2030.json
4. Test

**No code changes needed!**

### A/B Testing Rules

```json
{
  "version": {
    "code": "experimental-vespers",
    "parent_version": "rubrics-1960"
  },
  "vespers_rules": [
    {
      "name": "Experimental: All feasts get 1st Vespers",
      "conditions": {"tomorrow": {"rank": {"min": 3.0}}},
      "result": {"suppress_first_vespers": false}
    }
  ]
}
```

**Try variations without touching production**

---

## Trade-offs: Query Limitations

### SQL Can Do

```sql
-- Find all offices that beat Sundays
SELECT o.name, r.rank_numeric
FROM offices o
JOIN ranks r ON o.id = r.office_id
WHERE r.rank_numeric > (
    SELECT rank_numeric FROM ranks
    WHERE properties->>'is_sunday' = 'true'
)
```

### JSON Cannot Do This Easily

**Workaround**: Build indices in SQLite cache

```python
# Pre-compute and cache
for office in all_offices:
    if office.rank.numeric > 5.0:
        db.insert("high_rank_offices", office)
```

**Limitation**: Ad-hoc queries harder, but rarely needed

---

## Trade-offs: Validation

### SQL Enforces

```sql
CREATE TABLE offices (
    id SERIAL PRIMARY KEY,
    rank_numeric DECIMAL(4,2) CHECK (rank_numeric BETWEEN 1.0 AND 7.0),
    office_type VARCHAR(20) CHECK (office_type IN ('temporal', 'sanctoral'))
);
```

**Database prevents invalid data**

### JSON Requires

```python
# Validation in code
schema = {
    "type": "object",
    "properties": {
        "rank_numeric": {
            "type": "number",
            "minimum": 1.0,
            "maximum": 7.0
        }
    }
}

validate(office_data, schema)
```

**Must validate on load, but works well**

---

## Trade-offs Summary

| Aspect | JSON | SQL |
|--------|------|-----|
| **Deployment** | ✅ Simple (files) | ❌ Complex (server) |
| **Version Control** | ✅ Native git | ⚠️ Needs dumps |
| **Readability** | ✅ Very readable | ⚠️ Need SQL knowledge |
| **Validation** | ⚠️ Manual | ✅ Automatic |
| **Queries** | ⚠️ Limited | ✅ Powerful |
| **Performance** | ✅ Fast (cached) | ✅ Fast (indexed) |
| **Backup** | ✅ Copy folder | ⚠️ DB dumps |

**For Divinum Officium**: JSON advantages outweigh SQL advantages

---

# Part 8: Implementation Roadmap

---

## Phase 1: Foundation (Months 1-2)

**Tasks**:
- [ ] Design JSON schemas
- [ ] Create example version files
- [ ] Build data loader (Python)
- [ ] Implement version inheritance
- [ ] Create validation tools

**Deliverables**:
- JSON schemas for all data types
- Sample rubrics-1960.json
- Python loader library
- Validation scripts

**Success**: Can load and validate JSON files

---

## Phase 2: Rule Engine (Months 3-4)

**Tasks**:
- [ ] Implement concurrence resolver
- [ ] Build commemoration engine
- [ ] Create Vespers resolver
- [ ] Add transfer handling
- [ ] Write unit tests

**Deliverables**:
- Complete Python rule engine
- 100+ unit tests
- Performance benchmarks

**Success**: Engine produces correct outputs for test cases

---

## Phase 3: Data Migration (Months 5-6)

**Tasks**:
- [ ] Extract rules from Perl
- [ ] Convert to JSON format
- [ ] Create all version files
- [ ] Populate calendar data
- [ ] Build transfer tables

**Deliverables**:
- JSON files for all rubrics (1570, 1960, etc.)
- Complete calendar data
- All transfer rules

**Success**: Complete JSON dataset

---

## Phase 4: Validation (Months 7-8)

**Tasks**:
- [ ] Parallel testing (Perl vs Python)
- [ ] Compare outputs for 365+ days
- [ ] Fix discrepancies
- [ ] Document differences
- [ ] Performance optimization

**Deliverables**:
- Validation report
- Discrepancy analysis
- Performance metrics

**Success**: 99%+ match with Perl system

---

## Phase 5: Integration (Months 9-10)

**Tasks**:
- [ ] Integrate with Flask app
- [ ] Add SQLite caching
- [ ] Build API endpoints
- [ ] Create admin UI for JSON editing
- [ ] Documentation

**Deliverables**:
- Working Flask application
- REST API
- Admin interface
- User documentation

**Success**: Production-ready system

---

## Timeline Overview

```
┌────────────────────────────────────────────────┐
│           10-Month Implementation              │
├──────┬──────┬──────┬──────┬──────┬──────┬─────┤
│  M1  │  M2  │  M3  │  M4  │  M5  │  M6  │ ... │
├──────┼──────┼──────┼──────┼──────┼──────┼─────┤
│Schema│Loader│Engine│Engine│Extract│Convert│Test│
│Design│Build │Core  │Complete│Rules│Data │ Valid│
└──────┴──────┴──────┴──────┴──────┴──────┴─────┘
       │              │             │        │
       ▼              ▼             ▼        ▼
   Foundation    Rule Engine   Migration  Deploy
```

**Total**: 10 months to production-ready JSON system

---

## Resource Requirements

### Development Team

**Minimum**:
- 1 Python developer (20 hrs/week)
- 1 QA tester (5 hrs/week)

**Recommended**:
- 1.5 Python developers (30 hrs/week)
- 0.5 Liturgical expert (10 hrs/week)
- 1 QA tester (10 hrs/week)

### Infrastructure

- Development server (optional, can use local)
- GitHub repository (existing)
- CI/CD pipeline (GitHub Actions - free)

**Cost**: $0-20/month

---

## Risk Mitigation

### Risk: Rule Extraction Errors

**Mitigation**:
- Semi-automated extraction
- Manual review of each rule
- Parallel validation
- Liturgical expert review

### Risk: Performance Issues

**Mitigation**:
- SQLite caching layer
- Pre-compute common queries
- Optimize hot paths
- Benchmark early

### Risk: JSON Schema Changes

**Mitigation**:
- Version JSON schemas
- Migration tools for upgrades
- Backward compatibility
- Clear upgrade path

---

# Conclusion

---

## Why JSON Works for Divinum Officium

### ✅ Perfect Fit

1. **Configuration-Heavy**: Rules are configuration, not transactions
2. **Infrequent Writes**: Rules change rarely
3. **Git Workflow**: Version control is critical
4. **Small Team**: Simple deployment matters
5. **Transparency**: Rules must be readable

### ✅ Practical Benefits

- No database server to maintain
- Easy contributor onboarding
- Clear rule documentation
- Testable in isolation
- Version control friendly

---

## The Vision

### From This (Perl)

```perl
if ($srank[2] > $trank[2]) {
    $sanctoraloffice = 1;
} elsif ($trank[0] =~ /Dominica/i) {
    if ($version =~ /196/ && $srank[2] >= 6) {
        $sanctoraloffice = 1;
    }
}
```

### To This (JSON)

```json
{
  "rule": "Duplex I feast beats Sunday",
  "priority": 1,
  "conditions": {
    "sanctoral_rank": {"min": 6.0},
    "temporal_is_sunday": true
  },
  "result": {"winner": "sanctoral"}
}
```

**Clear, declarative, maintainable**

---

## Combined with TEI

**Perfect Architecture**:

```
TEI XML               →  Liturgical content
JSON Rules            →  Precedence logic
SQLite Cache          →  Performance
Python/Flask          →  Application layer
```

**Each technology used for its strength**

---

## Next Steps

### Immediate Actions

1. **Review this proposal**
2. **Discuss with team**
3. **Decide: JSON vs SQL**
4. **If JSON: Start Phase 1**

### Phase 1 Kickoff (Month 1)

1. Design JSON schemas
2. Create sample files
3. Build proof of concept
4. Validate approach

**Ready to proceed?**

---

## Success Metrics

### Technical Success
✅ 99%+ match with Perl system
✅ Performance < 100ms per office
✅ 100% rule coverage
✅ All versions supported

### Project Success
✅ Team can understand and modify rules
✅ New rubrics easy to add
✅ Community can contribute
✅ Long-term maintainable

### User Success
✅ No disruption to users
✅ Same accuracy as Perl
✅ Better performance (cached)
✅ New features enabled (API, search)

---

# Questions & Discussion

---

## Discussion Topics

1. **JSON vs SQL**: Which fits better?

2. **Timeline**: Is 10 months realistic?

3. **Resources**: Who can contribute?

4. **Priorities**:
   - Speed vs correctness?
   - Simplicity vs power?

5. **Concerns**: What worries you?

---

## Additional Resources

### Documentation
- **Full Analysis**: `claude-kb/json-vs-sql-analysis.md`
- **Migration Proposal**: `claude-kb/migration-proposal.md`
- **Precedence Model**: `claude-kb/precedence-data-model.md`

### JSON Resources
- **JSON Schema**: https://json-schema.org/
- **Python JSON**: https://docs.python.org/3/library/json.html
- **Validation Libraries**: jsonschema, pydantic

### Project
- **Repository**: https://github.com/DivinumOfficium/divinum-officium

---

# Thank You

**Questions?**

---

## Appendix: Code Examples

---

## Appendix A: Complete Version File

```json
{
  "version": {
    "code": "rubrics-1960",
    "name": "Rubrics of 1960",
    "year": 1960,
    "parent_version": "rubrics-1955",
    "description": "Last pre-Vatican II reform"
  },

  "parameters": {
    "vespers": {
      "min_rank_first_vespers": 6.0,
      "min_rank_first_vespers_exceptions": [
        {"condition": "is_feast_of_lord && day_of_week == 0", "min_rank": 5.0}
      ]
    },
    "commemorations": {
      "strategy": "strict_1960",
      "max_per_hour": 1,
      "min_rank_to_commemorate": 1.0
    },
    "octaves": {
      "suppress_common_octaves": true,
      "privileged_octaves_only": true,
      "octaves_list": ["Christmas", "Easter", "Pentecost"]
    },
    "special_offices": {
      "sanctoral_saturday_enabled": true,
      "sanctoral_saturday_min_temporal_rank": 1.4,
      "sanctoral_saturday_office": "C10"
    }
  },

  "concurrence_rules": [ /* ... */ ],
  "commemoration_rules": [ /* ... */ ],
  "vespers_rules": [ /* ... */ ]
}
```

---

## Appendix B: API Endpoints

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/office/<date>/<hour>')
def get_office(date, hour):
    """Get office for specific date and hour"""
    version = request.args.get('version', 'rubrics-1960')

    engine = PrecedenceEngine(version, parse_date(date))
    result = engine.get_office(hour)

    return jsonify({
        'date': date,
        'hour': hour,
        'version': version,
        'primary': result.primary.to_dict(),
        'commemorations': [c.to_dict() for c in result.commemorations]
    })

@app.route('/api/rules/<version>')
def get_rules(version):
    """Get all rules for a version"""
    loader = DataLoader()
    rules = loader.load_version(version)

    return jsonify(rules)

@app.route('/api/calendar/<year>/<month>')
def get_calendar(year, month):
    """Get calendar for month"""
    # Implementation
    pass
```

---

## Appendix C: JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Divinum Officium Version",
  "type": "object",
  "required": ["version", "concurrence_rules"],
  "properties": {
    "version": {
      "type": "object",
      "required": ["code", "name"],
      "properties": {
        "code": {"type": "string"},
        "name": {"type": "string"},
        "year": {"type": "integer"},
        "parent_version": {"type": "string"}
      }
    },
    "concurrence_rules": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["priority", "name", "result"],
        "properties": {
          "priority": {"type": "integer"},
          "name": {"type": "string"},
          "conditions": {"type": "object"},
          "result": {
            "type": "object",
            "required": ["winner"],
            "properties": {
              "winner": {"enum": ["office1", "office2", "higher_rank"]}
            }
          }
        }
      }
    }
  }
}
```

---

# End of Presentation

**Ready to build with JSON?**

Contact: [Project Team]

Repository: https://github.com/DivinumOfficium/divinum-officium
