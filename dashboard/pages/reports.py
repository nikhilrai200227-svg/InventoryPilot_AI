import streamlit as st
from dashboard.api_client import post

st.title("Executive Reports")

if st.button("Generate Report"):
    with st.spinner("Generating executive report via Gemini..."):
        try:
            resp = post("/reports/generate", json={}, timeout=60)
            report = resp.json().get("report", "")
            st.markdown(report)
        except Exception as e:
            st.error(f"Report generation failed: {e}")
