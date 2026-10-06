# System Overview

## Project Name

Smart Time Format Validator with Automata Trace and Formal Language Explanation

## Purpose

This system validates time strings in 12-hour and 24-hour formats and
demonstrates how the validation problem is modeled using Automata Theory:
formal language specification, regular expression, NFA, DFA, NFA-to-DFA
conversion, DFA minimization, step-by-step simulation, and acceptance or
rejection explanation.

## Project Context

University Automata Theory project (CCAUTOMA / COM241, Group Chicken Wings).

The team papers define the formal artifacts (language analysis, RE/NFA,
DFA conversion, minimization). This document defines the software system
that simulates and presents those artifacts.

---

## Core Idea: Two-Layer Pattern Recognition

The system uses two layers.

### Layer 1 - Formal Layer

- Validates the RAW input against the strict formal language.
- Performs the Alphabet Check on raw input.
- Runs the DFA on raw input only if the alphabet check passes.
- Its results match the team papers exactly.

### Layer 2 - Lexical Normalization Layer

- A documented system extension for human-friendly input.
- Applies exactly two rules (see Normalization Rules).
- Runs the same Alphabet Check and same DFA on the normalized string.
- Its trace is displayed on the normalized string.

The GUI always displays BOTH layers side by side, so the mathematics is
never hidden.

---

## Scope

### In Scope

1. Validate 24-hour format `HH:MM` (00-23, 00-59).
2. Validate 12-hour format `HH:MM AM` / `HH:MM PM` (01-12, 00-59).
3. Layer 1 alphabet check and DFA result on raw input.
4. Layer 2 normalization (two rules only) and DFA result on normalized input.
5. Dual-layer GUI display.
6. Formal language, regex, NFA, DFA, minimized DFA artifacts.
7. Step-by-step trace.
8. Rejection reasons with layer classification and suggestions.
9. Sample test cases.

### Out of Scope

1. Seconds, dates, time zones, locales.
2. Natural language parsing.
3. Arbitrary regex validation.
4. Lowercase or spacing fixes beyond the two normalization rules.
5. Persistent storage, authentication, deployment infrastructure.

---

## Accepted Formats (Strict, Canonical)

### 24-Hour

```text
HH:MM    HH = 00-23, MM = 00-59
```

Examples: `00:00`, `09:30`, `12:49`, `23:59`

### 12-Hour

```text
HH:MM AM | HH:MM PM
HH = 01-12 (two digits mandatory), MM = 00-59,
exactly one space before uppercase AM/PM
```

Examples: `01:05 AM`, `09:30 PM`, `12:49 AM`, `12:00 PM`

---

## Formal Language

Alphabet (15 symbols):

```text
Σ_TIME = {0,1,2,3,4,5,6,7,8,9, :, ␣, A, M, P}
```

Language:

```text
L_TIME = L24 ∪ L12   (no mode selection)
L24 = { h ":" m | h = 00-23, m = 00-59 }
L12 = { h ":" m ␣ r | h = 01-12, m = 00-59, r ∈ {AM, PM} }
```

Formal regular expression:

```text
R24 = ((0+1)D + 2(0+1+2+3)) : (0+1+2+3+4+5)D
R12 = (0(1+...+9) + 1(0+1+2)) : (0+1+2+3+4+5)D ␣ (AM+PM)
R_TIME = R24 + R12
```

Programming regex (implementation reference):

```text
^((([01][0-9]|2[0-3]):[0-5][0-9])|((0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)))$
```

Artifact sizes (frozen): NFA 19 states (q0-q18, F={q7,q18});
DFA 17 states (S0-S15 + ∅, F={S10,S11,S15});
minimized DFA 15 states (merges S10≡S15, S13≡S14);
exactly 2,880 accepted strings.

---

## Normalization Rules (Layer 2 Only)

Exactly two rules, nothing more:

- N1: Case-fold a trailing meridiem token (am/pm/Am/pM → AM/PM).
- N2: Pad a one-digit hour with one leading zero (9 → 09).

NOT normalized (rejected in both layers): missing space (`09:30AM`),
double spaces, seconds, symbols outside Σ_TIME, out-of-range values.

---

## System Behavior

### Accepted Input

Shows: ACCEPTED, raw input, normalized input (if different), detected
format, formal language, regex, NFA, DFA, minimized DFA, successful trace.

### Rejected Input

Shows: REJECTED, rejection layer (Alphabet Check or Automaton Dead State),
failure position, expected symbols, suggestion (UX only, never affects
acceptance), all formal artifacts, failed trace.

### Behavior Matrix (source of truth for GUI and tests)

| Raw input | Layer 1 (formal, raw) | Layer 2 (normalized) |
|---|---|---|
| `9:30 am` | REJECTED - Alphabet Check | `09:30 AM` → ACCEPTED |
| `09:30 am` | REJECTED - Alphabet Check | `09:30 AM` → ACCEPTED |
| `9:30 AM` | REJECTED - Dead State | `09:30 AM` → ACCEPTED |
| `09:30AM` | REJECTED - Dead State | unchanged → REJECTED |
| `09:30  AM` | REJECTED - Dead State | unchanged → REJECTED |
| `00:30 AM` | REJECTED - Dead State | unchanged → REJECTED |
| `13:30 PM` | REJECTED - Dead State | unchanged → REJECTED |
| `ab:cd` | REJECTED - Alphabet Check | unchanged → REJECTED |
| `23:45` | ACCEPTED | unchanged → ACCEPTED |

---

## Architecture

```text
Raw Input
   |
   +---------------------------+
   |                           |
   v                           v
Layer 1: Formal           Layer 2: Normalization
Alphabet Check (raw)      Apply N1 + N2
   |                           |
   v                           v
DFA on raw              Alphabet Check (normalized)
   |                           |
   v                           v
Formal Result           DFA on normalized
                               |
                               v
                        Normalized Result + Trace
   |                           |
   +-------------+-------------+
                 v
        GUI Dual-Layer Display
```

### Component Responsibilities

| Component | Responsibility |
|---|---|
| `app.py` | Streamlit entry point |
| `core/alphabet_check.py` | Σ_TIME membership check (both layers) |
| `core/normalizer.py` | N1 and N2 only |
| `core/automaton.py` | Minimized DFA table and validation |
| `core/trace.py` | Step-by-step trace builder |
| `core/diagnostics.py` | Rejection layer, position, expected symbols, suggestion |
| `core/samples.py` | Sample inputs |
| `artifacts/formal_language.py` | Formal language content for GUI |
| `artifacts/regex_artifacts.py` | Regular expression content for GUI |
| `artifacts/nfa_artifacts.py` | NFA content for GUI |
| `artifacts/dfa_artifacts.py` | DFA content for GUI |
| `artifacts/minimized_dfa_artifacts.py` | Minimized DFA content for GUI |
| `data/*.json`, `diagrams/*.dot` | Optional artifact data and diagram sources |
| `ui/*.py` | Tabs and layout |

---

## GUI Structure

### Summary Tab (dual-layer display)

Raw input; Layer 1 result with rejection layer; normalized form;
Layer 2 result; detected format; short explanation.

### Formal Language Tab

Alphabet, language definition, regex, accepted and rejected examples.

### Automata Tab

NFA, DFA, minimized DFA artifacts; transition tables; start and accepting
states; optional diagrams.

### Trace Tab

Layer 2 trace on the normalized string; Layer 1 trace when raw input
passes the alphabet check; failure point highlighted when rejected.

### Test Cases Tab

Behavior matrix samples with expected results and explanations.

---

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| GUI | Streamlit |
| Documentation | Markdown |
| Automaton data | Python dictionaries or JSON |
| Diagrams | Graphviz or static images (optional) |
| Testing | pytest |

Rationale: fast development, simple demo, low overhead, boring technology
that solves the problem.

---

## Testing Strategy

1. Unit tests: `test_alphabet_check.py`, `test_normalizer.py` (N1/N2 only),
   `test_automaton.py`, `test_trace.py`, `test_samples.py`.
2. Behavior matrix cases must pass in both layers.
3. Boundary cases: `00:00`, `12:00`, `12:00 AM`, `12:00 PM`, `23:59`,
   `00:00 AM`, `13:00 PM`.
4. Stretch: enumerate all 2,880 accepted strings and verify the DFA count.

---

## Assumptions

1. The team papers are the source of truth for Layer 1.
2. Normalization is documented only in system docs, never in the papers.
3. Static NFA/DFA/minimized DFA artifacts are acceptable for the demo.
4. Transition tables are acceptable if diagram generation is too slow.

## Constraints

1. One to two days total.
2. One developer implements the system; papers are team deliverables.
3. The system must stay explainable; no scope creep.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Automaton construction delays | Use frozen precomputed artifacts |
| GUI delays | Streamlit tabs, tables first, diagrams later |
| Papers vs system contradiction | Two-layer display + DOC_TEAM_TWO_LAYER_GUIDE |
| Scope creep | Out-of-scope list enforced |

---

## Decision Record: Two-Layer Input Handling

- Context: Panel may ask why human-valid inputs like `9:30 am` are rejected
  by the formal language.
- Options: (A) expand the formal language - rejected, state explosion and
  invalidates finished artifacts; (B) silent normalization - rejected, makes
  paper statements false; (C) strict formal layer plus separate lexical
  normalization layer with dual-layer display - approved.
- Tradeoffs: Slightly more GUI complexity; papers stay mathematically pure.
- Consequences: Papers unchanged; normalization lives only in system docs;
  GUI shows both results.

---

## Success Criteria and Definition of Done

1. Layer 1 results match the papers exactly.
2. Layer 2 accepts `9:30 am`-style human variants via N1/N2.
3. All artifacts and traces display correctly.
4. Rejection reasons state layer, position, expected symbols, suggestion.
5. All behavior matrix tests pass.
6. System is stable and explainable for the live demo.

## Related Documents

- `docs/PHASE_ROADMAP.md`
- `docs/DOC_TEAM_TWO_LAYER_GUIDE.md`
- `docs/FORMAL_SPECIFICATION.md` (Phase 1)
- `docs/REGULAR_EXPRESSION.md` (Phase 2)
- `docs/NFA_SPECIFICATION.md`, `DFA_SPECIFICATION.md`,
  `MINIMIZED_DFA_SPECIFICATION.md` (Phases 3-5)
- `docs/TEST_PLAN.md`, `docs/DEMO_SCRIPT.md` (Phase 8)