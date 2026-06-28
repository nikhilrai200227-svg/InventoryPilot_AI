# InventoryPilot AI

Agentic inventory intelligence platform: demand forecasting, explainability, and LLM-powered insights.

## Architecture

```
Streamlit Cloud  ──HTTP──▶  Render (FastAPI)
   (dashboard)                  │
                                ├── LangGraph agents
                                ├── ML pipeline (RF/XGB/LGBM/CatBoost)
                                ├── SHAP explainability
                                └── Gemini AI assistant
```

## Quick Start (Local)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Set your Gemini API key
echo "GEMINI_API_KEY=your-key-here" >> .env

# 3. Seed database and start API
python -c "from scripts.seed_data import seed; seed()"
uvicorn app.main:app --host 0.0.0.0 --port 8000

# 4. In another terminal, start dashboard
streamlit run dashboard/app.py
```

## Deploy to Production

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USER/InventoryPilot_AI.git
git push -u origin main
```

### Step 2: Deploy API on Render

1. Go to https://dashboard.render.com → **New +** → **Web Service**
2. Connect your GitHub repo
3. Use these settings:

| Setting | Value |
|---|---|
| Name | `inventorypilot-api` |
| Environment | `Docker` |
| Dockerfile Path | `Dockerfile.api` |
| Port | `8000` |

4. Add environment variable in Render dashboard:
   - `GEMINI_API_KEY` → your actual Gemini API key
5. Click **Create Web Service**
6. Wait for build/deploy. Copy the URL (e.g. `https://inventorypilot-api.onrender.com`)

### Step 3: Deploy Dashboard on Streamlit Cloud

1. Go to https://share.streamlit.io → **New app**
2. Connect your GitHub repo
3. Main file path: `dashboard/app.py`
4. In **Advanced settings** → **Secrets**, paste:
   ```toml
   GEMINI_API_KEY = "your-gemini-api-key"
   API_BASE_URL = "https://inventorypilot-api.onrender.com/api/v1"
   ```
5. Click **Deploy**

Your dashboard will be live at `https://YOUR_APP.streamlit.app`.

### Optional: Deploy with Docker Compose

```bash
docker-compose up --build
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/api/v1/forecast/run` | Run forecast for a product |
| GET | `/api/v1/inventory/levels` | Current stock levels |
| GET | `/api/v1/inventory/stockout-risk` | Stockout risk analysis |
| POST | `/api/v1/explain/prediction` | SHAP explanation |
| POST | `/api/v1/reports/generate` | Executive report |
| POST | `/api/v1/assistant/chat` | Chat with AI assistant |
