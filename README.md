---
title: CustomerCore API
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# CustomerCore Intelligence Platform

Real-time multi-tenant customer intelligence powered by streaming (Redpanda), lakehouse storage (Iceberg/R2), multi-agent AI (LangGraph), and full MLOps (MLflow/DagsHub).

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/saibalajinamburi/CustomerCore/actions)
[![License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)
[![EU AI Act](https://img.shields.io/badge/EU%20AI%20Act-Compliant-blue)](#responsible-ai)
[![HF Spaces](https://img.shields.io/badge/HF%20Spaces-Live-orange)](https://huggingface.co/spaces/saibalajiomg/customercore)

CustomerCore is an enterprise-grade customer intelligence system designed to automate ticket classification, prioritize issues, calculate churn and SLA breach risks, recall agent memories, retrieve grounded facts, and run automated human-in-the-loop triage flows.

---

## Live System Links

| Asset | Link | Status |
|---|---|---|
| **Live Operations Console (HF Spaces)** | [huggingface.co/spaces/saibalajiomg/customercore](https://huggingface.co/spaces/saibalajiomg/customercore) | ![uptime](https://img.shields.io/badge/Uptime-100%25-brightgreen) |
| **GitHub Repository** | [github.com/saibalajinamburi/CustomerCore](https://github.com/saibalajinamburi/CustomerCore) | Active |
| **DagsHub Repository & DVC** | [dagshub.com/saibalajinamburi/CustomerCore](https://dagshub.com/saibalajinamburi/CustomerCore) | Connected |
| **MLflow Experiment Server** | [dagshub.com/saibalajinamburi/CustomerCore.mlflow](https://dagshub.com/saibalajinamburi/CustomerCore.mlflow) | Runs Tracked |
| **MLflow Model Registry** | [dagshub.com/saibalajinamburi/CustomerCore/models](https://dagshub.com/saibalajinamburi/CustomerCore/models) | Versioned Models |
| **CI/CD Pipeline** | [github.com/saibalajinamburi/CustomerCore/actions](https://github.com/saibalajinamburi/CustomerCore/actions) | Passing ✅ |

---

## Architecture Overview

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full system diagram and description of the data flow pipeline.

### Core Pipelines
1. **Streaming Data Flow:** Kafka-compatible Redpanda topics (`tickets`, `product`, `billing`, `incidents`) ingest event micro-batches.
2. **Spark Lakehouse:** PySpark Structured Streaming processes raw data from Bronze to Silver layers with real-time PII masking and schema validation, writing to Apache Iceberg format.
3. **dbt Gold Layer:** Transforms silver tables into 7 curated business marts for analytics, features, and model training.
4. **LangGraph Triage:** A stateful multi-agent supervisor orchestrates six specialized sub-agents (Classify, Memory, RAG, Churn, Incident, and HITL) to yield a Pydantic-validated 14-field triage output in `<2s`.

---

## What It Does

When a support ticket is received at `/api/v1/triage`, the LangGraph supervisor executes the following sequence:

1. **Classify Agent:** Determines ticket category and initial priority.
2. **Memory Agent:** Recalls customer profile and past session memories from Mem0 (Supabase pgvector).
3. **RAG Agent:** Injects context using hybrid retrieval (Dense + BM25 sparse) from the Knowledge Base and product documentation, reranked by a cross-encoder model.
4. **Churn Agent:** Evaluates churn risk using a local **Random Forest Classifier** trained on client metrics.
5. **Incident Agent:** Inspects incident patterns and flags SLA-breach risks.
6. **HITL Agent:** Interrupts the graph and pauses execution if safety flags are violated or if classifier confidence falls below `0.65`, routing the ticket to the Supabase-backed human-in-the-loop review queue.
7. **Finalize & Log:** Consolidates state, applies PII scrubbing, logs the audit trail, and pushes a structured trace to Langfuse.

---

## Technology Stack

| Layer | Technology |
|---|---|
| **Streaming Backbone** | Redpanda (Kafka-compatible event broker) |
| **Lakehouse Storage** | Apache Iceberg on Cloudflare R2 / MinIO |
| **Stream Processing** | PySpark Structured Streaming / PyArrow |
| **Transformation** | dbt-core with DuckDB adapter (7 Gold marts) |
| **Vector Database** | ChromaDB (BM25 sparse + BGE-M3 dense hybrid retrieval) |
| **LLM Gateway** | LiteLLM routing proxy & Semantic Cache (L1/L2/L3) |
| **Agent Framework** | LangGraph multi-agent supervisor |
| **Long-Term Memory** | Mem0 backed by Supabase pgvector |
| **ML Models & Registry** | Random Forest Classifier, MLflow, DagsHub, DVC |
| **LLM Observability** | Langfuse (prompt management and tracing) & LangSmith |
| **Infrastructure Observability**| OpenTelemetry, Prometheus metrics, Grafana Cloud |
| **CI/CD & CML** | GitHub Actions with Continuous Machine Learning metrics reporting |
| **Hosting** | Hugging Face Spaces Docker (Inference) & Supabase PostgreSQL |

---

## Quick Start (Local)

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.12
- Doppler CLI (optional, for secret injection)

### 2. Installation
```bash
git clone https://github.com/saibalajinamburi/CustomerCore.git
cd CustomerCore
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Running Locally

#### Run base services (Redpanda, MinIO, Redis, ChromaDB, OTel):
```bash
docker compose up -d
```

#### Run observability console (Prometheus + Grafana):
```bash
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```
*   **Grafana Dashboard**: Open `http://localhost:3000` (pre-provisioned with metrics visualizations, no login required).
*   **Prometheus Console**: Open `http://localhost:9090`.

#### Start the FastAPI gateway:
Using Doppler:
```bash
doppler run -- uvicorn src.api.main:app --reload --port 8080
```
Without Doppler:
```bash
uvicorn src.api.main:app --reload --port 8080
```

#### Check Health:
```bash
curl http://localhost:8080/api/v1/health
```

---

## ML Model Training & DagsHub Integration

We train a **Random Forest Churn Predictor** locally or in CI, logging parameters, metrics, performance plots (ROC, Confusion Matrix, Feature Importance), and the model binaries directly to DagsHub's MLflow Experiments Server and Model Registry.

To train the model and push to DagsHub manually:
```bash
# Set DagsHub credentials in your shell environment
$env:MLFLOW_TRACKING_USERNAME="saibalajinamburi"
$env:MLFLOW_TRACKING_PASSWORD="YOUR_DAGSHUB_TOKEN"
$env:PYTHONIOENCODING="utf-8"

# Train model and track in MLflow Model Registry
doppler run -- python -X utf8 src/ml/train_churn.py

# Push raw dataset file versioning via DVC
doppler run -- dvc push
```

---

## Project Structure

```text
customercore/
├── .github/workflows/    # CI/CD Workflows (Lint, Pytest, HF Deploy, CML Train)
├── infra/
│   ├── monitoring/       # Prometheus and Grafana local config & dashboards
│   ├── k8s/              # Kubernetes YAML manifests (Deployment, Ingress, Secrets)
│   ├── kind-config.yaml  # Kind local multi-node cluster configuration
│   └── otel-collector.yaml
├── src/
│   ├── api/              # FastAPI Application endpoints and middleware
│   ├── agent/            # LangGraph supervisor and agent nodes
│   ├── rag/              # ChromaDB, Hybrid Retriever, Semantic Cache
│   ├── ml/               # Model training scripts (Random Forest)
│   ├── streaming/        # Redpanda Producers and PySpark pipeline
│   ├── dbt/              # dbt transform pipeline (Gold marts)
│   ├── db/               # Supabase database repositories and clients
│   └── responsible_ai/   # Model cards, fairness evaluation, audit logger
├── tests/                # Unit and integration test suites
├── Dockerfile            # Default Production Dockerfile
├── Dockerfile.hf         # Hugging Face optimized Dockerfile
├── docker-compose.yml    # Standard services configuration
└── docker-compose.monitoring.yml # Local Grafana / Prometheus observability stack
```

---

## Responsible AI & EU AI Act Compliance

CustomerCore is designed with compliance in mind for the **EU AI Act (effective August 2026)**:
- **Article 10 (Data Governance):** Schema enforcement and automated PII masking via Presidio.
- **Article 12 (Traceability):** Structured audit logging of all constitutional violations and inputs/outputs to Supabase PostgreSQL.
- **Article 14 (Human Oversight):** LangGraph-native `interrupt()` gates that pause low-confidence decisions for manual human sign-off.
- **Article 15 (Accuracy & Security):** Model card documentation for all ML models (`src/responsible_ai/model_cards/`) and demographic fairness accuracy gaps.

---

## Author

**Saibalaji Namburi**  
MSc Data Analytics, University of Hildesheim  
- GitHub: [@saibalajinamburi](https://github.com/saibalajinamburi)
- DagsHub: [saibalajinamburi](https://dagshub.com/saibalajinamburi)
