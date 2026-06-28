import os

import requests
import streamlit as st

API_BASE = (
    st.secrets.get("API_BASE_URL", "http://localhost:8000/api/v1")
    if hasattr(st, "secrets") and "API_BASE_URL" in st.secrets
    else os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")
)


def get(endpoint: str, timeout: int = 10, **kwargs):
    return requests.get(f"{API_BASE}{endpoint}", timeout=timeout, **kwargs)


def post(endpoint: str, json: dict | None = None, timeout: int = 30, **kwargs):
    return requests.post(
        f"{API_BASE}{endpoint}", json=json or {}, timeout=timeout, **kwargs
    )
