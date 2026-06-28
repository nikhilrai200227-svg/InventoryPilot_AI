import streamlit as st

st.title("💡 Business Insights")
st.markdown("AI-generated recommendations based on forecast and inventory analysis.")

if st.button("Generate Recommendations"):
    st.info("This will run the full agent workflow. Requires Gemini API key and running backend.")
    # Future: call /api/v1/agent/run or the LangGraph workflow
