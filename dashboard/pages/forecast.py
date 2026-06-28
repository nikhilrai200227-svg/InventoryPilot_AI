import streamlit as st
import pandas as pd
import plotly.express as px
from dashboard.api_client import post

st.title("Demand Forecast")

product_id = st.number_input("Product ID", min_value=1, value=1)
days_ahead = st.slider("Forecast Horizon (days)", 7, 365, 30)

if st.button("Run Forecast"):
    with st.spinner("Training models and generating forecast..."):
        try:
            resp = post("/forecast/run", json={"product_id": product_id, "days_ahead": days_ahead}, timeout=120).json()

            if "error" in resp:
                st.error(resp["error"])
            else:
                df = pd.DataFrame({
                    "Date": resp["forecast_dates"],
                    "Forecast": resp["forecast_values"],
                })
                df["Date"] = pd.to_datetime(df["Date"])

                fig = px.line(df, x="Date", y="Forecast", title=f"Forecast — Model: {resp['model_used']}")
                st.plotly_chart(fig, use_container_width=True)

                metrics = resp.get("metrics", {})
                if metrics:
                    st.subheader("Model Performance")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("MAE", f"{metrics.get('mae', 0):.2f}")
                    col2.metric("RMSE", f"{metrics.get('rmse', 0):.2f}")
                    col3.metric("MAPE", f"{metrics.get('mape', 0):.2%}")
        except Exception as e:
            st.error(f"Request failed: {e}")
