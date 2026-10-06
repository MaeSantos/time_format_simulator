"""Automata tab: renders NFA, DFA, and minimized DFA diagrams and tables."""

import json
import pathlib

import pandas as pd
import streamlit as st

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DIAGRAM_DIR = ROOT / "diagrams"


def _load_json(name):
    with open(DATA_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_dot(name):
    with open(DIAGRAM_DIR / name, "r", encoding="utf-8") as f:
        return f.read()


def _table(spec):
    has_eps = "epsilon_transitions" in spec
    rows = []
    for state in spec["states"]:
        label = state
        if state == spec.get("start"):
            label = "→ " + label
        if state in spec.get("accepting", []):
            label = "* " + label
        row = {"State": label}
        if has_eps:
            eps = spec["epsilon_transitions"].get(state)
            row["ε"] = ", ".join(eps) if eps else "∅"
        trans = spec["transitions"].get(state, {})
        for sym in spec["alphabet"]:
            disp = "␣" if sym == "SPACE" else sym
            targets = trans.get(sym)
            row[disp] = ", ".join(targets) if targets else "∅"
        rows.append(row)
    return pd.DataFrame(rows)


def render():
    st.subheader("Automata Artifacts")
    t1, t2, t3 = st.tabs([
        "NFA (19 states)", "DFA (17 states)", "Minimized DFA (15 states)"
    ])

    with t1:
        st.graphviz_chart(_load_dot("nfa.dot"))
        st.dataframe(_table(_load_json("nfa.json")), hide_index=True)

    with t2:
        st.graphviz_chart(_load_dot("dfa.dot"))
        st.dataframe(_table(_load_json("dfa.json")), hide_index=True)

    with t3:
        st.graphviz_chart(_load_dot("minimized_dfa.dot"))
        st.dataframe(_table(_load_json("minimized_dfa.json")), hide_index=True)

    st.caption(
        "Diagrams are rendered live from diagrams/*.dot and match the tables "
        "and the team papers. Full specs: docs/*_SPECIFICATION.md"
    )