# Formal Language Specification

## 1. Problem Definition

The Time Format Validator determines whether an input string follows a valid time format in the combined language $L_{TIME} = L_{24} \cup L_{12}$. 

The system supports two valid representations simultaneously without requiring manual mode selection:
1. 24-hour time, written as `HH:MM`
2. Standard 12-hour time, written as `HH:MM AM` or `HH:MM PM`

The validator receives an input string and returns `ACCEPTED` if the string satisfies the formal grammar of either format. Otherwise, it returns `REJECTED`.

---

## 2. The Master System Alphabet ($\Sigma_{TIME}$)

The system operates over a strictly defined, finite alphabet of exactly 15 symbols. Any symbol not present in this set is immediately rejected by the **Alphabet Check** layer before the automaton is executed.

$$
\Sigma_{TIME} = \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ':', '\sqcup', 'A', 'M', 'P'\}
$$

*(Note: $\sqcup$ denotes exactly one literal space character.)*

---

## 3. Component Sets

To define the language formally, we define the following component sets:

- **Decimal Digits ($D$):** $D = \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9\}$
- **Valid 24-Hour Hours ($H_{24}$):** Strings representing `00` to `23`.
- **Valid 12-Hour Hours ($H_{12}$):** Strings representing `01` to `12`.
- **Valid Minutes ($MIN$):** Strings representing `00` to `59`.
- **Meridiem Markers ($MER$):** $\{AM, PM\}$

---

## 4. The 24-Hour Language ($L_{24}$)

The 24-hour language consists of strings formatted as `HH:MM` where the hour is strictly between `00` and `23`, and the minute is strictly between `00` and `59`.

**Alphabet Subset:**
$$
\Sigma_{24} = \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ':'\} \subset \Sigma_{TIME}
$$

**Formal Definition:**
$$
L_{24} = \{ h \text{ ":" } m \mid h \in H_{24} \text{ and } m \in MIN \}
$$

---

## 5. The 12-Hour Language ($L_{12}$)

The 12-hour language consists of strings formatted as `HH:MM AM` or `HH:MM PM` where the hour is strictly between `01` and `12`, the minute is between `00` and `59`, and there is exactly one space before an uppercase meridiem marker.

**Alphabet Subset:**
$$
\Sigma_{12} = \{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, ':', '\sqcup', 'A', 'M', 'P'\} = \Sigma_{TIME}
$$

**Formal Definition:**
$$
L_{12} = \{ h \text{ ":" } m \sqcup r \mid h \in H_{12} \text{ and } m \in MIN \text{ and } r \in MER \}
$$

---

## 6. The Combined System Language ($L_{TIME}$)

The validator implements a single unified language over the alphabet $\Sigma_{TIME}$. The system processes inputs directly without an upfront mode selector. A string is accepted if it transitions to an accepting state for either format.

$$
L_{TIME} = L_{24} \cup L_{12}
$$

**Total Accepted Strings:** 2,880
- 1,440 strings from $L_{24}$ (24 hours × 60 minutes)
- 1,440 strings from $L_{12}$ (12 hours × 60 minutes × 2 markers)

---

## 7. Rejection Layers

When an input is rejected, it fails at one of two distinct layers. This classification is critical for the system's diagnostic output and the GUI's dual-layer display.

1. **Alphabet Check:** The input contains symbols not in $\Sigma_{TIME}$ (e.g., lowercase letters, dashes). The string is rejected *before* the DFA executes.
2. **Automaton (Dead State):** The input consists only of valid $\Sigma_{TIME}$ symbols, but the sequence violates the grammatical structure of $L_{TIME}$, causing the DFA to transition into the dead state ($\emptyset$) or end in a non-accepting state.

---

## 8. Boundary Cases

These edge cases demonstrate how the unified language $L_{TIME}$ resolves overlaps and strict formatting rules.

| Input | In $L_{24}$? | In $L_{12}$? | System Result ($L_{TIME}$) | Explanation |
|---|---|---|---|---|
| `00:00` | Yes | No | **ACCEPTED** | Earliest valid 24-hour time; standard hours start at 01. |
| `12:00` | Yes | No | **ACCEPTED** | Valid 24-hour noon; standard mode requires an AM/PM suffix. |
| `12:00 AM` | No | Yes | **ACCEPTED** | Midnight in standard 12-hour format. |
| `12:00 PM` | No | Yes | **ACCEPTED** | Noon in standard 12-hour format. |
| `13:00` | Yes | No | **ACCEPTED** | Valid 24-hour time; standard-time hours stop at 12. |
| `23:59` | Yes | No | **ACCEPTED** | Latest valid 24-hour time before midnight. |
| `00:00 AM` | No | No | **REJECTED** | Hour 00 does not exist in 12-hour time, and 24-hour time does not permit AM/PM. |
| `13:00 PM` | No | No | **REJECTED** | Hour 13 exceeds 12-hour maximum, and 24-hour time does not permit AM/PM. |

---

## 9. Rejected Strings Examples

### 9.1 Alphabet Check Rejections (Layer 1)
*Rejected before DFA execution due to invalid symbols.*

| Input | Reason for Rejection |
|---|---|
| `09-30` | Symbol `-` is not in $\Sigma_{TIME}$. |
| `ab:cd` | Symbols `a, b, c, d` are not in $\Sigma_{TIME}$. |
| `09:30 am` | Lowercase `a, m` are not in $\Sigma_{TIME}$ (meridiem must be uppercase). |
| `09:30 XM` | Symbol `X` is not in $\Sigma_{TIME}$. |

### 9.2 Automaton Dead State Rejections (Layer 2)
*Rejected by the DFA due to structural or numerical violations.*

| Input | Reason for Rejection |
|---|---|
| `24:00` | Hour exceeds 23. |
| `23:60` | Minute exceeds 59. |
| `9:30` | Hour does not have two digits (missing leading zero). |
| `09:5` | Minute does not have two digits. |
| `0930` | Missing colon `:`. |
| `18:30 PM` | Hour 18 is invalid for 12-hour format, and 24-hour format does not permit a meridiem suffix. |
| `09:30AM` | Missing required single space delimiter before meridiem. |
| `09:30  AM` | Contains consecutive spaces instead of exactly one. |

---