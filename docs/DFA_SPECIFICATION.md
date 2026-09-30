# DFA Specification

## 1. Overview

This document defines the Deterministic Finite Automaton (DFA) obtained by
applying the subset construction to the ε-NFA in NFA_SPECIFICATION.md.

The DFA removes all nondeterminism: the ε-branch at q0 is resolved by placing
both branch starts into the start subset, and every DFA state is a set of NFA
states. After each input symbol, exactly one DFA transition is possible.

Source: NFA-to-DFA conversion (Garcia). Verified against all 2,880 accepted
strings of L_TIME.

---

## 2. Formal Definition

The DFA is the 5-tuple M = (Q, Σ, δ, S0, F):

- Q = {S0, S1, ..., S15, ∅} (17 states, including the dead state ∅)
- Σ = {0,1,2,3,4,5,6,7,8,9, :, ␣, A, M, P} (15 symbols; ␣ = one literal space)
- δ : Q × Σ → Q (total function; every missing entry in the table goes to ∅)
- S0 = start state
- F = {S10, S11, S15} (accepting states)

---

## 3. Subset Construction: State Meanings

Each DFA state is a subset of NFA states. The meaning column explains what
the machine "knows" at that point.

| DFA State | NFA Subset | Meaning |
|---|---|---|
| S0 | {q0, q1, q8} | Start; nothing read yet; both branches alive via ε |
| S1 | {q2, q9} | First hour digit 0; 24-hour 00-09 or 12-hour 01-09 |
| S2 | {q2, q10} | First hour digit 1; 24-hour 10-19 or 12-hour 10-12 |
| S3 | {q3} | First hour digit 2; 24-hour only (20-23) |
| S4 | {q4} | Hour complete; 24-hour only; waiting for colon |
| S5 | {q4, q11} | Hour complete; still ambiguous (24-hour or 12-hour) |
| S6 | {q5} | Colon read; 24-hour only; waiting for minute tens |
| S7 | {q5, q12} | Colon read; ambiguous; waiting for minute tens |
| S8 | {q6} | Minute tens valid; 24-hour only |
| S9 | {q6, q13} | Minute tens valid; ambiguous |
| S10 | {q7} | ACCEPTING: complete 24-hour time |
| S11 | {q7, q14} | ACCEPTING: complete 24-hour time, and 12-hour HH:MM waiting for space + meridiem |
| S12 | {q15} | Space read after 12-hour HH:MM; waiting for A or P |
| S13 | {q16} | Letter A read; waiting for M |
| S14 | {q17} | Letter P read; waiting for M |
| S15 | {q18} | ACCEPTING: complete 12-hour time |
| ∅ | {} | Dead state; trap; no accepting path remains |

---

## 4. Transition Table

Legend: → start; * accepting; ∅ dead state. All entries not shown go to ∅.
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
| S8 | S10 | S10 | S10 | S10 | S10 | S10 | ∅ | ∅ | ∅ |  | ∅ |
| S9 | S11 | S11 | S11 | S11 | S11 | S11 | ∅ | ∅ | ∅ | ∅ | ∅ |
| *S10 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| *S11 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | S12 | ∅ | ∅ | ∅ |
| S12 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | S13 | S14 | ∅ |
| S13 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | S15 |
| S14 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | S15 |
| *S15 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |

---

## 5. Acceptance and Dead State Behavior

A string is accepted if, after consuming the entire input, the DFA is in
S10, S11, or S15.

The dead state ∅ is a trap: every symbol keeps it in ∅. Any structural
violation (invalid hour digit, minute tens 6-9, missing colon, missing
space, wrong meridiem letter, extra trailing symbols) leads to ∅.

Note on S11: it is accepting because the input so far is a complete
24-hour time. If more input arrives (a space), the machine continues toward
the 12-hour completion at S15. Any symbol other than ␣ at S11 goes to ∅,
which correctly rejects inputs like `09:30AM`.

---

## 6. Example Traces

### Accepted: 23:45
S0 -2-> S3 -3-> S4 -:-> S6 -4-> S8 -5-> S10 (accept)

### Accepted: 09:30 AM
S0 -0-> S1 -9-> S5 -:-> S7 -3-> S9 -0-> S11 -␣-> S12 -A-> S13 -M-> S15 (accept)

### Accepted: 12:00
S0 -1-> S2 -2-> S5 -:-> S7 -0-> S9 -0-> S11 (accept)

### Rejected: 13:30 PM
S0 -1-> S2 -3-> S4 -:-> S6 -3-> S8 -0-> S10 -␣-> ∅ (dead; 24-hour time
cannot take a meridiem)

### Rejected: 12:60
S0 -1-> S2 -2-> S5 -:-> S7 -6-> ∅ (minute tens must be 0-5)

### Rejected: 09:30AM
... -0-> S11 -A-> ∅ (missing required single space)

---

## 7. Equivalence Check

The DFA accepts exactly the same language as the NFA and the regular
expression: 2,880 strings (1,440 from L24 and 1,440 from L12). This count
was verified by exhaustive enumeration during the conversion.

---

## 8. Handoff to DFA Minimization

Two pairs of equivalent states are candidates for merging:

- S10 ≡ S15: both accepting; all 15 symbols go to ∅.
- S13 ≡ S14: both non-accepting; M goes to S15; all other symbols go to ∅.

No other merges are possible. In particular:

- S11 is distinguishable from S10/S15 because ␣ goes to S12, not ∅.
- S6 is distinguishable from S7 because they lead to S8 and S9, which lead
  to the distinguishable accepting states S10 and S11.

Merging the two pairs yields the 15-state minimized DFA
(MINIMIZED_DFA_SPECIFICATION.md).

---

## 9. Machine-Readable and Diagram Files

- `data/dfa.json`: structured transition table for the simulator. Missing
  transitions default to the dead state. The symbol key "SPACE" represents
  one literal space character.
- `diagrams/dfa.dot`: Graphviz source, horizontal orientation (rankdir=LR).
  Undefined transitions are not drawn; they all lead to the dead state.