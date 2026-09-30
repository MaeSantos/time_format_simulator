# PHASE_ROADMAP

## Phase 0: Theory, Artifacts, and Project Skeleton

### Objective

Finalize the project scope, establish the two-layer architecture policy, create the base folder skeleton, and complete all formal mathematical artifacts (Language, RE, NFA, DFA, Minimized DFA) and their corresponding data/diagram files.

### Tasks

1. Confirm scope, two-layer normalization policy, GUI layout, and tech stack.
2. Create project folder skeleton and base planning docs (`System_Overview.md`, `DOC_TEAM_TWO_LAYER_GUIDE.md`).
3. Define the Formal Language Specification (Alphabet $\Sigma_{TIME}$, sets, boundary cases).
4. Design the Regular Expression (Formal algebraic and programming regex).
5. Construct the NFA (States, transitions, diagram, JSON data).
6. Perform NFA-to-DFA Conversion (Subset construction, dead state).
7. Minimize the DFA (Partition refinement, merging equivalent states).

### Deliverables

- Project folder structure with all placeholders.
- `docs/System_Overview.md` & `docs/DOC_TEAM_TWO_LAYER_GUIDE.md`
- `docs/FORMAL_SPECIFICATION.md`
- `docs/REGULAR_EXPRESSION.md`
- `docs/NFA_SPECIFICATION.md` & `data/nfa.json` & `diagrams/nfa.dot`
- `docs/DFA_SPECIFICATION.md` & `data/dfa.json` & `diagrams/dfa.dot`
- `docs/MINIMIZED_DFA_SPECIFICATION.md` & `data/minimized_dfa.json` & `diagrams/minimized_dfa.dot`

### Definition of Done

- Scope and two-layer policy are finalized and documented.
- Project skeleton exists.
- All formal mathematical artifacts are defined, cross-verified for equivalence, and saved in their respective `.md`, `.json`, and `.dot` files.

### Estimated Time

4 to 6 hours.

---

## Phase 1: Core Validation Engine

### Objective

Implement the backend logic, including the Alphabet Check (Layer 1), the Lexical Normalizer (Layer 2), and the Minimized DFA simulation.

### Tasks

1. Implement `core/alphabet_check.py` (Layer 1 validation).
2. Implement `core/normalizer.py` (Layer 2: N1 meridiem case-fold, N2 hour padding).
3. Implement `core/automaton.py` (Minimized DFA transition table and state evaluation).
4. Implement `core/trace.py` (Step-by-step state transition recording).
5. Implement `core/diagnostics.py` (Rejection layer classification, failure position, and UX suggestions).
6. Implement `core/samples.py` (Curated test inputs).

### Deliverables

- Fully functional backend modules in the `core/` directory.

### Definition of Done

- Layer 1 correctly rejects invalid alphabet symbols.
- Layer 2 correctly normalizes and validates human-friendly inputs.
- The minimized DFA correctly accepts the 2,880 canonical strings.
- Trace generation and diagnostic explanations work without crashing.

### Estimated Time

2 to 3 hours.

---

## Phase 2: GUI Development

### Objective

Build the Streamlit front-end to display the dual-layer results, formal artifacts, and automaton traces.

### Tasks

1. Create main app layout (`app.py` and `ui/layout.py`).
2. Build Summary Tab (Dual-layer display: Raw vs Normalized results).
3. Build Formal Language Tab (Display alphabet, rules, and regex).
4. Build Automata Tab (Display NFA, DFA, and Minimized DFA tables/diagrams).
5. Build Trace Tab (Display step-by-step simulation).
6. Build Test Cases Tab (Display behavior matrix).
7. Wire UI components to the Core Validation Engine.

### Deliverables

- Fully functional Streamlit application in the `ui/` directory and `app.py`.

### Definition of Done

- User can enter input and trigger validation.
- Both Layer 1 and Layer 2 results are clearly displayed.
- All formal artifacts and traces render correctly in their respective tabs.
- GUI is stable and ready for live demonstration.

### Estimated Time

2 to 3 hours.

---

## Phase 3: Testing and Demonstration Preparation

### Objective

Ensure the system is bug-free, handles edge cases gracefully, and is fully prepared for the live panel defense.

### Tasks

1. Write unit tests for the alphabet check, normalizer, and automaton.
2. Verify all 9 cases in the Behavior Matrix.
3. Test boundary cases (`00:00`, `12:00 AM`, `23:59`, `13:00 PM`).
4. Fix any critical UI or logic bugs discovered during testing.
5. Write the final `docs/TEST_PLAN.md` and `docs/DEMO_SCRIPT.md`.

### Deliverables

- `tests/` directory with passing pytest scripts.
- `docs/TEST_PLAN.md` and `docs/DEMO_SCRIPT.md`.

### Definition of Done

- All unit tests and behavior matrix tests pass.
- Demo script is written and rehearsed.
- No critical crashes occur during normal or malicious input.

### Estimated Time

1 to 2 hours.

---

## Phase 4: Final Polish and Submission

### Objective

Finalize all documentation, polish the UI wording, and prepare the repository for final submission and grading.

### Tasks

1. Review all `docs/` for consistency, formatting, and alignment with the two-layer policy.
2. Polish GUI labels, colors, and explanations for maximum clarity.
3. Update the root `README.md` with final project status, setup instructions, and execution commands.
4. Final git cleanup and branch merging.

### Deliverables

- Completed documentation set.
- Final `README.md`.
- Clean, demo-ready `main` branch.

### Definition of Done

- Project looks complete and professional.
- Theory is clearly connected to the implementation.
- System can be demonstrated smoothly within 5 minutes.

### Estimated Time

1 to 2 hours.