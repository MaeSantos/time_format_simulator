"""DFA and NFA models used by the Time Format Validator Simulator."""

from dataclasses import dataclass
from typing import Dict, FrozenSet, List, Set, Tuple


@dataclass
class SimulationResult:
    accepted: bool
    steps: List[Tuple[str, str, str]]
    final_state: str
    explanation: str


class TimeDFA:
    """Deterministic validator for strict 24-hour time: HH:MM."""

    accepting = {"q5"}

    @staticmethod
    def _next(state: str, ch: str) -> str:
        if state == "q0" and ch in "01":
            return "q1"
        if state == "q0" and ch == "2":
            return "q2"
        if state == "q1" and ch.isdigit():
            return "q3"
        if state == "q2" and ch in "0123":
            return "q3"
        if state == "q3" and ch == ":":
            return "q4"
        if state == "q4" and ch in "012345":
            return "q6"
        if state == "q6" and ch.isdigit():
            return "q5"
        return "dead"

    def simulate(self, text: str) -> SimulationResult:
        state = "q0"
        steps = [("Start", "ε", state)]
        for ch in text:
            old = state
            state = self._next(state, ch)
            steps.append((old, repr(ch), state))
            if state == "dead":
                break
        accepted = state in self.accepting and len(steps) == len(text) + 1
        if accepted:
            explanation = "Accepted: the input follows HH:MM and is between 00:00 and 23:59."
        elif state == "dead":
            explanation = "Rejected: a character did not have a valid transition from the current state."
        else:
            explanation = "Rejected: the input ended before reaching the accepting state q5."
        return SimulationResult(accepted, steps, state, explanation)


class TimeNFA:
    """Nondeterministic validator for strict 12-hour time: hh:mm AM/PM."""

    accepting = frozenset({"n9"})

    def _next(self, states: FrozenSet[str], ch: str) -> FrozenSet[str]:
        result: Set[str] = set()
        upper = ch.upper()
        for state in states:
            if state == "n0" and ch == "0":
                result.add("n1")
            if state == "n0" and ch == "1":
                # Two possible paths on the same symbol demonstrate nondeterminism.
                result.add("n2")
            if state == "n1" and ch in "123456789":
                result.add("n3")
            if state == "n2" and ch in "012":
                result.add("n3")
            if state == "n3" and ch == ":":
                result.add("n4")
            if state == "n4" and ch in "012345":
                result.add("n5")
            if state == "n5" and ch.isdigit():
                result.add("n6")
            if state == "n6" and ch == " ":
                result.add("n7")
            if state == "n7" and upper in "AP":
                result.add("n8")
            if state == "n8" and upper == "M":
                result.add("n9")
        return frozenset(result)

    def simulate(self, text: str) -> SimulationResult:
        states = frozenset({"n0"})
        steps = [("Start", "ε", self._label(states))]
        for ch in text:
            old = self._label(states)
            states = self._next(states, ch)
            steps.append((old, repr(ch), self._label(states)))
            if not states:
                break
        accepted = bool(states & self.accepting) and len(steps) == len(text) + 1
        if accepted:
            explanation = "Accepted: the input follows hh:mm AM/PM and uses an hour from 01 to 12."
        elif not states:
            explanation = "Rejected: every possible NFA path stopped on an invalid character."
        else:
            explanation = "Rejected: the input ended without reaching accepting state n9."
        return SimulationResult(accepted, steps, self._label(states), explanation)

    @staticmethod
    def _label(states: FrozenSet[str]) -> str:
        return "{" + ", ".join(sorted(states)) + "}" if states else "∅"


def validate_time(text: str, machine: str) -> SimulationResult:
    if machine == "DFA – 24-hour (HH:MM)":
        return TimeDFA().simulate(text)
    return TimeNFA().simulate(text)
