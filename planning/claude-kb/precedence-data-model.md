# Precedence Rules - Data Model Design

## Executive Summary

The precedence system in Divinum Officium is complex because it encodes **centuries of liturgical law** with **version-specific variations**. A suitable data model must:

1. Represent ranks hierarchically with version-specific overrides
2. Model temporal/sanctoral office concurrence
3. Handle transfers based on movable feast dates (Easter)
4. Encode commemoration rules
5. Support Vespers precedence logic (1st vs 2nd Vespers)
6. Allow conditional rules based on rubrical version, day of week, season

## Recommended Approach: Hybrid Model

**Database Schema (PostgreSQL/SQLite) + Rule Engine**

### Core Principle
- **Data in database**: Offices, ranks, calendars, base transfer rules
- **Logic in code**: Complex precedence algorithms, version-specific conditionals
- **Configuration files**: Version definitions, rule parameters

This separates **declarative data** (what offices exist) from **procedural logic** (how to choose between them).

---

## Part 1: Database Schema

### 1.1 Office Definition

```sql
-- Core office metadata
CREATE TABLE offices (
    id                  SERIAL PRIMARY KEY,
    office_type         VARCHAR(20) NOT NULL,  -- 'temporal', 'sanctoral', 'commune'
    office_key          VARCHAR(50) NOT NULL,  -- e.g., 'Pent01-0', '12-25', 'C1'
    name_latin          TEXT NOT NULL,
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP DEFAULT NOW(),

    UNIQUE(office_type, office_key)
);

CREATE INDEX idx_offices_type_key ON offices(office_type, office_key);

-- Example records:
-- ('temporal', 'Pent01-0', 'Dominica Sanctissimæ Trinitatis')
-- ('sanctoral', '12-25', 'In Nativitate Domini')
-- ('commune', 'C1', 'Commune Apostolorum')
```

### 1.2 Rank System

```sql
-- Rank definitions per version
CREATE TABLE ranks (
    id                  SERIAL PRIMARY KEY,
    office_id           INTEGER REFERENCES offices(id),
    version_id          INTEGER REFERENCES versions(id),

    -- Rank components
    rank_name           VARCHAR(100),      -- 'Duplex I classis', 'Semiduplex'
    rank_numeric        DECIMAL(4,2),      -- 7.0, 6.0, 5.09, etc.
    rank_class          VARCHAR(50),       -- 'duplex_i', 'duplex_ii', 'semiduplex'

    -- Liturgical properties
    has_first_vespers   BOOLEAN DEFAULT TRUE,
    has_second_vespers  BOOLEAN DEFAULT TRUE,
    lectiones_count     INTEGER DEFAULT 3, -- 3, 9, or 12
    is_feast_of_lord    BOOLEAN DEFAULT FALSE,
    is_sunday           BOOLEAN DEFAULT FALSE,
    is_vigil            BOOLEAN DEFAULT FALSE,
    is_octave           BOOLEAN DEFAULT FALSE,
    octave_type         VARCHAR(20),       -- 'privileged', 'common', 'simple'

    -- Common office reference
    commune_ref         VARCHAR(20),       -- 'C1', 'C4a', etc.
    derives_from        INTEGER REFERENCES offices(id), -- 'ex Sancti/12-25'

    created_at          TIMESTAMP DEFAULT NOW(),

    UNIQUE(office_id, version_id)
);

CREATE INDEX idx_ranks_version ON ranks(version_id);
CREATE INDEX idx_ranks_numeric ON ranks(rank_numeric);

-- Example:
-- office: '01-01' (Circumcision)
-- version: 'Rubrics 1960'
-- rank_numeric: 6.0
-- rank_class: 'duplex_i'
-- has_first_vespers: true
```

### 1.3 Version Definitions

```sql
CREATE TABLE versions (
    id                  SERIAL PRIMARY KEY,
    version_code        VARCHAR(50) UNIQUE NOT NULL, -- 'tridentine', '1960', 'divino_afflatu'
    version_name        TEXT NOT NULL,
    version_year        INTEGER,
    parent_version_id   INTEGER REFERENCES versions(id), -- Inheritance chain

    -- Version parameters (JSON for flexibility)
    parameters          JSONB,

    created_at          TIMESTAMP DEFAULT NOW()
);

-- Parameters examples:
-- {
--   "suppress_octaves": false,
--   "min_rank_first_vespers": 5.0,
--   "min_rank_second_vespers": 2.0,
--   "sanctoral_saturday_min_rank": 1.4,
--   "commemoration_rules": "pre_divino_afflatu"
-- }
```

### 1.4 Calendar System

```sql
-- Fixed calendar dates
CREATE TABLE sanctoral_calendar (
    id                  SERIAL PRIMARY KEY,
    version_id          INTEGER REFERENCES versions(id),
    month               INTEGER CHECK (month BETWEEN 1 AND 12),
    day                 INTEGER CHECK (day BETWEEN 1 AND 31),
    office_id           INTEGER REFERENCES offices(id),
    priority            INTEGER DEFAULT 1,  -- When multiple offices on same day

    UNIQUE(version_id, month, day, office_id)
);

CREATE INDEX idx_calendar_date ON sanctoral_calendar(version_id, month, day);

-- Temporal cycle (relative to Easter)
CREATE TABLE temporal_calendar (
    id                  SERIAL PRIMARY KEY,
    version_id          INTEGER REFERENCES versions(id),
    offset_from_easter  INTEGER NOT NULL,  -- Days before/after Easter (negative = before)
    office_id           INTEGER REFERENCES offices(id),
    season              VARCHAR(50),       -- 'advent', 'lent', 'easter', 'pentecost'

    UNIQUE(version_id, offset_from_easter)
);

CREATE INDEX idx_temporal_offset ON temporal_calendar(version_id, offset_from_easter);

-- Example temporal records:
-- offset: -49 = Septuagesima (49 days before Easter)
-- offset: -46 = Sexagesima
-- offset: 0 = Easter Sunday
-- offset: 7 = Easter Octave Day
-- offset: 49 = Pentecost
```

### 1.5 Transfer Rules

```sql
-- Date-based transfers (depends on Easter date and letter)
CREATE TABLE transfer_rules (
    id                  SERIAL PRIMARY KEY,
    version_id          INTEGER REFERENCES versions(id),

    -- Trigger conditions
    trigger_type        VARCHAR(20) NOT NULL, -- 'easter_letter', 'easter_date', 'fixed_date'
    easter_letter       CHAR(1),              -- 'a' through 'g'
    easter_month        INTEGER,
    easter_day          INTEGER,

    -- Source date (what gets transferred FROM)
    source_month        INTEGER,
    source_day          INTEGER,
    source_office_id    INTEGER REFERENCES offices(id),

    -- Destination date (what gets transferred TO)
    dest_month          INTEGER,
    dest_day            INTEGER,
    dest_office_id      INTEGER REFERENCES offices(id),

    -- Conditions
    applies_when        JSONB,  -- Additional conditions as JSON

    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_transfer_version ON transfer_rules(version_id);
CREATE INDEX idx_transfer_easter ON transfer_rules(easter_letter, easter_month, easter_day);

-- Example:
-- When Easter is March 22 (earliest possible):
-- Transfer St. Joseph (03-19) to different date to avoid Lent conflicts
```

### 1.6 Concurrence Resolution Rules

```sql
-- Rules for when two offices compete for same day
CREATE TABLE concurrence_rules (
    id                  SERIAL PRIMARY KEY,
    version_id          INTEGER REFERENCES versions(id),
    rule_priority       INTEGER NOT NULL,  -- Order of evaluation

    -- Conditions (all must match)
    office1_type        VARCHAR(20),       -- 'temporal', 'sanctoral', 'any'
    office1_min_rank    DECIMAL(4,2),
    office1_max_rank    DECIMAL(4,2),
    office1_properties  JSONB,             -- e.g., {"is_sunday": true}

    office2_type        VARCHAR(20),
    office2_min_rank    DECIMAL(4,2),
    office2_max_rank    DECIMAL(4,2),
    office2_properties  JSONB,

    -- Additional context conditions
    day_of_week         INTEGER,           -- 0-6, NULL = any
    season              VARCHAR(50),       -- 'advent', 'lent', NULL = any

    -- Result
    winner              VARCHAR(10),       -- 'office1', 'office2', 'both'
    commemorate_loser   BOOLEAN DEFAULT TRUE,

    -- Special actions
    rank_adjustment     JSONB,             -- {"office1": "+0.5", "office2": "-1.0"}

    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_concurrence_version ON concurrence_rules(version_id, rule_priority);

-- Example rule:
-- version: '1960'
-- office1: {type: 'sanctoral', min_rank: 6.0, is_feast_of_lord: true}
-- office2: {type: 'temporal', max_rank: 5.0, is_sunday: true}
-- winner: 'office1'
-- commemorate_loser: false
-- Meaning: In 1960, Duplex I class feasts of the Lord beat Duplex II class Sundays
```

### 1.7 Commemoration Rules

```sql
CREATE TABLE commemoration_rules (
    id                  SERIAL PRIMARY KEY,
    version_id          INTEGER REFERENCES versions(id),
    canonical_hour      VARCHAR(20),       -- 'laudes', 'vespers', 'all', etc.

    -- Winner properties
    winner_min_rank     DECIMAL(4,2),
    winner_max_rank     DECIMAL(4,2),
    winner_properties   JSONB,

    -- Commemorated office properties
    commem_min_rank     DECIMAL(4,2),
    commem_max_rank     DECIMAL(4,2),
    commem_properties   JSONB,

    -- Additional conditions
    day_of_week         INTEGER,
    season              VARCHAR(50),

    -- Result
    is_commemorated     BOOLEAN DEFAULT TRUE,
    commemoration_type  VARCHAR(20),       -- 'full', 'laudes_only', 'none'

    created_at          TIMESTAMP DEFAULT NOW()
);

-- Example:
-- version: '1960'
-- canonical_hour: 'laudes'
-- winner: {is_sunday: true, rank < 6.0}
-- commem: {type: 'sanctoral', rank >= 5.0, rank < 6.0}
-- commemoration_type: 'laudes_only'
```

### 1.8 Vespers Precedence

```sql
CREATE TABLE vespers_rules (
    id                  SERIAL PRIMARY KEY,
    version_id          INTEGER REFERENCES versions(id),
    rule_priority       INTEGER NOT NULL,

    -- Today's office (providing 2nd Vespers)
    today_office_type   VARCHAR(20),
    today_min_rank      DECIMAL(4,2),
    today_max_rank      DECIMAL(4,2),
    today_properties    JSONB,

    -- Tomorrow's office (providing 1st Vespers)
    tomorrow_office_type VARCHAR(20),
    tomorrow_min_rank   DECIMAL(4,2),
    tomorrow_max_rank   DECIMAL(4,2),
    tomorrow_properties JSONB,

    -- Context
    day_of_week         INTEGER,
    season              VARCHAR(50),

    -- Result
    vespers_choice      VARCHAR(20),       -- 'first', 'second', 'both_a_capitulo'
    commemorate_other   BOOLEAN DEFAULT TRUE,

    created_at          TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_vespers_version ON vespers_rules(version_id, rule_priority);

-- Example:
-- tomorrow: {rank: 6.0, has_first_vespers: true}
-- today: {rank: 5.0}
-- vespers_choice: 'first'  (tomorrow wins, use 1st Vespers)
```

---

## Part 2: Rule Engine Architecture

### 2.1 Rule Evaluation Flow

```python
# Pseudocode for precedence engine

class PrecedenceEngine:
    def __init__(self, version: Version, date: Date):
        self.version = version
        self.date = date
        self.easter_date = calculate_easter(date.year)
        self.transfers = load_transfers(version, easter_date)

    def get_office_for_hour(self, canonical_hour: str) -> OfficeResult:
        """Main entry point for office determination"""

        if canonical_hour in ['vespers', 'completorium']:
            return self._handle_vespers()
        else:
            return self._handle_other_hours(canonical_hour)

    def _handle_other_hours(self, hour: str) -> OfficeResult:
        """For all hours except Vespers/Completorium"""

        # Get competing offices for this date
        temporal_office = self._get_temporal_office(self.date)
        sanctoral_offices = self._get_sanctoral_offices(self.date)

        # Apply transfers
        temporal_office = self._apply_transfer(temporal_office)
        sanctoral_offices = [self._apply_transfer(o) for o in sanctoral_offices]

        # Add special Saturday office if applicable
        if self.date.weekday == 6:  # Saturday
            saturday_office = self._check_saturday_bvm()
            if saturday_office:
                sanctoral_offices.append(saturday_office)

        # Resolve concurrence
        winner = self._resolve_concurrence(
            temporal_office,
            sanctoral_offices,
            hour
        )

        # Determine commemorations
        commemorations = self._determine_commemorations(
            winner,
            temporal_office,
            sanctoral_offices,
            hour
        )

        return OfficeResult(
            primary=winner,
            commemorations=commemorations,
            hour=hour
        )

    def _resolve_concurrence(
        self,
        temporal: Office,
        sanctorals: List[Office],
        hour: str
    ) -> Office:
        """Apply concurrence rules to choose winner"""

        # Get all applicable rules for this version
        rules = self._get_concurrence_rules()

        # Choose best sanctoral if multiple
        best_sanctoral = max(sanctorals, key=lambda o: o.rank.numeric) if sanctorals else None

        if not best_sanctoral:
            return temporal

        if not temporal:
            return best_sanctoral

        # Apply rules in priority order
        for rule in rules:
            if rule.matches(temporal, best_sanctoral, self.date, hour):
                winner = rule.apply(temporal, best_sanctoral)
                return winner

        # Default: higher rank wins
        if best_sanctoral.rank.numeric > temporal.rank.numeric:
            return best_sanctoral
        else:
            return temporal

    def _handle_vespers(self) -> OfficeResult:
        """Special handling for Vespers with 1st/2nd Vespers logic"""

        # Get today's office (for 2nd Vespers)
        today_result = self._handle_other_hours('vespers_temp')

        # Get tomorrow's office (for 1st Vespers)
        tomorrow_date = self.date + timedelta(days=1)
        tomorrow_engine = PrecedenceEngine(self.version, tomorrow_date)
        tomorrow_result = tomorrow_engine._handle_other_hours('vespers_temp')

        # Check if tomorrow has 1st Vespers
        if not tomorrow_result.primary.rank.has_first_vespers:
            # Use today's 2nd Vespers
            return OfficeResult(
                primary=today_result.primary,
                vespers_type='second',
                commemorations=today_result.commemorations
            )

        # Check if today has 2nd Vespers
        if not today_result.primary.rank.has_second_vespers:
            # Use tomorrow's 1st Vespers
            return OfficeResult(
                primary=tomorrow_result.primary,
                vespers_type='first',
                commemorations=tomorrow_result.commemorations
            )

        # Both have vespers - apply vespers precedence rules
        vespers_rules = self._get_vespers_rules()

        for rule in vespers_rules:
            if rule.matches(today_result.primary, tomorrow_result.primary, self.date):
                choice = rule.apply()

                if choice.vespers_type == 'first':
                    return OfficeResult(
                        primary=tomorrow_result.primary,
                        vespers_type='first',
                        commemorations=[today_result.primary] if choice.commemorate else []
                    )
                elif choice.vespers_type == 'second':
                    return OfficeResult(
                        primary=today_result.primary,
                        vespers_type='second',
                        commemorations=[tomorrow_result.primary] if choice.commemorate else []
                    )
                else:  # 'both_a_capitulo'
                    return OfficeResult(
                        primary=tomorrow_result.primary,
                        vespers_type='both',
                        commemorations=[today_result.primary]
                    )

        # Default: higher rank wins
        if tomorrow_result.primary.rank.numeric > today_result.primary.rank.numeric:
            return OfficeResult(
                primary=tomorrow_result.primary,
                vespers_type='first',
                commemorations=[today_result.primary]
            )
        else:
            return OfficeResult(
                primary=today_result.primary,
                vespers_type='second',
                commemorations=[tomorrow_result.primary]
            )
```

### 2.2 Version-Specific Rule Strategies

```python
class RuleStrategy:
    """Abstract base for version-specific rule strategies"""

    def adjust_rank_for_comparison(self, office: Office, context: Context) -> float:
        """Version-specific rank adjustments ('flattening')"""
        raise NotImplementedError

    def check_commemoration_allowed(
        self,
        winner: Office,
        candidate: Office,
        hour: str
    ) -> bool:
        """Version-specific commemoration rules"""
        raise NotImplementedError

class Tridentine1570Strategy(RuleStrategy):
    """Pre-Divino Afflatu rules with extensive flattening"""

    def adjust_rank_for_comparison(self, office: Office, context: Context) -> float:
        rank = office.rank.numeric

        # Flatten many ranks to 2.0 (Semiduplex level)
        if rank < 2.9 and not (rank == 2.1 and 'infra Octavam' not in office.rank.name):
            return 2.0

        # Flatten Double range
        if (3.0 <= rank < 3.9) or (4.1 <= rank < 4.9):
            if rank not in [3.9, 3.2]:
                return 3.0

        return rank

class Rubrics1960Strategy(RuleStrategy):
    """Post-1960 simplified rules"""

    def check_commemoration_allowed(
        self,
        winner: Office,
        candidate: Office,
        hour: str
    ) -> bool:
        # 1960: Much stricter commemoration rules

        if winner.rank.is_sunday:
            # On Sundays at hours other than Vespers/Completorium
            if hour not in ['vespers', 'completorium']:
                if candidate.rank.numeric >= 5:
                    return True
                if candidate.rank.numeric >= 6:
                    return True

            # At Lauds
            if hour == 'laudes' and candidate.rank.numeric >= 5 and winner.rank.numeric < 6:
                return True

        # Duplex I classis feasts
        elif candidate.rank.numeric >= 6:
            return True

        # Lesser feasts: Laudes only
        elif candidate.rank.numeric > 1:
            return 'laudes_only'

        return False

# Strategy registry
STRATEGIES = {
    'tridentine': Tridentine1570Strategy(),
    'divino_afflatu': DivinoAfflatuStrategy(),
    '1960': Rubrics1960Strategy(),
    'cistercian': CistercianStrategy(),
}
```

### 2.3 Transfer Resolution

```python
class TransferResolver:
    def __init__(self, version: Version, year: int):
        self.version = version
        self.year = year
        self.easter_date = calculate_easter(year)
        self.easter_letter = self._calculate_easter_letter()
        self._load_transfer_tables()

    def _calculate_easter_letter(self) -> str:
        """Calculate Easter letter (a-g) based on Easter date"""
        # Easter letter depends on relationship between Easter and calendar
        # Algorithm from Directorium.pm
        base_date = date(self.year, 3, 21)
        days_offset = (self.easter_date - base_date).days
        return chr(ord('a') + (days_offset % 7))

    def get_transfer_for_date(self, month: int, day: int) -> Optional[Office]:
        """Check if office on this date has been transferred"""

        # Query transfer_rules table
        transfers = TransferRule.query.filter(
            TransferRule.version_id == self.version.id,
            TransferRule.source_month == month,
            TransferRule.source_day == day
        ).filter(
            # Match Easter conditions
            (TransferRule.easter_letter == self.easter_letter) |
            (TransferRule.easter_month == self.easter_date.month and
             TransferRule.easter_day == self.easter_date.day) |
            (TransferRule.trigger_type == 'fixed_date')
        ).all()

        # Return the destination office if transfer applies
        for transfer in transfers:
            if self._check_transfer_conditions(transfer):
                return transfer.dest_office_id

        return None

    def get_transferred_to_date(self, month: int, day: int) -> List[Office]:
        """Check if any offices have been transferred TO this date"""

        transfers = TransferRule.query.filter(
            TransferRule.version_id == self.version.id,
            TransferRule.dest_month == month,
            TransferRule.dest_day == day
        ).filter(
            # Match Easter conditions
            (TransferRule.easter_letter == self.easter_letter) |
            (TransferRule.easter_month == self.easter_date.month and
             TransferRule.easter_day == self.easter_date.day)
        ).all()

        transferred_offices = []
        for transfer in transfers:
            if self._check_transfer_conditions(transfer):
                transferred_offices.append(transfer.source_office_id)

        return transferred_offices
```

---

## Part 3: Configuration-Driven Rules

### 3.1 Rule Configuration Format (YAML/JSON)

```yaml
# config/versions/1960.yaml

version:
  code: "1960"
  name: "Rubrics 1960"
  year: 1960
  parent: "1955"

parameters:
  # Vespers rules
  min_rank_first_vespers: 6.0
  min_rank_first_vespers_feast_of_lord_on_sunday: 5.0
  min_rank_second_vespers: 2.0

  # Commemoration
  commemoration_strategy: "strict"
  max_commemorations: 1

  # Octaves
  suppress_common_octaves: true
  privileged_octaves_only: true

  # Sundays
  sunday_always_privileged: true

  # Special rules
  sanctoral_saturday_enabled: true
  sanctoral_saturday_min_rank: 1.4

rank_flattening:
  enabled: false  # 1960 doesn't use flattening

concurrence_rules:
  - priority: 1
    name: "Duplex I classis feast of Lord beats Duplex II classis Sunday"
    conditions:
      office1:
        type: "sanctoral"
        min_rank: 6.0
        is_feast_of_lord: true
      office2:
        type: "temporal"
        max_rank: 5.0
        is_sunday: true
    result:
      winner: "office1"
      commemorate: false

  - priority: 2
    name: "Duplex II classis feast of Lord beats Duplex II classis Sunday"
    conditions:
      office1:
        type: "sanctoral"
        min_rank: 5.0
        max_rank: 5.99
        is_feast_of_lord: true
      office2:
        type: "temporal"
        max_rank: 5.0
        is_sunday: true
    result:
      winner: "office1"
      commemorate: false

commemoration_rules:
  - canonical_hour: "all_except_vespers"
    conditions:
      winner:
        is_sunday: true
        max_rank: 5.99
      candidate:
        type: "sanctoral"
        min_rank: 5.0
    result:
      commemorated: true
      type: "full"

  - canonical_hour: "laudes"
    conditions:
      winner:
        is_sunday: true
        max_rank: 5.99
      candidate:
        type: "sanctoral"
        min_rank: 5.0
        max_rank: 5.99
    result:
      commemorated: true
      type: "laudes_only"

  - canonical_hour: "any"
    conditions:
      candidate:
        max_rank: 1.0
    result:
      commemorated: false
      type: "none"

vespers_rules:
  - priority: 1
    name: "No first Vespers for offices below Duplex I classis"
    conditions:
      tomorrow:
        max_rank: 5.99
    result:
      suppress_first_vespers: true

  - priority: 2
    name: "Duplex I classis feast of Lord on Sunday has first Vespers"
    conditions:
      tomorrow:
        min_rank: 5.0
        is_feast_of_lord: true
        day_of_week: 0  # Sunday
    result:
      suppress_first_vespers: false

  - priority: 10
    name: "Standard vespers precedence by rank"
    conditions: {}  # Default rule
    result:
      higher_rank_wins: true
      commemorate_lower: true
```

### 3.2 Loading Configuration

```python
class VersionConfig:
    def __init__(self, version_code: str):
        self.config = self._load_config(version_code)
        self.rules = self._compile_rules()

    def _load_config(self, version_code: str) -> dict:
        """Load YAML configuration with inheritance"""
        config_path = f"config/versions/{version_code}.yaml"
        config = yaml.safe_load(open(config_path))

        # Load parent config if exists
        if 'parent' in config['version']:
            parent_config = self._load_config(config['version']['parent'])
            config = self._merge_configs(parent_config, config)

        return config

    def _compile_rules(self) -> CompiledRules:
        """Compile rules into efficient format"""
        return CompiledRules(
            concurrence=self._compile_concurrence_rules(),
            commemoration=self._compile_commemoration_rules(),
            vespers=self._compile_vespers_rules()
        )

    def get_parameter(self, key: str, default=None):
        """Get configuration parameter"""
        return self.config.get('parameters', {}).get(key, default)
```

---

## Part 4: Advantages of This Model

### 4.1 Separation of Concerns

✅ **Database**: Holds declarative data (offices, ranks, calendars)
✅ **Rule Engine**: Implements complex procedural logic
✅ **Configuration**: Version-specific parameters easily modified
✅ **Code**: Algorithms separate from data

### 4.2 Testability

```python
# Easy to write unit tests
def test_1960_feast_of_lord_beats_sunday():
    engine = PrecedenceEngine(version='1960', date=date(2025, 3, 23))

    # Mock offices
    sanctoral = Office(
        key='03-25',
        name='Annunciation',
        rank=Rank(numeric=5.0, is_feast_of_lord=True)
    )
    temporal = Office(
        key='Quad4-0',
        name='Passion Sunday',
        rank=Rank(numeric=5.0, is_sunday=True)
    )

    winner = engine._resolve_concurrence(temporal, [sanctoral], 'matins')

    assert winner == sanctoral  # Feast of Lord wins
```

### 4.3 Extensibility

- ✅ Add new versions by creating config files
- ✅ Override specific rules without touching core code
- ✅ A/B test rule variations
- ✅ Support experimental rubrics

### 4.4 Query Capabilities

```sql
-- Find all Duplex I classis feasts in 1960 calendar
SELECT o.name_latin, r.rank_numeric
FROM offices o
JOIN ranks r ON o.id = r.office_id
JOIN versions v ON r.version_id = v.id
WHERE v.version_code = '1960'
  AND r.rank_numeric >= 6.0
  AND o.office_type = 'sanctoral'
ORDER BY r.rank_numeric DESC;

-- Find all offices that have first Vespers
SELECT o.name_latin
FROM offices o
JOIN ranks r ON o.id = r.office_id
WHERE r.has_first_vespers = true;

-- Find all transfers for Easter on March 25
SELECT tr.source_month, tr.source_day,
       o1.name_latin as source_name,
       tr.dest_month, tr.dest_day,
       o2.name_latin as dest_name
FROM transfer_rules tr
JOIN offices o1 ON tr.source_office_id = o1.id
JOIN offices o2 ON tr.dest_office_id = o2.id
WHERE tr.easter_month = 3 AND tr.easter_day = 25;
```

### 4.5 Migration Path

**Phase 1**: Build database schema, populate from existing text files
**Phase 2**: Implement rule engine alongside Perl code
**Phase 3**: Validate outputs match
**Phase 4**: Gradually replace Perl with Python
**Phase 5**: Deprecate old system

---

## Part 5: Alternative Approaches Considered

### 5.1 Pure Rule-Based System (Drools/Business Rules)

**Pros:**
- Declarative rules easy to read
- Non-programmers can edit rules

**Cons:**
- ❌ Performance overhead
- ❌ Steep learning curve for maintainers
- ❌ Debugging difficulty
- ❌ May not handle complexity well

**Verdict**: Too heavyweight for this use case

### 5.2 Graph Database (Neo4j)

**Pros:**
- Natural for relationships (commemorations, transfers)
- Good for querying relationships

**Cons:**
- ❌ Overkill for mostly tree-like hierarchy
- ❌ Additional infrastructure complexity
- ❌ Less familiar to developers

**Verdict**: Not worth the complexity

### 5.3 Pure Procedural (All Logic in Code)

**Pros:**
- Simple, no database needed
- Fast execution

**Cons:**
- ❌ Hard to modify rules without code changes
- ❌ Version differences buried in if/else chains
- ❌ Difficult to query/analyze
- ❌ No data validation

**Verdict**: Current Perl approach - works but not ideal for TEI migration

### 5.4 Document Database (MongoDB)

**Pros:**
- Flexible schema
- JSON-like documents natural for TEI

**Cons:**
- ❌ Weak support for complex queries
- ❌ No referential integrity
- ❌ Rank comparisons harder than SQL

**Verdict**: Not suited for hierarchical rank comparisons

---

## Part 6: Recommended Implementation Stack

### Technology Choices

**Database**: PostgreSQL
- ✅ JSONB for flexible parameters
- ✅ Strong relational integrity
- ✅ Excellent query performance
- ✅ Full-text search for office names

**ORM**: SQLAlchemy (Python)
- ✅ Mature, well-documented
- ✅ Good migration support (Alembic)
- ✅ Flexible querying

**Rule Engine**: Custom Python classes
- ✅ Full control over logic
- ✅ Testable
- ✅ Debuggable
- ✅ Performance-tunable

**Configuration**: YAML files + database
- ✅ Human-readable
- ✅ Version control friendly
- ✅ Can override with database for admin UI

**Caching**: Redis
- ✅ Cache computed offices
- ✅ Key: (version, date, hour) → office result
- ✅ Invalidate on data changes

### Performance Optimizations

1. **Eager loading**: Load ranks with offices
2. **Index optimization**: Indexes on rank_numeric, version_id, dates
3. **Caching**: Redis cache for computed results
4. **Materialized views**: Pre-compute common queries
5. **Connection pooling**: Reuse database connections

---

## Conclusion

The recommended **Hybrid Model** (database schema + rule engine + configuration) provides:

✅ **Separation of data and logic**
✅ **Version-specific flexibility**
✅ **Testability and maintainability**
✅ **Query capabilities for analysis**
✅ **Extensibility for new rubrics**
✅ **Performance through caching**
✅ **Migration path from existing system**

This approach respects the complexity of liturgical precedence while creating a maintainable, modern system suitable for TEI integration and long-term evolution.

---

**Document Version**: 1.0
**Last Updated**: 2025-12-28
**Author**: Claude (Sonnet 4.5)
**For**: Divinum Officium Knowledge Base
