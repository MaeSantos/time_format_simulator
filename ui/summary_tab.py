import streamlit as st


def _invalid_text(invalid):
    return ", ".join(f"'{c}' at index {i}" for i, c in invalid)


def render(report):
    if report["system_accepted"]:
        st.success(f"ACCEPTED - detected as {report['detected_format']} format")
    else:
        st.error(f"REJECTED - {report['rejection_layer']}")

    left, right = st.columns(2)

    with left:
        st.markdown("### Layer 1 - Formal (raw input)")
        st.code(report["raw"])
        if report["layer1"]["sim"] is None:
            st.error("Alphabet Check failed (rejected before automaton).")
            st.write("Invalid symbols:", _invalid_text(report["layer1"]["invalid"]))
        else:
            sim = report["layer1"]["sim"]
            if report["formal_accepted"]:
                st.success(f"ACCEPTED (final state {sim['final_state']})")
            else:
                st.error(f"REJECTED (final state {sim['final_state']})")

    with right:
        st.markdown("### Layer 2 - System (normalized)")
        st.code(report["normalized"])
        if report["layer2"]["sim"] is None:
            st.error("Alphabet Check failed on normalized input.")
            st.write("Invalid symbols:", _invalid_text(report["layer2"]["invalid"]))
        else:
            sim = report["layer2"]["sim"]
            if report["system_accepted"]:
                st.success(f"ACCEPTED (final state {sim['final_state']})")
            else:
                st.error(f"REJECTED (final state {sim['final_state']})")

    st.info(report["explanation"])

    if report["failure"]:
        f = report["failure"]
        cols = st.columns(3)
        cols[0].metric("Failure index", f["index"])
        cols[1].metric("Received symbol", f["char"] if f["char"] else "(end of input)")
        cols[2].write(f"**Expected:** {', '.join(f['expected'])}")