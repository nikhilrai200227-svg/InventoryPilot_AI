import streamlit as st
import pandas as pd
from dashboard.api_client import post

st.title("Explainability")
st.markdown("Understand **why** the model made its prediction using SHAP.")

product_id = st.number_input("Product ID", min_value=1, value=1)

if st.button("Explain Prediction"):
    with st.spinner("Computing SHAP values..."):
        try:
            resp = post("/explain/prediction", json={"product_id": product_id, "forecast_date": ""}, timeout=120).json()

            st.subheader("Global Feature Importance")
            importance = resp.get("global_importance", {})
            imp_df = pd.DataFrame(
                list(importance.items()), columns=["Feature", "Mean |SHAP|"]
            ).sort_values("Mean |SHAP|", ascending=False)
            st.bar_chart(imp_df.set_index("Feature"))

            st.subheader("Local Explanation")
            local = resp.get("local_shap_values", {})
            local_df = pd.DataFrame(
                list(local.items()), columns=["Feature", "SHAP Value"]
            ).sort_values("SHAP Value", ascending=False)
            st.dataframe(local_df, use_container_width=True)

        except Exception as e:
            st.error(f"Request failed: {e}")
