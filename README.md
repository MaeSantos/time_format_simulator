# Time Format Validator – DFA and NFA Simulator

This Python desktop application validates time formats while showing the state transition made for every input character.

## Formats

- **DFA:** strict 24-hour format `HH:MM`, from `00:00` to `23:59`
- **NFA:** strict 12-hour format `hh:mm AM/PM`, from `01:00 AM` to `12:59 PM`

Because both formats are strict, the hour always has two digits. Therefore, `9:30` is rejected while `09:30` is accepted by the DFA.

## Run the simulator

1. Install Python 3.10 or newer. Tkinter is normally included with Python on Windows.
2. Open a terminal inside this folder.
3. Run:

```bash
python app.py
```

No external Python packages are needed.

## Run the tests

```bash
python -m unittest -v
```

## How DFA is applied

The DFA has only one active state at any moment. The first two characters are checked as a valid 24-hour hour, the third must be a colon, and the last two must form a minute from 00 to 59. Any invalid character moves the machine to a dead state.

## How NFA is applied

The NFA stores a set of possible current states. When the first digit is `1`, the machine can explore more than one possible hour path. A time is accepted when at least one path finishes at `n9` after reading the complete `hh:mm AM/PM` input.

## Suggested demonstration

Try these inputs while explaining the transition table:

| Machine | Input | Result | Reason |
|---|---|---|---|
| DFA | `09:30` | Accepted | Correct 24-hour format |
| DFA | `9:30` | Rejected | Missing leading zero |
| DFA | `24:00` | Rejected | Hour cannot be 24 |
| NFA | `11:45 PM` | Accepted | Correct 12-hour format |
| NFA | `13:00 PM` | Rejected | Hour cannot be 13 |
| NFA | `09:60 AM` | Rejected | Minute cannot be 60 |
