import streamlit as st
import pandas as pd
from dashboard.api_client import get

st.title("Dashboard Home")

col1, col2, col3, col4 = st.columns(4)

try:
    inv = get("/inventory/levels", timeout=5).json()
    col1.metric("Products Tracked", len(inv))

    risks = get("/inventory/stockout-risk", timeout=5).json()
    high_risk = sum(1 for r in risks if r.get("risk_level") == "high")
    col2.metric("High Stockout Risk", high_risk, delta_color="inverse")

    total_stock = sum(r.get("quantity_on_hand", 0) for r in inv)
    col3.metric("Total Units on Hand", total_stock)

    col4.metric("System Status", "Online")
except Exception as e:
    st.error(f"Could not reach API: {e}")
    st.info("Make sure the API server is running and API_BASE_URL is set in secrets.")
