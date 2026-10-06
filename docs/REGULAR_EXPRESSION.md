# Regular Expression Specification

## 1. Overview

The Regular Expression (RE) provides a concise, algebraic representation of the formal language $L_{TIME}$. It serves as the bridge between the formal language definition and the construction of the $\epsilon$-NFA. 

The system uses two representations of the regular expression:
1. **Formal Algebraic RE:** Used for mathematical proofs and NFA construction (as documented in the team papers).
2. **Programming RE:** Used for quick validation references and standard pattern matching in Python/PCRE.

---

## 2. Formal Algebraic Regular Expression

Based on the component sets defined in the Formal Language Specification, the algebraic regular expression for $L_{TIME}$ is constructed using union ($+$), concatenation, and Kleene star (where applicable, though not needed for this finite language).

Let $D = \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9\}$ represent the set of decimal digits.

### 2.1 The 24-Hour Subexpression ($R_{24}$)

The 24-hour format requires a valid hour (`00`-`23`) followed by a colon and a valid minute (`00`-`59`).

$$
R_{24} = \Big( (0 + 1)D + 2(0 + 1 + 2 + 3) \Big) \cdot \text{" : "} \cdot \Big( (0 + 1 + 2 + 3 + 4 + 5)D \Big)
$$

### 2.2 The 12-Hour Subexpression ($R_{12}$)

The 12-hour format requires a valid hour (`01`-`12`), a colon, a valid minute (`00`-`59`), exactly one space ($\sqcup$), and a meridiem marker (`AM` or `PM`).

$$
R_{12} = \Big( 0(1 + 2 + \dots + 9) + 1(0 + 1 + 2) \Big) \cdot \text{" : "} \cdot \Big( (0 + 1 + 2 + 3 + 4 + 5)D \Big) \cdot \sqcup \cdot (AM + PM)
$$

### 2.3 The Combined System Expression ($R_{TIME}$)

The unified language is the union of both formats.

$$
R_{TIME} = R_{24} + R_{12}
$$

---

## 3. Programming Regular Expression (Implementation Reference)

For software implementation, testing, and standard pattern matching (e.g., Python's `re` module), the algebraic expression is translated into standard PCRE (Perl Compatible Regular Expressions) syntax.

```regex
^((([01][0-9]|2[0-3]):[0-5][0-9])|((0[1-9]|1[0-2]):[0-5][0-9] (AM|PM)))$