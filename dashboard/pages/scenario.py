import streamlit as st

st.title("🎯 Scenario Planner")
st.markdown("""
Adjust parameters below to simulate **what-if scenarios** and see how they affect forecasts and inventory levels.
*(Scenario engine will be connected in a future iteration — the pipeline supports re-running with modified inputs.)*
""")

col1, col2 = st.columns(2)
with col1:
    demand_multiplier = st.slider("Demand Change (%)", -50, 100, 0)
    lead_time = st.slider("Lead Time (days)", 1, 60, 7)
with col2:
    safety_stock = st.number_input("Safety Stock", min_value=0, value=0)
    reorder_point = st.number_input("Reorder Point", min_value=0, value=10)

if st.button("Run Scenario"):
    st.info(
        f"Scenario: {demand_multiplier:+,d}% demand, {lead_time}d lead time, "
        f"{safety_stock} safety stock. Full integration with forecast pipeline incoming."
    )
