import pandas as pd
import streamlit as st

from core.diagnostics import build_report
from core.samples import SAMPLES


def render():
    st.subheader("Behavior Matrix (live check)")
    rows = []
    for s in SAMPLES:
        r = build_report(s["input"])
        ok = (r["formal_accepted"] == s["formal"]) and (r["system_accepted"] == s["system"])
        rows.append({
            "Input": s["input"],
            "Expected (L1/L2)": f"{s['formal']}/{s['system']}",
            "Actual (L1/L2)": f"{r['formal_accepted']}/{r['system_accepted']}",
            "Result": "PASS" if ok else "FAIL",
            "Note": s["note"],
        })
    df = pd.DataFrame(rows)
    st.dataframe(df, hide_index=True)
    if (df["Result"] == "FAIL").any():
        st.error("Some behavior-matrix cases fail.")
    else:
        st.success("All behavior-matrix cases pass.")