import streamlit as st
import pandas as pd
from dashboard.api_client import get

st.title("Inventory Analysis")

tab1, tab2 = st.tabs(["Stock Levels", "Stockout Risk"])

with tab1:
    try:
        resp = get("/inventory/levels", timeout=5)
        df = pd.DataFrame(resp.json())
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load inventory: {e}")

with tab2:
    try:
        resp = get("/inventory/stockout-risk", timeout=5)
        df = pd.DataFrame(resp.json())
        st.dataframe(df, use_container_width=True)

        risk_counts = df["risk_level"].value_counts()
        st.bar_chart(risk_counts)
    except Exception as e:
        st.error(f"Could not load stockout risk: {e}")
