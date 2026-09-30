# Documentation Team Guide: Two-Layer Architecture Policy

Project: Time Format Validator
Group: Chicken Wings — CCAUTOMA / COM241
Status: FINAL DECISION — applies to all remaining documentation work

---

## 1. Purpose

This guide coordinates all remaining documentation work under the approved
two-layer system design. It tells every documentation owner:

1. What to edit.
2. What NOT to edit.
3. What to watch out for so the papers, the final compilation, and the
   simulator never contradict each other.

Your existing revision briefs remain valid (Mae: 6 areas; Markie: 8 sections).
This guide adds constraints on top of them. It does not replace them.

---

## 2. The Approved Decision (Decision Record)

- Context: The panel may ask, "What if the user inputs 9:30 am? Humans consider
  that valid."
- Option A (rejected): Expand the formal language to accept lowercase and
  single-digit hours. Causes state explosion, invalidates the finished NFA,
  DFA conversion, minimization, and the 2,880-string equivalence check.
- Option B (rejected): Silently normalize input in the simulator. Makes several
  paper sentences false (for example, Garcia §11 and the Alphabet Check rows).
- Option C (approved): Keep the formal layer strict. Add a separate lexical
  normalization layer in the system. The GUI displays BOTH results
  (dual-layer display).

Consequences:

- The papers describe Layer 1 only and stay mathematically strict.
- Normalization is documented ONLY in `docs/System_Overview.md`, never inside
  the individual papers.
- The GUI shows the formal result on the raw input and the result on the
  normalized input, side by side.

---

## 3. The Two Layers (Everyone Must Memorize This)

### Layer 1 — Formal Layer (what the papers describe)

- Alphabet: Σ_TIME = {0–9, :, ␣, A, M, P} (15 symbols, uppercase only).
- Language: L_TIME = L24 ∪ L12, no mode selection.
- Strict two-digit hours in both formats.
- Exactly one space before uppercase AM/PM.
- Rejection layers: Alphabet Check vs Automaton (Dead State).
- Artifacts: 19-state NFA, 17-state DFA, 15-state minimized DFA,
  2,880 accepted strings.

### Layer 2 — Lexical Normalization Layer (system extension)

Exactly two rules, nothing more:

- N1: Case-fold a trailing meridiem token (am / pm / Am / pM → AM / PM).
- N2: Pad a one-digit hour with one leading zero (9 → 09).

NOT normalized (rejected in both layers): missing space (`09:30AM`),
double spaces, seconds, symbols outside Σ_TIME, invalid hours/minutes.

---

## 4. Golden Rules (All Documentation Owners)

1. The mathematics is FROZEN. No changes to Σ_TIME, R_TIME, the NFA table,
   the DFA table, the minimization, the traces, or the 2,880 count.
2. The papers NEVER mention normalization, lowercase acceptance, or
   hour padding.
3. The system docs NEVER claim the papers accept non-canonical input.
4. Fixed terminology only: "Alphabet Check", "Automaton (Dead State)",
   "canonical form", "lexical normalization layer", "Layer 1 / Layer 2".
5. Never renumber or rename states (q0–q18, S0–S15, ∅) or counts
   (19 / 17 / 15 / 2,880).

---

## 5. Per-Owner Tasks and Watchouts

### Mae Santos (RE / NFA Designer)

Edits (from your existing brief):

- [ ] Add the formal algebraic regular expression (R24, R12).
- [ ] Fix the q8 callout text to "12-Hour / Standard: 01:00–12:59 (AM or PM)".
- [ ] Standardize accepting markers and set notation in the NFA table.
- [ ] Add the Rejection Layer column to the rejected strings table.
- [ ] Re-export the NFA diagram in landscape orientation.
- [ ] Fix typographical errors.

Watchouts:

- Do NOT add lowercase symbols or optional-zero branches to R_TIME or the NFA.
- KEEP the `09:30 am` row as an Alphabet Check rejection. It is true for
  Layer 1.
- KEEP the phrase "rejected before automaton execution".

### Markie Mojica (Language Analyst)

Edits (from your existing brief):

- [ ] Remove all mode-selection wording.
- [ ] Introduce Σ_TIME formally after set D.
- [ ] State Σ24 ⊂ Σ_TIME and Σ12 = Σ_TIME.
- [ ] Add Rejection Layer columns to §4.6 and §5.6.
- [ ] Replace the boundary table with the 5-column version.
- [ ] Apply the §8 and §9 handoff rewording.

Watchouts:

- Σ_TIME stays at exactly 15 symbols.
- KEEP the §9 wording "perform an initial alphabet validation against
  Σ_TIME ... before executing the DFA transitions". The GUI's Layer 1 does
  exactly this on raw input.

### Antonio Garcia (DFA Designer)

Edits: NONE. The document is complete and verified.

Watchouts:

- Do NOT reword §11 ("...rejected by the simulator's alphabet check before
  the DFA runs"). It is true for Layer 1.
- Do NOT reword the §12 handoff.

### Automata Optimizer

- [ ] Confirm merges S10 ≡ S15 and S13 ≡ S14.
- [ ] Publish the 15-state minimized DFA.

Watchout: normalization does not change the minimization input or result.

### Programmer (for reference)

- GUI displays Layer 1 result (raw input) and Layer 2 result (normalized
  input) with the trace run on the normalized string.
- Normalization is documented only in `docs/System_Overview.md`.

---

## 6. Behavior Matrix (Verify Your Tables Against This)

| Raw input | Layer 1 (formal, raw) | Layer 2 (normalized) | Paper reference |
|---|---|---|---|
| `9:30 am` | REJECTED — Alphabet Check | `09:30 AM` → ACCEPTED | Mae §4 / Markie §5.6 |
| `09:30 am` | REJECTED — Alphabet Check | `09:30 AM` → ACCEPTED | Mae §4 / Markie §5.6 |
| `9:30 AM` | REJECTED — Dead State | `09:30 AM` → ACCEPTED | Mae §4 |
| `09:30AM` | REJECTED — Dead State | unchanged → REJECTED | Mae §4 |
| `09:30  AM` | REJECTED — Dead State | unchanged → REJECTED | Mae §4 |
| `00:30 AM` | REJECTED — Dead State | unchanged → REJECTED | Garcia §10 |
| `13:30 PM` | REJECTED — Dead State | unchanged → REJECTED | Garcia §10 |
| `ab:cd` | REJECTED — Alphabet Check | unchanged → REJECTED | Markie §4.6 / §5.6 |
| `23:45` | ACCEPTED | unchanged → ACCEPTED | Garcia §10 |

If any paper table disagrees with this matrix, the table is wrong.
Escalate to the lead before editing.

---

## 7. Optional Standardized Note (Final Compilation ONLY)

If the lead approves mentioning the UX layer in the final compilation, paste
this paragraph ONCE, in the compilation introduction or architecture section.
Do not paraphrase it. Do not place it inside individual papers.

> System Architecture Note (Two-Layer Design). The formal artifacts in this
> compilation describe the canonical language L_TIME over Σ_TIME. The software
> implementation adds a documented lexical normalization layer for user
> convenience only: it case-folds a trailing meridiem token and pads a
> one-digit hour with a leading zero. The interface always displays both the
> formal result on the raw input (Layer 1) and the result on the normalized
> input (Layer 2). All tables, traces, and counts in this compilation refer to
> the formal layer and to canonical input.

---

## 8. Panel Defense Script

Question: "What if the user inputs 9:30 am? It is valid in human sense."

Answer: "Correct, and Layer 1 on screen shows the formal rejection live,
exactly as the papers describe. The papers define the canonical language.
The acceptance you see is a separate, documented lexical normalization layer
that maps human variants to canonical form before the same minimized DFA
runs. Both layers are displayed so the mathematics is never hidden. We kept
the formal language strict to avoid state explosion and to keep the NFA,
DFA, and minimization verifiable."

---

## 9. Pre-Submission Consistency Checklist

- [ ] All brief revisions applied (Mae 6 areas, Markie 8 sections).
- [ ] No mathematics changed beyond the briefs.
- [ ] No mention of normalization inside individual papers.
- [ ] Standardized note added to the final compilation (if approved).
- [ ] Terminology consistent across all papers.
- [ ] State names, subsets, and counts unchanged.
- [ ] Every paper table matches the Behavior Matrix in §6.
- [ ] Demo behavior matches the papers: Layer 1 results equal the paper tables.