# NFA Specification

## 1. Overview

This document defines the ε-NFA that recognizes the combined time language:

L_TIME = L24 ∪ L12

The NFA is constructed directly from the formal regular expression
R_TIME = R24 + R12. The only nondeterminism is the ε-choice at the start
state between the 24-hour branch and the 12-hour branch. After that choice,
both branches read the same HH:MM prefix structure step by step.

This NFA is the exact input used by the NFA-to-DFA conversion
(DFA_SPECIFICATION.md), which verified it against all 2,880 accepted strings.

---

## 2. Formal Definition

The NFA is the 5-tuple M = (Q, Σ, δ, q0, F):

- Q = {q0, q1, ..., q18} (19 states)
- Σ = {0,1,2,3,4,5,6,7,8,9, :, ␣, A, M, P} (15 symbols; ␣ = one literal space)
- δ : Q × (Σ ∪ {ε}) → P(Q) (transition function mapping to the power set of Q)
- q0 = start state
- F = {q7, q18} (accepting states)

---

## 3. Branch Construction

### ε-Branching at q0

From q0, two ε-transitions select a branch without consuming input:

- ε → q1 : enter the 24-hour branch
- ε → q8 : enter the 12-hour branch

### 24-Hour Branch (q1–q7)

- q1: first hour digit. 0,1 → q2 (hours 00–19); 2 → q3 (hours 20–23).
- q2: second hour digit, any 0–9 → q4.
- q3: second hour digit restricted to 0–3 → q4 (enforces 20–23).
- q4: colon ":" → q5.
- q5: first minute digit restricted to 0–5 → q6.
- q6: second minute digit, any 0–9 → q7.
- q7: accepting. Complete 24-hour time.

Branch callout: "24-Hour: 00:00–23:59".

### 12-Hour Branch (q8–q18)

- q8: first hour digit. 0 → q9 (hours 01–09); 1 → q10 (hours 10–12).
- q9: second hour digit restricted to 1–9 → q11 (enforces 01–09).
- q10: second hour digit restricted to 0–2 → q11 (enforces 10–12).
- q11: colon ":" → q12.
- q12: first minute digit restricted to 0–5 → q13.
- q13: second minute digit, any 0–9 → q14.
- q14: exactly one space ␣ → q15.
- q15: meridiem first letter. A → q16; P → q17.
- q16: M → q18 (completes AM).
- q17: M → q18 (completes PM).
- q18: accepting. Complete 12-hour time.

Branch callout (corrected): "12-Hour / Standard: 01:00–12:59 (AM or PM)".

---

## 4. Transition Table

Legend: → marks the start state; * marks an accepting state; ∅ is the empty set.
Grouped columns apply separately to each digit in the range.

| State | ε | 0 | 1 | 2 | 3 | 4–5 | 6–9 | : | ␣ | A | P | M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| → q0 | {q1, q8} | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| q1 | ∅ | {q2} | {q2} | {q3} | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| q2 | ∅ | {q4} | {q4} | {q4} | {q4} | {q4} | {q4} | ∅ | ∅ | ∅ | ∅ | ∅ |
| q3 | ∅ | {q4} | {q4} | {q4} | {q4} | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| q4 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | {q5} | ∅ | ∅ | ∅ | ∅ |
| q5 | ∅ | {q6} | {q6} | {q6} | {q6} | {q6} | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| q6 | ∅ | {q7} | {q7} | {q7} | {q7} | {q7} | {q7} | ∅ | ∅ | ∅ | ∅ | ∅ |
| *q7 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| q8 | ∅ | {q9} | {q10} | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| q9 | ∅ | ∅ | {q11} | {q11} | {q11} | {q11} | {q11} | ∅ | ∅ | ∅ | ∅ | ∅ |
| q10 | ∅ | {q11} | {q11} | {q11} | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| q11 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | {q12} | ∅ | ∅ | ∅ | ∅ |
| q12 | ∅ | {q13} | {q13} | {q13} | {q13} | {q13} | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |
| q13 | ∅ | {q14} | {q14} | {q14} | {q14} | {q14} | {q14} | ∅ | ∅ | ∅ | ∅ | ∅ |
| q14 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | {q15} | ∅ | ∅ | ∅ |
| q15 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | {q16} | {q17} | ∅ |
| q16 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | {q18} |
| q17 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | {q18} |
| *q18 | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ | ∅ |

---

## 5. Acceptance Rule

A string is accepted if, after reading the entire input, at least one of the
possible NFA computations ends in q7 or q18. Because the only ε-moves are at
q0, each input follows at most one branch.

---

## 6. Rejection Behavior

Strings over Σ that violate hour, minute, colon, space, or meridiem structure
have no valid path to q7 or q18. In the equivalent DFA these strings enter the
dead state ∅. Strings containing symbols outside Σ_TIME (for example
lowercase letters) are rejected by the Alphabet Check layer before automaton
execution, as defined in FORMAL_SPECIFICATION.md.

---

## 7. Machine-Readable and Diagram Files

- `data/nfa.json`: structured representation of this NFA for the simulator
  GUI. Note: the symbol key "SPACE" in the JSON represents one literal space
  character; the simulator maps ' ' to "SPACE" before table lookup.
- `diagrams/nfa.dot`: Graphviz source for the state diagram, exported in
  horizontal (landscape) orientation with rankdir=LR.

---

## 8. Equivalence and Handoff

- This NFA recognizes exactly the language of R_TIME (REGULAR_EXPRESSION.md).
- It accepts exactly 2,880 strings (1,440 from L24 and 1,440 from L12),
  as verified by the subset construction in DFA_SPECIFICATION.md.
- This NFA is the input to the NFA-to-DFA conversion. No modifications are
  permitted after this specification; any change requires re-running the
  subset construction and the 2,880-string equivalence check.