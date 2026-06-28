import streamlit as st
from dashboard.api_client import post

st.title("AI Assistant")
st.markdown("Ask questions about your inventory, forecasts, or supply chain.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about your inventory..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                resp = post("/assistant/chat", json={"message": prompt}, timeout=30).json()
                reply = resp.get("reply", "No response")
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Assistant error: {e}")
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})
