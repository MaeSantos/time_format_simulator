# Minimized DFA Specification

## 1. Overview

This document defines the minimized DFA for L_TIME, obtained by applying
partition refinement to the 17-state DFA in DFA_SPECIFICATION.md.

The minimization merges exactly two pairs of equivalent states:

- S15 into S10 (both accepting; every symbol goes to the dead state)
- S14 into S13 (both non-accepting; M goes to the accepting state; all
  other symbols go to the dead state)

Result: 15 states (S0-S13 plus the dead state), 2 accepting states.

This 15-state machine is the one the simulator implements in
core/automaton.py, per the DFA Designer's handoff.

---

## 2. Formal Definition

The minimized DFA is the 5-tuple M = (Q, Σ, δ, S0, F):

- Q = {S0, S1, ..., S13, ∅} (15 states)
- Σ = {0,1,2,3,4,5,6,7,8,9, :, ␣, A, M, P} (15 symbols; ␣ = one literal space)
- δ : Q × Σ → Q (total function; missing entries go to ∅)
- S0 = start state
- F = {S10, S11} (accepting states)

---

## 3. Merge Map and State Meanings

| New State | Old States | Meaning |
|---|---|---|
| S0 | S0 | Start; nothing read |
| S1 | S1 | First hour digit 0 |
| S2 | S2 | First hour digit 1 |
| S3 | S3 | First hour digit 2 (24-hour only) |
| S4 | S4 | Hour complete; 24-hour only |
| S5 | S5 | Hour complete; valid in both formats |
| S6 | S6 | Colon read; 24-hour only |
| S7 | S7 | Colon read; both formats |
| S8 | S8 | Minute tens valid; 24-hour only |
| S9 | S9 | Minute tens valid; both formats |
| S10 | S10 + S15 | ACCEPTING: complete valid time (24-hour or 12-hour) |
| S11 | S11 | ACCEPTING: complete 24-hour time that may continue as 12-hour |
| S12 | S12 | Space read after 12-hour HH:MM; waiting for A or P |
| S13 | S13 + S14 | Meridiem first letter read (A or P); waiting for M |
| ∅ | ∅ | Dead state; trap |

---

## 4. Proof of Minimization (Partition Refinement)

[PENDING: The Automata Optimizer's formal partition-refinement proof will
be inserted here. The 15-state result below is locked and already in use by
the simulator; only the written proof is pending.]

Template for the pending proof:

1. Initial partition P0 = { F, Q \ F } with F = {S10, S11, S15} (pre-merge
   accepting set).
2. Refinement steps showing which blocks split on which symbols.
3. Indistinguishability arguments for the two merged pairs:
   - S10 ≡ S15: both accepting; no continuation is accepted from either.
   - S13 ≡ S14: both accept exactly the continuation "M" and nothing else.
4. Distinguishing strings proving no further merges, for example:
   - S11 vs S10: continuation "␣AM" accepts from S11, dies from S10.
   - S13 vs S10: continuation "M" accepts from S13, dies from S10.
   - S6 vs S7: continuation "00␣AM" accepts from S7, dies from S6.
   - S12 vs ∅: continuation "AM" accepts from S12, dies from ∅.

---

## 5. Transition Table

Legend: → start; * accepting; ∅ dead state. Missing entries go to ∅.
Grouped columns apply separately to each digit in the range.

| State | 0 | 1 | 2 | 3 | 4–5 | 6–9 | : | ␣ | A | P | M |
|---|---|---|---|---|---|---|---|---|---|---|---|
| → S0 | S1 | S2 | S3 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| S1 | S4 | S5 | S5 | S5 | S5 | S5 | ∅ | ∅ | ∅ | ∅ | ∅ |
| S2 | S5 | S5 | S5 | S4 | S4 | S4 | ∅ | ∅ | ∅ | ∅ | ∅ |
| S3 | S4 | S4 | S4 | S4 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| S4 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | S6 | ∅ | ∅ | ∅ | ∅ |
| S5 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | S7 | ∅ | ∅ | ∅ | ∅ |
| S6 | S8 | S8 | S8 | S8 | S8 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| S7 | S9 | S9 | S9 | S9 | S9 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| S8 | S10 | S10 | S10 | S10 | S10 | S10 | ∅ | ∅ | ∅ | ∅ | ∅ |
| S9 | S11 | S11 | S11 | S11 | S11 | S11 | ∅ | ∅ | ∅ | ∅ | ∅ |
| *S10 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| *S11 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | S12 | ∅ | ∅ | ∅ |
| S12 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | S13 | S13 | ∅ |
| S13 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | S10 |
| ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |

---

## 6. Example Traces (Minimized States)

### Accepted: 23:45
S0 -2-> S3 -3-> S4 -:-> S6 -4-> S8 -5-> S10 (accept)

### Accepted: 09:30 AM
S0 -0-> S1 -9-> S5 -:-> S7 -3-> S9 -0-> S11 -␣-> S12 -A-> S13 -M-> S10
(accept; the old S15 endpoint is now the merged S10)

### Accepted: 12:00
S0 -1-> S2 -2-> S5 -:-> S7 -0-> S9 -0-> S11 (accept)

### Rejected: 13:30 PM
S0 -1-> S2 -3-> S4 -:-> S6 -3-> S8 -0-> S10 --> ∅ (dead)

### Rejected: 12:60
S0 -1-> S2 -2-> S5 -:-> S7 -6-> ∅ (minute tens must be 0-5)

### Rejected: 09:30AM
... -0-> S11 -A-> ∅ (missing required single space)

---

## 7. Equivalence

The minimized DFA accepts exactly the same language as the NFA, the regular
expression, and the 17-state DFA: 2,880 strings (1,440 from L24 and 1,440
from L12). Minimization changes the number of states, never the language.

---

## 8. Machine-Readable and Diagram Files

- `data/minimized_dfa.json`: structured transition table used by
  core/automaton.py. Missing transitions default to the dead state. The
  symbol key "SPACE" represents one literal space character.
- `diagrams/minimized_dfa.dot`: Graphviz source, horizontal orientation
  (rankdir=LR). Merged states are labeled with their original names.

---

## 9. Handoff to Programmer

Implement this exact table in core/automaton.py:

1. Run the Alphabet Check first (reject symbols outside Σ_TIME).
2. Map ' ' to "SPACE" before table lookup.
3. Treat missing transitions as moves to the dead state.
4. Accept only if the final state after the full input is S10 or S11.
5. Record every transition for the Trace Tab.