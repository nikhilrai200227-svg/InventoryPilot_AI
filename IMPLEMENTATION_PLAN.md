# InventoryPilot AI – Implementation Plan

## Phase 1: Project Foundation
- **1.1** – Python project structure, `pyproject.toml`, dependencies, folder skeleton
- **1.2** – Configuration management with Pydantic Settings
- **1.3** – Data models (SQLAlchemy ORM) and Pydantic schemas
- **1.4** – Data ingestion pipeline (CSV/API loaders, cleaning, feature engineering)

## Phase 2: Forecasting Engine
- **2.1** – Feature engineering module (time-based, product, calendar features)
- **2.2** – Model registry with unified wrapper (RF, XGB, LGBM, CatBoost)
- **2.3** – Optuna hyperparameter optimization
- **2.4** – Automatic model selection pipeline

## Phase 3: Multi-Agent LangGraph Workflow
- **3.1** – Base agent class and registry
- **3.2** – 5 specialized agents (DemandForecast, InventoryAnalysis, Explainability, BusinessRecommendation, ExecutiveReport)
- **3.3** – LangGraph `StateGraph` with nodes, edges, conditional routing
- **3.4** – LangChain tool definitions per agent

## Phase 4: Explainability (SHAP)
- **4.1** – `ShapExplainer` class (global + local explanations)
- **4.2** – Explanation storage and API formatting

## Phase 5: FastAPI Backend
- **5.1** – Application factory with middleware, lifespan events
- **5.2** – Route modules: forecast, inventory, explain, recommendations, reports, assistant
- **5.3** – Background task management for long-running jobs

## Phase 6: Streamlit Dashboard
- **6.1** – Multi-page app structure
- **6.2** – Pages: Home, Forecast, Inventory, Explainability, Scenario, Insights, Reports, Assistant
- **6.3** – Shared components (charts, navigation, theme)

## Phase 7: Gemini AI Assistant
- **7.1** – LangChain Gemini integration with system prompt
- **7.2** – RAG pipeline over product docs/reports (optional)
- **7.3** – Prompt templates for Q&A, recommendations, summarization

## Phase 8: Docker & Deployment
- **8.1** – Dockerfiles for API and dashboard
- **8.2** – Docker Compose (api, dashboard, db, redis)
- **8.3** – Nginx config, healthchecks, environment configs

## Phase 9: Testing & Quality
- **9.1** – Unit tests for models, agents, features, SHAP, utils
- **9.2** – Integration tests for API endpoints and full workflow
- **9.3** – Ruff, mypy, pre-commit, coverage

## Phase 10: Documentation & Git
- **10.1** – Git init, .gitignore, README, architecture diagram
- **10.2** – Makefile with convenience targets
