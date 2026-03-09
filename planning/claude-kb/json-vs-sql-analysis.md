# JSON vs SQL for Precedence Rules - Detailed Analysis

## Executive Summary

**Yes, a JSON-based solution is viable and potentially superior** for the Divinum Officium precedence system, especially if combined with TEI XML data files. This document explores a pure file-based architecture using JSON for rules and TEI for content.

---

## Part 1: Why JSON Could Work Better

### 1.1 Advantages Over SQL for This Use Case

✅ **No Database Server Required**
- Simpler deployment (just files)
- No PostgreSQL installation/maintenance
- Easier for contributors to understand
- Git-friendly version control

✅ **Natural Hierarchy**
- JSON naturally represents nested rules
- Version inheritance through file structure
- Easier to visualize rule precedence

✅ **Better Version Control**
- Each version = separate JSON file
- Clear diffs in git
- Easy rollback of rule changes
- Branch-friendly for experimental rubrics

✅ **Portable & Self-Contained**
- Entire system can be a folder of files
- Easy backup (just copy directory)
- No database dumps needed
- Works offline immediately

✅ **Familiar Format**
- Most developers know JSON
- No SQL learning curve
- JavaScript/Python native support
- Easy manual editing

✅ **Aligns with Current Architecture**
- Current system already uses text files
- Maintains file-based philosophy
- Less architectural disruption
- Gradual migration easier

### 1.2 When SQL Would Be Better

SQL databases excel at:
- ❌ Complex ad-hoc queries across versions
- ❌ High-frequency writes (not applicable here)
- ❌ Concurrent modifications (rare in this project)
- ❌ Referential integrity enforcement
- ❌ Large-scale data analytics

**Reality Check**: Most of these don't apply to Divinum Officium:
- Queries are predictable (get office for date)
- Writes are infrequent (content updates)
- Concurrent edits rare (small contributor base)
- Integrity can be validated on load
- Analytics needs are minimal

---

## Part 2: Proposed JSON Architecture

### 2.1 Directory Structure

```
divinum-officium/
├── data/
│   ├── offices/                    # TEI XML files for office content
│   │   ├── temporal/
│   │   │   ├── Pent01-0.xml       # Trinity Sunday TEI
│   │   │   ├── Pasc0-0.xml        # Easter Sunday TEI
│   │   │   └── ...
│   │   ├── sanctoral/
│   │   │   ├── 01-01.xml          # Circumcision TEI
│   │   │   ├── 12-25.xml          # Christmas TEI
│   │   │   └── ...
│   │   └── commune/
│   │       ├── C1.xml             # Apostles TEI
│   │       └── ...
│   │
│   ├── versions/                   # Version-specific rule definitions
│   │   ├── tridentine-1570.json
│   │   ├── divino-afflatu-1939.json
│   │   ├── rubrics-1955.json
│   │   ├── rubrics-1960.json
│   │   ├── cistercian.json
│   │   └── dominican.json
│   │
│   ├── calendars/                  # Calendar definitions per version
│   │   ├── tridentine-1570/
│   │   │   ├── sanctoral.json     # Fixed date calendar
│   │   │   └── temporal.json      # Easter-relative dates
│   │   ├── rubrics-1960/
│   │   │   ├── sanctoral.json
│   │   │   └── temporal.json
│   │   └── ...
│   │
│   ├── transfers/                  # Transfer rules by version and Easter
│   │   ├── tridentine-1570/
│   │   │   ├── easter-a.json      # Easter letter A
│   │   │   ├── easter-b.json
│   │   │   ├── easter-322.json    # Easter March 22
│   │   │   ├── easter-425.json    # Easter April 25
│   │   │   └── permanent.json     # Fixed transfers
│   │   ├── rubrics-1960/
│   │   │   └── ...
│   │   └── ...
│   │
│   └── metadata/
│       ├── ranks.json              # Rank definitions (shared)
│       └── seasons.json            # Liturgical season metadata
│
└── cache/                          # Runtime cache (gitignored)
    └── computed-offices/
        ├── 1960-2025-01-01.json
        └── ...
```

### 2.2 Office Metadata (JSON Sidecar to TEI)

Each TEI office file has a companion JSON metadata file:

```json
// data/offices/sanctoral/12-25.json
{
  "office_key": "12-25",
  "office_type": "sanctoral",
  "names": {
    "latin": "In Nativitate Domini",
    "english": "The Nativity of Our Lord"
  },

  "ranks": {
    "tridentine-1570": {
      "rank_name": "Duplex I classis cum Octava privilegiata",
      "rank_numeric": 7.0,
      "rank_class": "duplex_i_privileged_octave",
      "properties": {
        "has_first_vespers": true,
        "has_second_vespers": true,
        "lectiones_count": 9,
        "is_feast_of_lord": true,
        "is_sunday": false,
        "octave_type": "privileged",
        "octave_days": 8
      },
      "commune_ref": null,
      "derives_from": null
    },

    "rubrics-1960": {
      "rank_name": "Duplex I classis",
      "rank_numeric": 6.0,
      "rank_class": "duplex_i",
      "properties": {
        "has_first_vespers": true,
        "has_second_vespers": true,
        "lectiones_count": 9,
        "is_feast_of_lord": true,
        "is_sunday": false,
        "octave_type": null,
        "octave_days": 0
      },
      "commune_ref": null,
      "derives_from": null
    }
  },

  "tei_file": "12-25.xml",
  "last_updated": "2025-12-28T10:00:00Z"
}
```

### 2.3 Version Definition File

```json
// data/versions/rubrics-1960.json
{
  "version": {
    "code": "rubrics-1960",
    "name": "Rubrics of 1960",
    "year": 1960,
    "parent_version": "rubrics-1955",
    "description": "Last pre-Vatican II reform of the Roman Breviary"
  },

  "parameters": {
    "vespers": {
      "min_rank_first_vespers": 6.0,
      "min_rank_first_vespers_exceptions": [
        {
          "condition": "is_feast_of_lord && day_of_week == 0",
          "min_rank": 5.0
        }
      ],
      "min_rank_second_vespers": 2.0,
      "rank_flattening_enabled": false
    },

    "commemorations": {
      "strategy": "strict_1960",
      "max_per_hour": 1,
      "min_rank_to_commemorate": 1.0
    },

    "octaves": {
      "suppress_common_octaves": true,
      "privileged_octaves_only": true,
      "octaves_list": [
        "Christmas",
        "Easter",
        "Pentecost"
      ]
    },

    "special_offices": {
      "sanctoral_saturday_enabled": true,
      "sanctoral_saturday_min_temporal_rank": 1.4,
      "sanctoral_saturday_min_sanctoral_rank": 1.4,
      "sanctoral_saturday_office": "C10"
    }
  },

  "concurrence_rules": [
    {
      "priority": 1,
      "name": "Duplex I classis feast of Lord beats Duplex II classis Sunday",
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
      "priority": 2,
      "name": "Duplex II classis feast of Lord on Sunday beats Duplex II classis Sunday",
      "conditions": {
        "office1": {
          "type": "sanctoral",
          "rank": {"min": 5.0, "max": 5.99},
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
      "name": "Default: higher numeric rank wins",
      "conditions": {},
      "result": {
        "winner": "higher_rank",
        "commemorate_loser": true
      }
    }
  ],

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
        "winner": {
          "properties": {"is_sunday": true}
        },
        "candidate": {
          "rank": {"min": 5.0, "max": 5.99}
        }
      },
      "result": {
        "commemorated": true,
        "type": "laudes_only"
      }
    },

    {
      "canonical_hours": ["all"],
      "conditions": {
        "candidate": {
          "rank": {"max": 1.0}
        }
      },
      "result": {
        "commemorated": false,
        "type": "none"
      }
    }
  ],

  "vespers_rules": [
    {
      "priority": 1,
      "name": "No first Vespers for offices below Duplex I classis",
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
      "name": "Exception: Duplex II classis feast of Lord on Sunday gets first Vespers",
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
    },

    {
      "priority": 100,
      "name": "Standard precedence: higher rank wins",
      "conditions": {},
      "result": {
        "comparison": "rank",
        "commemorate_loser": true
      }
    }
  ],

  "rank_adjustments": {
    "enabled": false,
    "description": "1960 rubrics don't use rank flattening"
  }
}
```

### 2.4 Calendar File

```json
// data/calendars/rubrics-1960/sanctoral.json
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

    "01-06": [
      {
        "office_key": "01-06",
        "priority": 1,
        "note": "Epiphany"
      }
    ],

    "03-19": [
      {
        "office_key": "03-19",
        "priority": 1,
        "note": "St. Joseph, transferred if in Lent",
        "transfer_conditions": {
          "if_season": "lent",
          "see_transfer_table": true
        }
      }
    ],

    "03-25": [
      {
        "office_key": "03-25",
        "priority": 1,
        "note": "Annunciation of the BVM"
      }
    ],

    "12-25": [
      {
        "office_key": "12-25",
        "priority": 1,
        "note": "Nativity of Our Lord"
      }
    ]
  },

  "last_updated": "2025-12-28"
}
```

```json
// data/calendars/rubrics-1960/temporal.json
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
      "office_key": "Pasc0-1",
      "offset_from_easter": 1,
      "name": "Feria II infra Octavam Paschae",
      "season": "easter"
    },
    {
      "office_key": "Pent0-0",
      "offset_from_easter": 49,
      "name": "Dominica Pentecostes",
      "season": "pentecost"
    },
    {
      "office_key": "Pent01-0",
      "offset_from_easter": 56,
      "name": "Dominica Sanctissimae Trinitatis",
      "season": "post_pentecost"
    },
    {
      "office_key": "Quad1-0",
      "offset_from_easter": -42,
      "name": "Dominica I in Quadragesima",
      "season": "lent"
    }
  ],

  "last_updated": "2025-12-28"
}
```

### 2.5 Transfer Rules

```json
// data/transfers/rubrics-1960/easter-322.json
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
        "reason": "St. Joseph falls in Holy Week, transferred after Easter Octave"
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
        "reason": "Annunciation falls in Holy Week, transferred after Easter Octave"
      }
    }
  ],

  "last_updated": "2025-12-28"
}
```

```json
// data/transfers/rubrics-1960/permanent.json
{
  "version": "rubrics-1960",
  "trigger": {
    "type": "permanent",
    "description": "Transfers that apply every year regardless of Easter"
  },

  "transfers": [
    {
      "from": {
        "date": "12-28",
        "office_key": "12-28",
        "name": "Holy Innocents",
        "condition": "day_of_week == 0"
      },
      "to": {
        "date": "12-29",
        "reason": "If Holy Innocents falls on Sunday, observed on Monday"
      }
    }
  ],

  "last_updated": "2025-12-28"
}
```

### 2.6 Shared Rank Definitions

```json
// data/metadata/ranks.json
{
  "rank_classes": {
    "duplex_i_privileged_octave": {
      "numeric_range": [7.0, 7.99],
      "name_latin": "Duplex I classis cum Octava privilegiata",
      "name_english": "Double of the First Class with Privileged Octave",
      "properties": {
        "has_first_vespers": true,
        "has_second_vespers": true,
        "default_lectiones": 9,
        "excludes_all_commemorations": true
      }
    },

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
    },

    "duplex_majus": {
      "numeric_range": [4.0, 4.99],
      "name_latin": "Duplex majus",
      "name_english": "Greater Double",
      "properties": {
        "has_first_vespers": false,
        "has_second_vespers": true,
        "default_lectiones": 9
      }
    },

    "duplex": {
      "numeric_range": [3.0, 3.99],
      "name_latin": "Duplex",
      "name_english": "Double",
      "properties": {
        "has_first_vespers": false,
        "has_second_vespers": true,
        "default_lectiones": 9
      }
    },

    "semiduplex": {
      "numeric_range": [2.0, 2.99],
      "name_latin": "Semiduplex",
      "name_english": "Semidouble",
      "properties": {
        "has_first_vespers": false,
        "has_second_vespers": false,
        "default_lectiones": 3
      }
    },

    "simplex": {
      "numeric_range": [1.0, 1.99],
      "name_latin": "Simplex",
      "name_english": "Simple",
      "properties": {
        "has_first_vespers": false,
        "has_second_vespers": false,
        "default_lectiones": 3
      }
    }
  }
}
```

---

## Part 3: Python Implementation with JSON

### 3.1 Loading JSON Data

```python
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import date, timedelta

class DataLoader:
    def __init__(self, data_root: Path):
        self.data_root = data_root
        self._cache = {}

    def load_version(self, version_code: str) -> Dict:
        """Load version definition with parent inheritance"""
        cache_key = f"version:{version_code}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        version_path = self.data_root / "versions" / f"{version_code}.json"
        with open(version_path) as f:
            version_data = json.load(f)

        # Load and merge parent if exists
        parent_code = version_data.get("version", {}).get("parent_version")
        if parent_code:
            parent_data = self.load_version(parent_code)
            version_data = self._merge_versions(parent_data, version_data)

        self._cache[cache_key] = version_data
        return version_data

    def _merge_versions(self, parent: Dict, child: Dict) -> Dict:
        """Deep merge child version over parent (child wins)"""
        result = parent.copy()

        for key, value in child.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_versions(result[key], value)
            else:
                result[key] = value

        return result

    def load_office_metadata(self, office_key: str, office_type: str) -> Dict:
        """Load office metadata JSON"""
        cache_key = f"office:{office_type}:{office_key}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        office_path = self.data_root / "offices" / office_type / f"{office_key}.json"
        with open(office_path) as f:
            office_data = json.load(f)

        self._cache[cache_key] = office_data
        return office_data

    def load_calendar(self, version_code: str, calendar_type: str) -> Dict:
        """Load sanctoral or temporal calendar"""
        cache_key = f"calendar:{version_code}:{calendar_type}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        calendar_path = self.data_root / "calendars" / version_code / f"{calendar_type}.json"
        with open(calendar_path) as f:
            calendar_data = json.load(f)

        self._cache[cache_key] = calendar_data
        return calendar_data

    def load_transfers(self, version_code: str, easter_date: date) -> List[Dict]:
        """Load applicable transfer rules for this Easter date"""
        transfer_dir = self.data_root / "transfers" / version_code

        # Calculate Easter letter
        easter_letter = self._calculate_easter_letter(easter_date)
        easter_key = f"{easter_date.month:02d}{easter_date.day:02d}"

        transfers = []

        # Load permanent transfers
        permanent_path = transfer_dir / "permanent.json"
        if permanent_path.exists():
            with open(permanent_path) as f:
                transfers.extend(json.load(f).get("transfers", []))

        # Load Easter letter specific transfers
        letter_path = transfer_dir / f"easter-{easter_letter}.json"
        if letter_path.exists():
            with open(letter_path) as f:
                transfers.extend(json.load(f).get("transfers", []))

        # Load Easter date specific transfers
        date_path = transfer_dir / f"easter-{easter_key}.json"
        if date_path.exists():
            with open(date_path) as f:
                transfers.extend(json.load(f).get("transfers", []))

        return transfers

    def _calculate_easter_letter(self, easter_date: date) -> str:
        """Calculate Easter letter (a-g)"""
        base_date = date(easter_date.year, 3, 21)
        days_offset = (easter_date - base_date).days
        return chr(ord('a') + (days_offset % 7))
```

### 3.2 Office Resolution

```python
@dataclass
class Office:
    key: str
    type: str  # 'temporal', 'sanctoral', 'commune'
    name: str
    rank: 'Rank'
    metadata: Dict
    tei_path: Path

@dataclass
class Rank:
    numeric: float
    name: str
    class_name: str
    has_first_vespers: bool
    has_second_vespers: bool
    lectiones_count: int
    is_feast_of_lord: bool
    is_sunday: bool
    is_vigil: bool
    octave_type: Optional[str]

class OfficeResolver:
    def __init__(self, data_loader: DataLoader, version_code: str):
        self.loader = data_loader
        self.version_code = version_code
        self.version_data = data_loader.load_version(version_code)

    def get_office(self, office_key: str, office_type: str) -> Office:
        """Load and construct an Office object"""
        metadata = self.loader.load_office_metadata(office_key, office_type)

        # Get rank for this version
        rank_data = metadata["ranks"].get(self.version_code)
        if not rank_data:
            raise ValueError(f"No rank defined for {office_key} in {self.version_code}")

        rank = Rank(
            numeric=rank_data["rank_numeric"],
            name=rank_data["rank_name"],
            class_name=rank_data["rank_class"],
            **rank_data["properties"]
        )

        tei_path = (
            self.loader.data_root / "offices" / office_type / metadata["tei_file"]
        )

        return Office(
            key=office_key,
            type=office_type,
            name=metadata["names"]["latin"],
            rank=rank,
            metadata=metadata,
            tei_path=tei_path
        )

    def get_offices_for_date(self, target_date: date) -> Dict[str, List[Office]]:
        """Get all offices (temporal + sanctoral) for a given date"""

        # Get temporal office
        temporal_calendar = self.loader.load_calendar(self.version_code, "temporal")
        temporal_office = self._find_temporal_office(target_date, temporal_calendar)

        # Get sanctoral offices
        sanctoral_calendar = self.loader.load_calendar(self.version_code, "sanctoral")
        sanctoral_offices = self._find_sanctoral_offices(target_date, sanctoral_calendar)

        return {
            "temporal": [temporal_office] if temporal_office else [],
            "sanctoral": sanctoral_offices
        }

    def _find_temporal_office(self, target_date: date, calendar: Dict) -> Optional[Office]:
        """Find temporal office based on Easter offset"""
        easter_date = calculate_easter(target_date.year)
        offset = (target_date - easter_date).days

        for entry in calendar["entries"]:
            if entry["offset_from_easter"] == offset:
                return self.get_office(entry["office_key"], "temporal")

        return None

    def _find_sanctoral_offices(self, target_date: date, calendar: Dict) -> List[Office]:
        """Find sanctoral offices for this date"""
        date_key = f"{target_date.month:02d}-{target_date.day:02d}"

        offices = []
        entries = calendar.get("entries", {}).get(date_key, [])

        for entry in sorted(entries, key=lambda e: e.get("priority", 999)):
            office = self.get_office(entry["office_key"], "sanctoral")
            offices.append(office)

        return offices
```

### 3.3 Rule Engine with JSON Rules

```python
class RuleEngine:
    def __init__(self, version_data: Dict):
        self.version_data = version_data
        self.concurrence_rules = version_data.get("concurrence_rules", [])
        self.commemoration_rules = version_data.get("commemoration_rules", [])
        self.vespers_rules = version_data.get("vespers_rules", [])

    def resolve_concurrence(
        self,
        temporal: Optional[Office],
        sanctorals: List[Office],
        context: Dict
    ) -> Office:
        """Apply concurrence rules to determine winner"""

        if not sanctorals:
            return temporal

        if not temporal:
            return max(sanctorals, key=lambda o: o.rank.numeric)

        # Get best sanctoral
        best_sanctoral = max(sanctorals, key=lambda o: o.rank.numeric)

        # Apply rules in priority order
        for rule in sorted(self.concurrence_rules, key=lambda r: r.get("priority", 999)):
            if self._matches_rule(rule, temporal, best_sanctoral, context):
                winner_choice = rule["result"]["winner"]

                if winner_choice == "office1":
                    return best_sanctoral
                elif winner_choice == "office2":
                    return temporal
                elif winner_choice == "higher_rank":
                    return best_sanctoral if best_sanctoral.rank.numeric > temporal.rank.numeric else temporal

        # Default fallback
        return best_sanctoral if best_sanctoral.rank.numeric > temporal.rank.numeric else temporal

    def _matches_rule(
        self,
        rule: Dict,
        office1: Office,
        office2: Office,
        context: Dict
    ) -> bool:
        """Check if a rule's conditions match the given offices"""
        conditions = rule.get("conditions", {})

        if not conditions:
            return True  # Default rule with no conditions

        # Check office1 conditions
        if "office1" in conditions:
            if not self._matches_office_conditions(office1, conditions["office1"], context):
                return False

        # Check office2 conditions
        if "office2" in conditions:
            if not self._matches_office_conditions(office2, conditions["office2"], context):
                return False

        return True

    def _matches_office_conditions(
        self,
        office: Office,
        conditions: Dict,
        context: Dict
    ) -> bool:
        """Check if an office matches specific conditions"""

        # Check type
        if "type" in conditions and office.type != conditions["type"]:
            return False

        # Check rank range
        if "rank" in conditions:
            rank_cond = conditions["rank"]
            if "min" in rank_cond and office.rank.numeric < rank_cond["min"]:
                return False
            if "max" in rank_cond and office.rank.numeric > rank_cond["max"]:
                return False

        # Check properties
        if "properties" in conditions:
            for prop, expected_value in conditions["properties"].items():
                actual_value = getattr(office.rank, prop, None)
                if actual_value != expected_value:
                    return False

        # Check context (day of week, season, etc.)
        if "day_of_week" in conditions:
            if context.get("day_of_week") != conditions["day_of_week"]:
                return False

        return True

    def determine_commemorations(
        self,
        winner: Office,
        candidates: List[Office],
        canonical_hour: str,
        context: Dict
    ) -> List[Office]:
        """Determine which offices should be commemorated"""

        commemorations = []

        for candidate in candidates:
            if candidate == winner:
                continue

            for rule in self.commemoration_rules:
                # Check if rule applies to this hour
                hours = rule.get("canonical_hours", [])
                if hours and canonical_hour not in hours and "all" not in hours:
                    continue

                # Check conditions
                if self._matches_commemoration_rule(rule, winner, candidate, context):
                    if rule["result"]["commemorated"]:
                        commemorations.append(candidate)
                    break  # First matching rule wins

        return commemorations

    def _matches_commemoration_rule(
        self,
        rule: Dict,
        winner: Office,
        candidate: Office,
        context: Dict
    ) -> bool:
        """Check if commemoration rule conditions match"""
        conditions = rule.get("conditions", {})

        if "winner" in conditions:
            if not self._matches_office_conditions(winner, conditions["winner"], context):
                return False

        if "candidate" in conditions:
            if not self._matches_office_conditions(candidate, conditions["candidate"], context):
                return False

        return True
```

### 3.4 Caching Layer

```python
import hashlib
from pathlib import Path

class CacheManager:
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)

    def get_cached_office(
        self,
        version_code: str,
        date: date,
        canonical_hour: str
    ) -> Optional[Dict]:
        """Retrieve cached office result"""
        cache_key = self._make_cache_key(version_code, date, canonical_hour)
        cache_path = self.cache_dir / f"{cache_key}.json"

        if cache_path.exists():
            with open(cache_path) as f:
                cached = json.load(f)
                # Check if cache is still valid (could add timestamp check)
                return cached

        return None

    def set_cached_office(
        self,
        version_code: str,
        date: date,
        canonical_hour: str,
        result: Dict
    ):
        """Store office result in cache"""
        cache_key = self._make_cache_key(version_code, date, canonical_hour)
        cache_path = self.cache_dir / f"{cache_key}.json"

        with open(cache_path, 'w') as f:
            json.dump(result, f, indent=2)

    def _make_cache_key(self, version_code: str, date: date, canonical_hour: str) -> str:
        """Generate unique cache key"""
        key_string = f"{version_code}:{date.isoformat()}:{canonical_hour}"
        return hashlib.md5(key_string.encode()).hexdigest()

    def invalidate_all(self):
        """Clear all cached results"""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
```

---

## Part 4: Comparison Matrix

| Aspect | SQL Database | JSON Files |
|--------|-------------|------------|
| **Setup Complexity** | ❌ Requires PostgreSQL server | ✅ Just files, no server |
| **Version Control** | ⚠️ Need dumps/migrations | ✅ Native git support |
| **Query Flexibility** | ✅ Complex ad-hoc queries | ⚠️ Pre-defined queries only |
| **Performance (reads)** | ✅ Indexed lookups fast | ⚠️ File I/O, but cacheable |
| **Performance (writes)** | ✅ Optimized for updates | ✅ Writes are rare anyway |
| **Data Integrity** | ✅ Foreign keys, constraints | ⚠️ Validation on load |
| **Portability** | ⚠️ Need database export | ✅ Copy folder = done |
| **Backup/Restore** | ⚠️ Database dumps | ✅ Standard file backup |
| **Developer Familiarity** | ⚠️ Need SQL knowledge | ✅ JSON is universal |
| **Contributor Barrier** | ❌ Can't easily edit data | ✅ Edit JSON in text editor |
| **Migration from Current** | ❌ Big architectural shift | ✅ Similar to current approach |
| **Scalability** | ✅ Handles millions of records | ⚠️ Fine for liturgical data (<10K records) |
| **Referential Integrity** | ✅ Enforced by DB | ⚠️ Must validate programmatically |
| **Deployment** | ❌ Need DB provisioning | ✅ Static files, simple deploy |
| **Testing** | ⚠️ Need test database | ✅ Test fixtures as JSON |
| **Documentation** | ⚠️ Need schema docs | ✅ Self-documenting format |

---

## Part 5: Hybrid Approach (Best of Both)

### 5.1 JSON for Rules, SQLite for Computed Results

```python
# Use JSON for all configuration/rules
# Use SQLite for runtime cache and queries

import sqlite3

class HybridDataManager:
    def __init__(self, data_root: Path, cache_db_path: Path):
        self.json_loader = DataLoader(data_root)
        self.db = sqlite3.connect(cache_db_path)
        self._init_cache_schema()

    def _init_cache_schema(self):
        """Create lightweight SQLite tables for caching"""
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS computed_offices (
                version_code TEXT,
                date TEXT,
                canonical_hour TEXT,
                winner_office_key TEXT,
                winner_office_type TEXT,
                commemorations TEXT,  -- JSON array
                computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (version_code, date, canonical_hour)
            )
        """)

        self.db.execute("""
            CREATE INDEX IF NOT EXISTS idx_date
            ON computed_offices(version_code, date)
        """)

    def get_office_result(self, version_code: str, date: str, hour: str):
        """Try cache first, compute if needed"""
        cursor = self.db.execute("""
            SELECT winner_office_key, winner_office_type, commemorations
            FROM computed_offices
            WHERE version_code = ? AND date = ? AND canonical_hour = ?
        """, (version_code, date, hour))

        row = cursor.fetchone()
        if row:
            return {
                "winner": {"key": row[0], "type": row[1]},
                "commemorations": json.loads(row[2])
            }

        # Not cached, compute from JSON rules
        result = self._compute_office(version_code, date, hour)
        self._cache_result(version_code, date, hour, result)
        return result

    def query_all_offices_in_range(self, version: str, start: date, end: date):
        """SQL query for analysis - leverages SQLite"""
        cursor = self.db.execute("""
            SELECT date, winner_office_key, winner_office_type
            FROM computed_offices
            WHERE version_code = ?
              AND date BETWEEN ? AND ?
            ORDER BY date
        """, (version, start.isoformat(), end.isoformat()))

        return cursor.fetchall()
```

---

## Part 6: Recommendation

### **Use JSON Files with Lightweight SQLite Cache**

**Primary Data**: JSON files
- Version definitions
- Rank metadata
- Calendars
- Transfer rules
- Concurrence/commemoration/vespers rules

**Runtime Cache**: SQLite
- Computed office results
- Enables fast queries
- Easy to regenerate from JSON

**Content**: TEI XML files
- Actual liturgical texts
- Prayers, readings, antiphons

### Why This Works Best

✅ **Simple deployment**: No PostgreSQL server needed
✅ **Git-friendly**: All rules versioned in git
✅ **Easy contributions**: Edit JSON in any editor
✅ **Performance**: SQLite cache for speed
✅ **Portable**: Entire system is a directory
✅ **Testable**: Mock JSON for unit tests
✅ **Queryable**: SQLite for analytics when needed
✅ **Aligns with current architecture**: Similar to existing file-based system

### Migration Path

1. **Phase 1**: Convert current text files to JSON metadata + TEI
2. **Phase 2**: Implement JSON-based rule engine in Python
3. **Phase 3**: Add SQLite cache layer
4. **Phase 4**: Build Flask web interface
5. **Phase 5**: Validate against Perl output
6. **Phase 6**: Gradual transition to new system

---

## Conclusion

**Yes, JSON is not only viable but likely superior** for this use case because:

1. The data is **configuration-heavy, not transaction-heavy**
2. **Version control** is critical for tracking rule changes
3. **Contributor accessibility** matters more than query flexibility
4. **Deployment simplicity** is valuable
5. **File-based philosophy** aligns with project culture

The hybrid approach (JSON + SQLite cache) gives you the best of both worlds:
- JSON for maintainability and version control
- SQLite for performance and ad-hoc queries
- No heavyweight database server
- Natural fit with TEI XML content files

This architecture would be a **natural evolution** from the current Perl + text file system, rather than a disruptive revolution.

---

**Document Version**: 1.0
**Last Updated**: 2025-12-28
**Author**: Claude (Sonnet 4.5)
