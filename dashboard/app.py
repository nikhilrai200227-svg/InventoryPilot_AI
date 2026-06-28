import streamlit as st

st.set_page_config(
    page_title="InventoryPilot AI",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📦 InventoryPilot AI")
st.caption("Agentic Inventory Intelligence Platform")
st.sidebar.markdown("## Navigation")

pages = {
    "Home": "home",
    "Forecast": "forecast",
    "Inventory": "inventory",
    "Explainability": "explain",
    "Scenario Planner": "scenario",
    "Insights": "insights",
    "Reports": "reports",
    "AI Assistant": "assistant",
}

for label, page_file in pages.items():
    st.sidebar.page_link(f"pages/{page_file}.py", label=label)
