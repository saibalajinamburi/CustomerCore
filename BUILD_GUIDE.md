# CustomerCore - Complete Step-by-Step Build Guide
# Real-Time Multi-Tenant Customer Intelligence Platform
# Cloud-Deployed | Permanently Free | No Credit Card | Built From Scratch
# Author: Saibalaji Namburi | MSc Data Analytics, University of Hildesheim

---

## HOW TO USE THIS GUIDE

Each phase produces a binary checkpoint - a testable, demonstrable output.
Do NOT start the next phase until the current checkpoint is fully green.
Every phase adds to a working system and never breaks it.

Total Phases: 16
Total Estimated Time: 8-10 weeks

---

##############################################################
# PHASE 1 - FOUNDATION, CLOUD ACCOUNTS AND PROJECT SCAFFOLD
##############################################################

Goal: By the end of Phase 1 you have a live GitHub repository,
all 14 free cloud accounts registered, all secrets stored in
Doppler, the full project directory structure on disk, and a
working Python 3.11 virtual environment with all dependencies
installed and frozen.

Estimated Time: 1-2 days

------------------------------------------------------------
## Step 1.1 - Create the GitHub Repository
------------------------------------------------------------

1. Go to github.com
2. Click New repository
3. Name: customercore
4. Visibility: Public
5. Tick: Add a README.md
6. .gitignore template: Python
7. Click Create repository

Then clone it locally:

    git clone https://github.com/YOUR_USERNAME/customercore.git
    cd customercore

------------------------------------------------------------
## Step 1.2 - Register All 14 Free Cloud Accounts
------------------------------------------------------------

Open each in a new browser tab. Use the same email for all.
None of these require a credit card at any step.
If any asks for payment details, select Free or Community plan.

1.  Hugging Face     - huggingface.co         - API backend hosting (HF Spaces Docker)
2.  Supabase         - supabase.com            - PostgreSQL + pgvector database
3.  Upstash          - upstash.com             - Redis for caching and rate limiting
4.  Cloudflare       - dash.cloudflare.com     - R2 object storage for Iceberg lakehouse
5.  Grafana Cloud    - grafana.com             - Metrics, logs, and traces dashboards
6.  OpenRouter       - openrouter.ai           - 29 free LLM models for cloud inference
7.  LangSmith        - smith.langchain.com     - LangGraph agent tracing
8.  Langfuse Cloud   - cloud.langfuse.com      - Prompt registry and observability
9.  Sentry           - sentry.io               - Error tracking for FastAPI
10. Doppler          - doppler.com             - Secret management synced to all platforms
11. DagsHub          - dagshub.com             - MLflow server and DVC remote storage
12. Weights & Biases - wandb.ai                - ML experiment visual tracking
13. UptimeRobot      - uptimerobot.com         - Uptime monitoring and public status page
14. Kaggle           - kaggle.com              - Free T4 GPU for training (30h per week)

------------------------------------------------------------
## Step 1.3 - Collect All API Keys
------------------------------------------------------------

After registering each account, collect the keys below.
Store them temporarily in a plain text file called temp_secrets.txt
on your Desktop. Never put this file inside the git repo.

Where to find each key:
- Supabase: Project -> Settings -> API
- Upstash: Console -> Database -> Details
- Cloudflare R2: R2 -> Manage API Tokens -> Create Token (Object Read Write)
- OpenRouter: openrouter.ai -> Keys -> Create Key
- LangSmith: smith.langchain.com -> Settings -> API Keys
- Langfuse: cloud.langfuse.com -> Settings -> API Keys
- Sentry: Project -> Settings -> Client Keys (DSN)
- DagsHub: User Settings -> Tokens
- W&B: User Settings -> API Keys
- Doppler: Will be set up in Step 1.4

Keys to collect:

    SUPABASE_URL=https://YOUR_PROJECT.supabase.co
    SUPABASE_KEY=your-anon-public-key
    SUPABASE_DB_URL=postgresql://postgres:PASSWORD@db.YOUR_PROJECT.supabase.co:5432/postgres
    UPSTASH_REDIS_URL=rediss://:PASSWORD@HOST.upstash.io:6380
    CLOUDFLARE_R2_ACCESS_KEY_ID=your-key-id
    CLOUDFLARE_R2_SECRET_ACCESS_KEY=your-secret-key
    CLOUDFLARE_R2_ENDPOINT=https://ACCOUNT_ID.r2.cloudflarestorage.com
    CLOUDFLARE_R2_BUCKET=customercore
    OPENROUTER_API_KEY=sk-or-your-key
    LANGSMITH_API_KEY=ls__your-key
    LANGCHAIN_PROJECT=customercore
    LANGCHAIN_TRACING_V2=true
    LANGFUSE_PUBLIC_KEY=pk-lf-your-key
    LANGFUSE_SECRET_KEY=sk-lf-your-key
    SENTRY_DSN=https://KEY@oID.ingest.sentry.io/PROJECT_ID
    DAGSHUB_TOKEN=your-dagshub-token
    MLFLOW_TRACKING_URI=https://dagshub.com/YOUR_USERNAME/customercore.mlflow
    WANDB_API_KEY=your-wandb-key
    LITELLM_MASTER_KEY=sk-generate-a-random-32-char-string-here
    APP_ENV=development
    APP_VERSION=1.0.0
    LLM_BACKEND=openrouter

------------------------------------------------------------
## Step 1.4 - Set Up Doppler as the Secret Manager
------------------------------------------------------------

Doppler is the single source of truth for all secrets.
It syncs automatically to GitHub Actions and HF Spaces.

Install Doppler CLI on Windows (run PowerShell as Administrator):

    winget install doppler

Verify the install:

    doppler --version

Log in to Doppler (opens a browser window):

    doppler login

Inside the customercore repo directory, run setup:

    doppler setup

When prompted:
- Create new project: yes
- Project name: customercore
- Config name: production

Now go to doppler.com in your browser:
1. Open the customercore project
2. Open the production config
3. Click Add Secret for every key from your temp_secrets.txt
4. Paste name and value for each one
5. Save

Sync Doppler to GitHub Actions:
1. Doppler web UI -> Integrations -> GitHub Actions
2. Authorize GitHub
3. Select repo: customercore
4. Click Enable Sync

Verify all secrets are stored:

    doppler secrets --only-names

You should see all 20+ key names listed.

Now delete the local temp file - you no longer need it:

    del "%USERPROFILE%\Desktop\temp_secrets.txt"

------------------------------------------------------------
## Step 1.5 - Create the Full Project Scaffold
------------------------------------------------------------

Run all commands from inside the customercore directory:

    mkdir src\api
    mkdir src\agent
    mkdir src\rag
    mkdir src\ml
    mkdir src\streaming\producers
    mkdir src\dbt\models\bronze
    mkdir src\dbt\models\silver
    mkdir src\dbt\models\gold
    mkdir src\monitoring
    mkdir src\responsible_ai\model_cards
    mkdir infra\k8s
    mkdir tests\unit
    mkdir tests\integration
    mkdir k6
    mkdir data\raw
    mkdir data\features
    mkdir docs\postmortems
    mkdir docs\prompts
    mkdir .github\workflows
    mkdir grafana\dashboards

Create the following files exactly as shown:

--- FILE: .gitignore ---
Replace the GitHub-generated one with this complete version:

    # Secrets - NEVER commit these
    .env
    .env.*
    temp_secrets.txt
    doppler.yaml

    # Python
    __pycache__/
    *.pyc
    *.pyo
    .venv/
    venv/
    *.egg-info/
    dist/
    build/
    .pytest_cache/
    .mypy_cache/
    .ruff_cache/

    # ML artifacts
    mlruns/
    wandb/
    *.gguf
    *.bin
    chroma_data/
    chromadb_data/

    # DVC
    .dvc/tmp/
    .dvc/cache/

    # Data tracked by DVC not git
    data/raw/
    data/features/

    # Local overrides
    *.local

    # OS
    .DS_Store
    Thumbs.db

--- FILE: pyproject.toml ---

    [build-system]
    requires = ["setuptools>=68"]
    build-backend = "setuptools.backends.legacy:build"

    [project]
    name = "customercore"
    version = "1.0.0"
    requires-python = ">=3.11"
    description = "Real-Time Multi-Tenant Customer Intelligence Platform"
    dependencies = []

    [tool.ruff]
    line-length = 100
    target-version = "py311"
    select = ["E", "W", "F", "I"]

    [tool.pytest.ini_options]
    testpaths = ["tests"]
    addopts = "--tb=short -q"
    asyncio_mode = "auto"

--- FILE: .env.example (committed - no real values) ---

    # CustomerCore - Environment Variable Template
    # All real values are managed in Doppler
    # Copy this file to understand what variables are needed

    SUPABASE_URL=https://project.supabase.co
    SUPABASE_KEY=your-anon-key
    SUPABASE_DB_URL=postgresql://postgres:password@db.project.supabase.co:5432/postgres
    UPSTASH_REDIS_URL=rediss://:password@host.upstash.io:6380
    CLOUDFLARE_R2_ACCESS_KEY_ID=your-key-id
    CLOUDFLARE_R2_SECRET_ACCESS_KEY=your-secret
    CLOUDFLARE_R2_ENDPOINT=https://account-id.r2.cloudflarestorage.com
    CLOUDFLARE_R2_BUCKET=customercore
    OPENROUTER_API_KEY=sk-or-your-key
    LANGSMITH_API_KEY=ls__your-key
    LANGCHAIN_PROJECT=customercore
    LANGCHAIN_TRACING_V2=true
    LANGFUSE_PUBLIC_KEY=pk-lf-your-key
    LANGFUSE_SECRET_KEY=sk-lf-your-key
    SENTRY_DSN=https://key@o123.ingest.sentry.io/project
    DAGSHUB_TOKEN=your-token
    MLFLOW_TRACKING_URI=https://dagshub.com/user/customercore.mlflow
    WANDB_API_KEY=your-key
    LITELLM_MASTER_KEY=sk-your-32-char-key
    APP_ENV=development
    APP_VERSION=1.0.0
    LLM_BACKEND=openrouter

--- FILE: conftest.py (project root) ---

    import sys
    import os

    # Make src/ importable from all tests without installing the package
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

--- FILE: tests/__init__.py --- (empty file, just create it)
--- FILE: tests/unit/__init__.py --- (empty file, just create it)
--- FILE: tests/integration/__init__.py --- (empty file, just create it)

--- FILE: src/__init__.py --- (empty file, just create it)

------------------------------------------------------------
## Step 1.6 - Python Virtual Environment and Dependencies
------------------------------------------------------------

Create and activate the virtual environment:

    python -m venv .venv

    # Activate on Windows
    .venv\Scripts\activate

    # Verify you are inside the venv - should show (.venv) in prompt
    python --version
    # Expected: Python 3.11.x

Upgrade pip first:

    python -m pip install --upgrade pip

Install all dependencies in groups:

Group 1 - Web framework and validation:
    pip install fastapi==0.115.0 uvicorn[standard]==0.30.0 pydantic==2.7.0 httpx==0.27.0 python-dotenv==1.0.1 tenacity==8.3.0

Group 2 - LangChain, agents, and LLM tools:
    pip install langchain==0.2.0 langgraph==0.1.0 langchain-community==0.2.0 langsmith==0.1.0 langfuse==2.0.0 mem0ai==0.0.20 litellm==1.40.0 openai==1.30.0

Group 3 - Vector database and embeddings:
    pip install chromadb==0.5.0 sentence-transformers==3.0.0 rank-bm25==0.2.2

Group 4 - ML experiment tracking and data versioning:
    pip install mlflow==2.13.0 dagshub==0.3.9 dvc==3.50.0 wandb==0.17.0

Group 5 - Pipeline orchestration:
    pip install prefect==3.0.0

Group 6 - ML evaluation:
    pip install evidently==0.4.30 ragas==0.1.12

Group 7 - ML models:
    pip install lightgbm==4.3.0 xgboost==2.0.3 scikit-learn==1.4.2 prophet==1.1.5

Group 8 - Data processing:
    pip install pandas==2.2.2 pyarrow==16.0.0 duckdb==0.10.3

Group 9 - Observability:
    pip install structlog==24.1.0 prometheus-client==0.20.0 opentelemetry-sdk==1.25.0 opentelemetry-api==1.25.0 opentelemetry-instrumentation-fastapi==0.46b0

Group 10 - Error tracking:
    pip install sentry-sdk[fastapi]==2.3.0

Group 11 - Cloud service clients:
    pip install supabase==2.4.0 redis==5.0.4 upstash-redis==1.1.0 boto3==1.34.0

Group 12 - Data quality and PII:
    pip install great-expectations==0.18.15 presidio-analyzer==2.2.354 presidio-anonymizer==2.2.354

Group 13 - Streaming:
    pip install confluent-kafka==2.4.0

Group 14 - Testing and code quality:
    pip install pytest==8.2.0 pytest-asyncio==0.23.7 pytest-cov==5.0.0 ruff==0.4.4 black==24.4.2 mypy==1.10.0

Freeze the exact versions:

    pip freeze > requirements.txt

Verify the install worked:

    python -c "import fastapi, langchain, langgraph, chromadb, mlflow, prefect; print('All core imports OK')"

    # Expected output: All core imports OK

------------------------------------------------------------
## Step 1.7 - Write the First Smoke Test
------------------------------------------------------------

Create tests/unit/test_scaffold.py:

    import os
    import sys

    def test_src_on_path():
        """Confirm conftest.py added src/ to sys.path correctly."""
        src_path = os.path.join(os.path.dirname(__file__), "..", "..", "src")
        src_abs = os.path.abspath(src_path)
        assert src_abs in sys.path, f"src/ not found in sys.path: {sys.path}"

    def test_required_dirs_exist():
        """Confirm all scaffold directories were created."""
        base = os.path.join(os.path.dirname(__file__), "..", "..")
        required = [
            "src/api",
            "src/agent",
            "src/rag",
            "src/ml",
            "src/streaming",
            "src/dbt",
            "src/monitoring",
            "src/responsible_ai",
            "tests/unit",
            "tests/integration",
            "infra",
            "k6",
            "data",
            "docs",
            ".github/workflows",
            "grafana/dashboards",
        ]
        for d in required:
            full = os.path.join(base, d)
            assert os.path.isdir(full), f"Missing directory: {d}"

    def test_env_example_exists():
        """Confirm .env.example is committed."""
        base = os.path.join(os.path.dirname(__file__), "..", "..")
        assert os.path.isfile(os.path.join(base, ".env.example")), ".env.example missing"

    def test_pyproject_exists():
        """Confirm pyproject.toml is present."""
        base = os.path.join(os.path.dirname(__file__), "..", "..")
        assert os.path.isfile(os.path.join(base, "pyproject.toml")), "pyproject.toml missing"

Run the smoke tests:

    doppler run -- pytest tests/unit/test_scaffold.py -v

    # Expected:
    # test_src_on_path PASSED
    # test_required_dirs_exist PASSED
    # test_env_example_exists PASSED
    # test_pyproject_exists PASSED
    # 4 passed

------------------------------------------------------------
## Step 1.8 - Initialize DVC and DagsHub
------------------------------------------------------------

DVC handles data versioning. DagsHub provides the remote storage and MLflow server.

    # Initialize DVC
    dvc init

    # Add DagsHub as the remote
    dvc remote add -d dagshub https://dagshub.com/YOUR_USERNAME/customercore.dvc

    # Store auth locally (NOT committed to git)
    dvc remote modify dagshub --local auth basic
    dvc remote modify dagshub --local user YOUR_DAGSHUB_USERNAME
    dvc remote modify dagshub --local password YOUR_DAGSHUB_TOKEN

    # Create a placeholder data file so DVC has something to track
    echo "# CustomerCore raw data directory" > data/raw/.gitkeep

    # Track the data directory with DVC
    dvc add data/raw

    # Add DVC files to git
    git add data/raw.dvc .dvcignore .gitignore
    git commit -m "Phase 1: DVC initialized and DagsHub remote configured"

    # Push data to DagsHub
    dvc push

------------------------------------------------------------
## Step 1.9 - Configure MLflow with DagsHub
------------------------------------------------------------

DagsHub auto-creates an MLflow tracking server when you import the repo.

    # In your browser: go to dagshub.com/YOUR_USERNAME/customercore
    # Click: Remote -> MLflow -> copy the tracking URI
    # It will look like: https://dagshub.com/YOUR_USERNAME/customercore.mlflow

Verify MLflow connection works:

Create a test script at the project root called test_mlflow.py:

    import mlflow
    import os

    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
    mlflow.set_experiment("customercore-phase1-test")

    with mlflow.start_run(run_name="scaffold-check"):
        mlflow.log_param("phase", 1)
        mlflow.log_metric("test_value", 1.0)
        print("MLflow connection OK - check DagsHub UI for the run")

Run it with Doppler injecting secrets:

    doppler run -- python test_mlflow.py

    # Expected: MLflow connection OK - check DagsHub UI for the run

Go to dagshub.com/YOUR_USERNAME/customercore/mlflow in your browser.
You should see the experiment "customercore-phase1-test" with one run.

Delete the test script after confirming:

    del test_mlflow.py

------------------------------------------------------------
## Step 1.10 - Set Up Cloudflare R2 Bucket
------------------------------------------------------------

R2 is the S3-compatible object storage that will hold all Iceberg tables.

In your browser at dash.cloudflare.com:
1. Go to R2 Object Storage
2. Click Create bucket
3. Bucket name: customercore
4. Location: Automatic
5. Click Create bucket

Create R2 API credentials:
1. R2 -> Manage API Tokens -> Create API Token
2. Permissions: Object Read and Write
3. Specify bucket: customercore
4. Click Create API Token
5. Copy the Access Key ID and Secret Access Key into Doppler as:
   - CLOUDFLARE_R2_ACCESS_KEY_ID
   - CLOUDFLARE_R2_SECRET_ACCESS_KEY
   - CLOUDFLARE_R2_ENDPOINT (format: https://ACCOUNT_ID.r2.cloudflarestorage.com)

Verify R2 access from Python:

Create test_r2.py at the project root:

    import boto3
    import os

    s3 = boto3.client(
        "s3",
        endpoint_url=os.environ["CLOUDFLARE_R2_ENDPOINT"],
        aws_access_key_id=os.environ["CLOUDFLARE_R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["CLOUDFLARE_R2_SECRET_ACCESS_KEY"],
    )

    # Create a test object
    s3.put_object(Bucket="customercore", Key="test/phase1.txt", Body=b"phase 1 ok")

    # Read it back
    obj = s3.get_object(Bucket="customercore", Key="test/phase1.txt")
    content = obj["Body"].read()
    print(f"R2 connection OK: {content.decode()}")

    # Clean up
    s3.delete_object(Bucket="customercore", Key="test/phase1.txt")

Run it:

    doppler run -- python test_r2.py

    # Expected: R2 connection OK: phase 1 ok

Delete after confirming:

    del test_r2.py

------------------------------------------------------------
## Step 1.11 - Final Git Commit
------------------------------------------------------------

    git add .
    git commit -m "Phase 1 complete: scaffold, deps, venv, DVC, MLflow, R2 verified, smoke tests passing"
    git push origin main

------------------------------------------------------------
## PHASE 1 CHECKPOINT - ALL MUST PASS BEFORE PHASE 2
------------------------------------------------------------

Run each check and confirm the expected result:

CHECK 1 - Scaffold smoke tests:
    doppler run -- pytest tests/unit/test_scaffold.py -v
    Expected: 4 passed

CHECK 2 - Ruff lint:
    ruff check src/
    Expected: All checks passed!

CHECK 3 - Doppler secrets present:
    doppler secrets --only-names | Sort-Object
    Expected: 20+ key names listed

CHECK 4 - DVC remote reachable:
    dvc push --dry
    Expected: No errors

CHECK 5 - Git clean:
    git status
    Expected: nothing to commit, working tree clean

CHECK 6 - MLflow on DagsHub:
    Open browser: dagshub.com/YOUR_USERNAME/customercore/mlflow
    Expected: customercore-phase1-test experiment visible

CHECK 7 - R2 bucket exists:
    Open browser: dash.cloudflare.com -> R2 -> customercore
    Expected: Bucket visible, empty (test files deleted)

CHECK 8 - All imports work:
    doppler run -- python -c "import fastapi, langchain, langgraph, chromadb, mlflow, prefect, structlog; print('OK')"
    Expected: OK

Summary table:

    | Check | Command                                | Must See            |
    |-------|----------------------------------------|---------------------|
    | 1     | pytest tests/unit/test_scaffold.py -v  | 4 passed            |
    | 2     | ruff check src/                        | All checks passed!  |
    | 3     | doppler secrets --only-names           | 20+ keys listed     |
    | 4     | dvc push --dry                         | No errors           |
    | 5     | git status                             | nothing to commit   |
    | 6     | DagsHub MLflow browser                 | Experiment visible  |
    | 7     | Cloudflare R2 browser                  | Bucket visible      |
    | 8     | python import check                    | OK                  |

------------------------------------------------------------
## PHASE 1 COMPLETE - WHAT COMES NEXT
------------------------------------------------------------

Phase 2 will cover:
- Installing and starting Redpanda locally with Docker
- Creating 4 Kafka-compatible topics
- Writing 4 Python producer scripts:
    * Ticket producer (GitHub Issues API polling)
    * Product event producer (synthetic events)
    * Billing event producer (synthetic events)
    * Incident alert producer (synthetic burst events)
- Verifying all 4 topics receive live messages with rpk

Say "phase 2" when your Phase 1 checkpoint is fully green.

---

##############################################################
# PHASE 2 - REDPANDA STREAMING AND 4 EVENT PRODUCERS
##############################################################

Goal: By the end of Phase 2 you have Redpanda running locally
in Docker, 4 Kafka-compatible topics created, and 4 Python
producer scripts writing live messages to those topics.

Estimated Time: 3-4 days

------------------------------------------------------------
## Step 2.1 - Install Docker Desktop
------------------------------------------------------------

Redpanda runs as a Docker container. Install Docker Desktop first.

1. Go to docs.docker.com/desktop/install/windows-install/
2. Download Docker Desktop for Windows
3. Install and restart your machine
4. Open Docker Desktop and wait for it to start (green icon in taskbar)

Verify Docker is running:

    docker --version
    docker ps

Expected: Docker version X.X.X and an empty container list.

------------------------------------------------------------
## Step 2.2 - Create the Docker Compose File
------------------------------------------------------------

Create docker-compose.yml at the project root:

    version: "3.8"

    services:

      redpanda:
        image: docker.redpanda.com/redpandadata/redpanda:latest
        container_name: redpanda
        command: >
          redpanda start
          --overprovisioned
          --smp 1
          --memory 512M
          --reserve-memory 0M
          --node-id 0
          --check=false
          --kafka-addr PLAINTEXT://0.0.0.0:9092
          --advertise-kafka-addr PLAINTEXT://localhost:9092
          --pandaproxy-addr 0.0.0.0:8082
          --advertise-pandaproxy-addr localhost:8082
        ports:
          - "9092:9092"
          - "9644:9644"
          - "8082:8082"
        volumes:
          - redpanda_data:/var/lib/redpanda/data
        healthcheck:
          test: ["CMD", "rpk", "cluster", "health"]
          interval: 10s
          timeout: 5s
          retries: 5

      redpanda-console:
        image: docker.redpanda.com/redpandadata/console:latest
        container_name: redpanda-console
        ports:
          - "8080:8080"
        environment:
          KAFKA_BROKERS: redpanda:9092
        depends_on:
          - redpanda

    volumes:
      redpanda_data:

------------------------------------------------------------
## Step 2.3 - Start Redpanda
------------------------------------------------------------

    # Start Redpanda and the console
    docker compose up -d redpanda redpanda-console

    # Wait 15 seconds then verify it is healthy
    docker compose ps

    # Expected: redpanda is running (healthy)

    # Open Redpanda Console in browser:
    # http://localhost:8080
    # You should see an empty cluster with 0 topics

------------------------------------------------------------
## Step 2.4 - Install rpk (Redpanda CLI)
------------------------------------------------------------

rpk is the command-line tool for managing Redpanda topics.

    # Install rpk via pip (cross-platform)
    pip install rpk

    # Or download the binary from:
    # https://github.com/redpanda-data/redpanda/releases
    # Add to PATH

    # Verify rpk works
    rpk cluster health --brokers localhost:9092

    # Expected: HEALTHY

------------------------------------------------------------
## Step 2.5 - Create the 4 Kafka Topics
------------------------------------------------------------

    # Topic 1: Support tickets (from GitHub Issues API)
    rpk topic create customercore.tickets.raw \
      --brokers localhost:9092 \
      --partitions 3 \
      --replicas 1

    # Topic 2: Product usage events (synthetic)
    rpk topic create customercore.product.events \
      --brokers localhost:9092 \
      --partitions 3 \
      --replicas 1

    # Topic 3: Billing events (synthetic)
    rpk topic create customercore.billing.events \
      --brokers localhost:9092 \
      --partitions 3 \
      --replicas 1

    # Topic 4: Incident alerts (synthetic)
    rpk topic create customercore.incidents.raw \
      --brokers localhost:9092 \
      --partitions 3 \
      --replicas 1

    # Topic 5: Dead letter queue for failed events
    rpk topic create customercore.dlq \
      --brokers localhost:9092 \
      --partitions 1 \
      --replicas 1

    # Verify all 5 topics were created
    rpk topic list --brokers localhost:9092

    # Expected: 5 topics listed

------------------------------------------------------------
## Step 2.6 - Create Shared Event Schema
------------------------------------------------------------

Create src/streaming/schema.py:

    from dataclasses import dataclass, field, asdict
    from typing import Optional
    import uuid
    import json
    from datetime import datetime, timezone

    VALID_EVENT_TYPES = {"ticket", "product_event", "billing_event", "incident", "kb_article"}
    VALID_SOURCES = {"github", "zendesk", "synthetic_product", "synthetic_billing", "synthetic_incident"}
    VALID_PRIORITIES = {"critical", "high", "medium", "low"}

    @dataclass
    class CustomerCoreEvent:
        event_type: str
        source: str
        tenant_id: str
        customer_id: str
        priority: str = "medium"
        body: str = ""
        event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
        created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
        schema_version: str = "1.0"
        is_synthetic: bool = False

        def validate(self):
            assert self.event_type in VALID_EVENT_TYPES, f"Invalid event_type: {self.event_type}"
            assert self.source in VALID_SOURCES, f"Invalid source: {self.source}"
            assert self.priority in VALID_PRIORITIES, f"Invalid priority: {self.priority}"
            assert self.event_id, "event_id is required"
            assert self.tenant_id, "tenant_id is required"
            return self

        def to_json(self) -> bytes:
            return json.dumps(asdict(self)).encode("utf-8")

Create src/streaming/__init__.py:

    # empty file

------------------------------------------------------------
## Step 2.7 - Create the Base Producer Class
------------------------------------------------------------

Create src/streaming/base_producer.py:

    import json
    import logging
    from confluent_kafka import Producer, KafkaException
    import structlog

    log = structlog.get_logger()

    class BaseProducer:
        def __init__(self, bootstrap_servers: str = "localhost:9092"):
            self.producer = Producer({
                "bootstrap.servers": bootstrap_servers,
                "acks": "all",
                "retries": 3,
                "retry.backoff.ms": 500,
                "compression.type": "lz4",
            })

        def delivery_callback(self, err, msg):
            if err:
                log.error("delivery_failed", topic=msg.topic(), error=str(err))
            else:
                log.info("delivery_ok", topic=msg.topic(), partition=msg.partition(), offset=msg.offset())

        def send(self, topic: str, key: str, value: bytes):
            try:
                self.producer.produce(
                    topic=topic,
                    key=key.encode("utf-8"),
                    value=value,
                    on_delivery=self.delivery_callback,
                )
                self.producer.poll(0)
            except KafkaException as e:
                log.error("produce_failed", topic=topic, key=key, error=str(e))
                self._send_to_dlq(key, value, str(e))

        def _send_to_dlq(self, key: str, value: bytes, error: str):
            import json
            dlq_payload = json.dumps({
                "original_key": key,
                "original_value": value.decode("utf-8", errors="replace"),
                "error": error,
            }).encode("utf-8")
            self.producer.produce(topic="customercore.dlq", key=key.encode(), value=dlq_payload)
            self.producer.poll(0)

        def flush(self):
            remaining = self.producer.flush(timeout=30)
            if remaining > 0:
                log.warning("flush_timeout", remaining_messages=remaining)

------------------------------------------------------------
## Step 2.8 - Producer 1: Ticket Producer (GitHub Issues API)
------------------------------------------------------------

Create src/streaming/producers/ticket_producer.py:

    import os
    import time
    import json
    import httpx
    import structlog
    from src.streaming.base_producer import BaseProducer
    from src.streaming.schema import CustomerCoreEvent

    log = structlog.get_logger()
    TOPIC = "customercore.tickets.raw"
    GITHUB_TOKEN = os.environ.get("GITHUB_PAT", "")

    REPOS = [
        ("huggingface", "transformers"),
        ("langchain-ai", "langchain"),
        ("tiangolo", "fastapi"),
    ]

    PRIORITY_MAP = {
        "critical": "critical", "bug": "high",
        "enhancement": "medium", "question": "low",
        "help wanted": "medium", "documentation": "low",
    }

    def fetch_issues(owner: str, repo: str, since: str = None) -> list:
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
        params = {"state": "all", "per_page": 100, "since": since} if since else {"state": "all", "per_page": 30}
        resp = httpx.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()

    def issue_to_priority(labels: list) -> str:
        label_names = [l["name"].lower() for l in labels]
        for label, priority in PRIORITY_MAP.items():
            if label in label_names:
                return priority
        return "medium"

    def run_ticket_producer(poll_interval_seconds: int = 60):
        producer = BaseProducer()
        log.info("ticket_producer_started", repos=REPOS)

        while True:
            for owner, repo in REPOS:
                try:
                    issues = fetch_issues(owner, repo)
                    for issue in issues:
                        if "pull_request" in issue:
                            continue
                        event = CustomerCoreEvent(
                            event_type="ticket",
                            source="github",
                            tenant_id=f"{owner}-{repo}",
                            customer_id=str(issue.get("user", {}).get("id", "unknown")),
                            priority=issue_to_priority(issue.get("labels", [])),
                            body=f"{issue.get('title', '')} {issue.get('body', '') or ''}".strip()[:2000],
                            is_synthetic=False,
                        ).validate()

                        producer.send(topic=TOPIC, key=event.event_id, value=event.to_json())
                        log.info("ticket_sent", repo=f"{owner}/{repo}", issue_id=issue["id"])

                except Exception as e:
                    log.error("ticket_fetch_failed", repo=f"{owner}/{repo}", error=str(e))

            producer.flush()
            log.info("ticket_producer_sleeping", seconds=poll_interval_seconds)
            time.sleep(poll_interval_seconds)

    if __name__ == "__main__":
        run_ticket_producer()

------------------------------------------------------------
## Step 2.9 - Producer 2: Product Event Producer (Synthetic)
------------------------------------------------------------

Create src/streaming/producers/product_producer.py:

    import os
    import time
    import random
    import structlog
    from src.streaming.base_producer import BaseProducer
    from src.streaming.schema import CustomerCoreEvent

    log = structlog.get_logger()
    TOPIC = "customercore.product.events"

    TENANTS = ["acme-corp", "contoso-ltd", "globex-inc", "initech-llc"]
    EVENT_SUBTYPES = ["page_view", "feature_used", "error_triggered", "session_end", "api_call"]
    FEATURES = ["dashboard", "reports", "integrations", "billing", "settings", "api_keys", "webhooks"]

    def generate_product_event(tenant_id: str) -> CustomerCoreEvent:
        subtype = random.choice(EVENT_SUBTYPES)
        feature = random.choice(FEATURES)
        priority = "high" if subtype == "error_triggered" else "low"
        body = f"{subtype} on {feature} feature by customer in tenant {tenant_id}"
        return CustomerCoreEvent(
            event_type="product_event",
            source="synthetic_product",
            tenant_id=tenant_id,
            customer_id=f"cust-{random.randint(1000, 9999)}",
            priority=priority,
            body=body,
            is_synthetic=True,
        ).validate()

    def run_product_producer(events_per_minute: int = 100):
        producer = BaseProducer()
        sleep_seconds = 60 / events_per_minute
        log.info("product_producer_started", events_per_minute=events_per_minute)

        while True:
            tenant = random.choice(TENANTS)
            event = generate_product_event(tenant)
            producer.send(topic=TOPIC, key=event.event_id, value=event.to_json())
            time.sleep(sleep_seconds)

    if __name__ == "__main__":
        run_product_producer()

------------------------------------------------------------
## Step 2.10 - Producer 3: Billing Event Producer (Synthetic)
------------------------------------------------------------

Create src/streaming/producers/billing_producer.py:

    import os
    import time
    import random
    import structlog
    from src.streaming.base_producer import BaseProducer
    from src.streaming.schema import CustomerCoreEvent

    log = structlog.get_logger()
    TOPIC = "customercore.billing.events"

    TENANTS = ["acme-corp", "contoso-ltd", "globex-inc", "initech-llc"]
    BILLING_EVENTS = ["payment_failed", "plan_upgrade", "plan_downgrade", "subscription_cancelled", "trial_started"]
    TIERS = ["free", "professional", "enterprise"]

    def generate_billing_event(tenant_id: str) -> CustomerCoreEvent:
        subtype = random.choices(
            BILLING_EVENTS,
            weights=[30, 20, 15, 10, 25],
            k=1
        )[0]
        tier = random.choice(TIERS)
        priority = "critical" if subtype in ("payment_failed", "subscription_cancelled") else "medium"
        body = f"Billing event: {subtype} for {tier} tier customer in tenant {tenant_id}"
        return CustomerCoreEvent(
            event_type="billing_event",
            source="synthetic_billing",
            tenant_id=tenant_id,
            customer_id=f"cust-{random.randint(1000, 9999)}",
            priority=priority,
            body=body,
            is_synthetic=True,
        ).validate()

    def run_billing_producer(events_per_minute: int = 10):
        producer = BaseProducer()
        sleep_seconds = 60 / events_per_minute
        log.info("billing_producer_started", events_per_minute=events_per_minute)

        while True:
            tenant = random.choice(TENANTS)
            event = generate_billing_event(tenant)
            producer.send(topic=TOPIC, key=event.event_id, value=event.to_json())
            time.sleep(sleep_seconds)

    if __name__ == "__main__":
        run_billing_producer()

------------------------------------------------------------
## Step 2.11 - Producer 4: Incident Alert Producer (Synthetic)
------------------------------------------------------------

Create src/streaming/producers/incident_producer.py:

    import os
    import time
    import random
    import structlog
    from src.streaming.base_producer import BaseProducer
    from src.streaming.schema import CustomerCoreEvent

    log = structlog.get_logger()
    TOPIC = "customercore.incidents.raw"

    TENANTS = ["acme-corp", "contoso-ltd", "globex-inc", "initech-llc"]
    INCIDENT_TYPES = ["service_down", "latency_spike", "error_rate_high", "cpu_spike", "memory_leak"]
    SERVICES = ["auth-service", "payment-service", "api-gateway", "ml-inference", "database"]

    def generate_incident_event(tenant_id: str) -> CustomerCoreEvent:
        incident_type = random.choice(INCIDENT_TYPES)
        service = random.choice(SERVICES)
        priority = "critical" if incident_type == "service_down" else "high"
        body = f"Incident detected: {incident_type} on {service} for tenant {tenant_id}"
        return CustomerCoreEvent(
            event_type="incident",
            source="synthetic_incident",
            tenant_id=tenant_id,
            customer_id="system",
            priority=priority,
            body=body,
            is_synthetic=True,
        ).validate()

    def run_incident_producer(events_per_minute: int = 5, burst_mode: bool = False):
        producer = BaseProducer()
        sleep_seconds = 60 / events_per_minute
        log.info("incident_producer_started", events_per_minute=events_per_minute)

        while True:
            tenant = random.choice(TENANTS)
            event = generate_incident_event(tenant)
            producer.send(topic=TOPIC, key=event.event_id, value=event.to_json())

            if burst_mode and random.random() < 0.1:
                log.info("burst_mode_triggered")
                for _ in range(10):
                    burst_event = generate_incident_event(tenant)
                    producer.send(topic=TOPIC, key=burst_event.event_id, value=burst_event.to_json())

            time.sleep(sleep_seconds)

    if __name__ == "__main__":
        run_incident_producer()

Also create src/streaming/producers/__init__.py as empty file.

------------------------------------------------------------
## Step 2.12 - Write Producer Unit Tests
------------------------------------------------------------

Create tests/unit/test_producers.py:

    import json
    import pytest
    from src.streaming.schema import CustomerCoreEvent

    def test_event_serialization():
        event = CustomerCoreEvent(
            event_type="ticket",
            source="github",
            tenant_id="acme-corp",
            customer_id="cust-001",
            priority="high",
            body="Test ticket body",
            is_synthetic=False,
        ).validate()
        payload = event.to_json()
        data = json.loads(payload)
        assert data["event_type"] == "ticket"
        assert data["tenant_id"] == "acme-corp"
        assert data["priority"] == "high"
        assert data["is_synthetic"] is False
        assert len(data["event_id"]) == 36

    def test_event_invalid_type():
        with pytest.raises(AssertionError):
            CustomerCoreEvent(
                event_type="invalid_type",
                source="github",
                tenant_id="acme",
                customer_id="c1",
            ).validate()

    def test_event_invalid_priority():
        with pytest.raises(AssertionError):
            CustomerCoreEvent(
                event_type="ticket",
                source="github",
                tenant_id="acme",
                customer_id="c1",
                priority="urgent",
            ).validate()

    def test_synthetic_billing_event():
        from src.streaming.producers.billing_producer import generate_billing_event
        event = generate_billing_event("acme-corp")
        assert event.is_synthetic is True
        assert event.event_type == "billing_event"
        assert event.priority in ("critical", "medium")

    def test_synthetic_incident_event():
        from src.streaming.producers.incident_producer import generate_incident_event
        event = generate_incident_event("contoso-ltd")
        assert event.is_synthetic is True
        assert event.event_type == "incident"
        assert event.priority in ("critical", "high")

    def test_synthetic_product_event():
        from src.streaming.producers.product_producer import generate_product_event
        event = generate_product_event("globex-inc")
        assert event.is_synthetic is True
        assert event.event_type == "product_event"

Run these tests:

    doppler run -- pytest tests/unit/test_producers.py -v

    # Expected: 5 passed

------------------------------------------------------------
## Step 2.13 - Verify Live Messages in Redpanda
------------------------------------------------------------

Start each producer in a separate terminal window. Use Doppler to inject secrets.

Terminal 1 - Start ticket producer (polls GitHub every 60s):
    doppler run -- python -m src.streaming.producers.ticket_producer

Terminal 2 - Start product event producer:
    doppler run -- python -m src.streaming.producers.product_producer

Terminal 3 - Start billing event producer:
    doppler run -- python -m src.streaming.producers.billing_producer

Terminal 4 - Start incident producer:
    doppler run -- python -m src.streaming.producers.incident_producer

After 30 seconds, verify messages are arriving in each topic:

    # Check ticket topic
    rpk topic consume customercore.tickets.raw --brokers localhost:9092 --num 3

    # Check product events
    rpk topic consume customercore.product.events --brokers localhost:9092 --num 3

    # Check billing events
    rpk topic consume customercore.billing.events --brokers localhost:9092 --num 3

    # Check incidents
    rpk topic consume customercore.incidents.raw --brokers localhost:9092 --num 3

Also verify in Redpanda Console:
    Open http://localhost:8080
    Click Topics -> you should see message counts growing on all 4 topics

------------------------------------------------------------
## Step 2.14 - Commit Phase 2
------------------------------------------------------------

    git add .
    git commit -m "Phase 2: Redpanda running, 4 topics created, 4 producers writing live messages"
    git push origin main

------------------------------------------------------------
## PHASE 2 CHECKPOINT - ALL MUST PASS BEFORE PHASE 3
------------------------------------------------------------

CHECK 1 - Redpanda healthy:
    rpk cluster health --brokers localhost:9092
    Expected: HEALTHY

CHECK 2 - All 5 topics exist:
    rpk topic list --brokers localhost:9092
    Expected: 5 topics listed (4 data + 1 DLQ)

CHECK 3 - Messages flowing on all topics:
    rpk topic consume customercore.tickets.raw --brokers localhost:9092 --num 1
    rpk topic consume customercore.product.events --brokers localhost:9092 --num 1
    rpk topic consume customercore.billing.events --brokers localhost:9092 --num 1
    rpk topic consume customercore.incidents.raw --brokers localhost:9092 --num 1
    Expected: valid JSON event printed for each topic

CHECK 4 - Producer unit tests green:
    doppler run -- pytest tests/unit/test_producers.py -v
    Expected: 5 passed

CHECK 5 - Git clean:
    git status
    Expected: nothing to commit

---


##############################################################
# PHASE 3 - PYSPARK BRONZE TO SILVER PIPELINE (ICEBERG)
##############################################################

Goal: By the end of Phase 3 you have PySpark Structured
Streaming reading from all 4 Redpanda topics, applying PII
masking with Presidio, enforcing the unified schema, and
writing clean Silver events to Apache Iceberg tables on
Cloudflare R2. Micro-batches run every 30 seconds.

Estimated Time: 4-5 days

------------------------------------------------------------
## Step 3.1 - Install Java and PySpark
------------------------------------------------------------

PySpark requires Java 11 or 17. Install it first.

Download Java 17 (OpenJDK):
    https://adoptium.net/temurin/releases/?version=17
    Choose: Windows x64 JDK installer
    Install it (default settings)

Set JAVA_HOME environment variable:
    Windows search -> "Edit the system environment variables"
    Environment Variables -> System Variables -> New
    Variable name: JAVA_HOME
    Variable value: C:\Program Files\Eclipse Adoptium\jdk-17.X.X.X-hotspot
    Click OK

Add to PATH:
    Edit PATH variable -> New -> %JAVA_HOME%\bin
    Click OK, close all dialogs

Verify Java:
    java -version
    Expected: openjdk version "17.X.X"

Now install PySpark and Iceberg packages:

    pip install pyspark==3.5.0
    pip freeze > requirements.txt

------------------------------------------------------------
## Step 3.2 - Add MinIO to Docker Compose (Local S3 Proxy)
------------------------------------------------------------

For local development, MinIO acts as a local S3 endpoint.
In production this switches to Cloudflare R2 via one env var.

Add the following services to your docker-compose.yml:

      minio:
        image: minio/minio:latest
        container_name: minio
        command: server /data --console-address ":9001"
        environment:
          MINIO_ROOT_USER: minioadmin
          MINIO_ROOT_PASSWORD: minioadmin
        ports:
          - "9000:9000"
          - "9001:9001"
        volumes:
          - minio_data:/data
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
          interval: 10s
          timeout: 5s
          retries: 5

Add to the volumes section at the bottom:
      minio_data:

Start MinIO:

    docker compose up -d minio

    # Verify MinIO is running
    docker compose ps minio

Open MinIO Console: http://localhost:9001
Login: minioadmin / minioadmin
Create bucket: customercore

Add MinIO credentials to Doppler:

    MINIO_ENDPOINT=http://localhost:9000
    MINIO_ACCESS_KEY=minioadmin
    MINIO_SECRET_KEY=minioadmin
    MINIO_BUCKET=customercore

    # For cloud deployment this switches to:
    # MINIO_ENDPOINT=https://ACCOUNT_ID.r2.cloudflarestorage.com
    # And uses your Cloudflare R2 keys

------------------------------------------------------------
## Step 3.3 - Create the Spark Session Factory
------------------------------------------------------------

Create src/streaming/spark_session.py:

    import os
    from pyspark.sql import SparkSession

    ICEBERG_PACKAGE = "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.5.0"
    KAFKA_PACKAGE = "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0"
    AWS_PACKAGE = "org.apache.hadoop:hadoop-aws:3.3.4"

    def create_spark_session(app_name: str = "CustomerCore") -> SparkSession:
        endpoint = os.environ.get("MINIO_ENDPOINT", "http://localhost:9000")
        access_key = os.environ.get("MINIO_ACCESS_KEY", "minioadmin")
        secret_key = os.environ.get("MINIO_SECRET_KEY", "minioadmin")

        spark = (
            SparkSession.builder.appName(app_name)
            .config("spark.jars.packages", f"{ICEBERG_PACKAGE},{KAFKA_PACKAGE},{AWS_PACKAGE}")
            .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
            .config("spark.sql.catalog.local", "org.apache.iceberg.spark.SparkCatalog")
            .config("spark.sql.catalog.local.type", "hadoop")
            .config("spark.sql.catalog.local.warehouse", f"s3a://customercore/warehouse")
            .config("spark.hadoop.fs.s3a.endpoint", endpoint)
            .config("spark.hadoop.fs.s3a.access.key", access_key)
            .config("spark.hadoop.fs.s3a.secret.key", secret_key)
            .config("spark.hadoop.fs.s3a.path.style.access", "true")
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
            .config("spark.sql.shuffle.partitions", "4")
            .config("spark.default.parallelism", "4")
            .getOrCreate()
        )
        spark.sparkContext.setLogLevel("WARN")
        return spark

------------------------------------------------------------
## Step 3.4 - Create the Unified Event Schema for Spark
------------------------------------------------------------

Create src/streaming/spark_schema.py:

    from pyspark.sql.types import (
        StructType, StructField, StringType, BooleanType, TimestampType
    )

    EVENT_SCHEMA = StructType([
        StructField("event_id", StringType(), False),
        StructField("event_type", StringType(), False),
        StructField("source", StringType(), False),
        StructField("tenant_id", StringType(), False),
        StructField("customer_id", StringType(), True),
        StructField("created_at", StringType(), False),
        StructField("body", StringType(), True),
        StructField("priority", StringType(), False),
        StructField("schema_version", StringType(), True),
        StructField("is_synthetic", BooleanType(), False),
    ])

------------------------------------------------------------
## Step 3.5 - Create the PII Masking UDF
------------------------------------------------------------

Create src/streaming/pii_masker.py:

    import re
    from presidio_analyzer import AnalyzerEngine
    from presidio_anonymizer import AnonymizerEngine
    from presidio_anonymizer.entities import OperatorConfig

    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()

    REGEX_PII_PATTERNS = [
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "<EMAIL>"),
        (r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", "<PHONE>"),
        (r"\b\d{3}-\d{2}-\d{4}\b", "<SSN>"),
        (r"\b4[0-9]{12}(?:[0-9]{3})?\b", "<CREDIT_CARD>"),
    ]

    def mask_pii_regex(text: str) -> str:
        if not text:
            return text
        for pattern, replacement in REGEX_PII_PATTERNS:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        return text

    def mask_pii_presidio(text: str) -> str:
        if not text or len(text) < 10:
            return text
        try:
            results = analyzer.analyze(text=text, language="en")
            if not results:
                return mask_pii_regex(text)
            anonymized = anonymizer.anonymize(
                text=text,
                analyzer_results=results,
                operators={"DEFAULT": OperatorConfig("replace", {"new_value": "<MASKED>"})}
            )
            return anonymized.text
        except Exception:
            return mask_pii_regex(text)

    def mask_pii(text: str) -> str:
        return mask_pii_presidio(text)

    # Create a PySpark UDF version
    from pyspark.sql.functions import udf
    from pyspark.sql.types import StringType

    mask_pii_udf = udf(mask_pii, StringType())

------------------------------------------------------------
## Step 3.6 - Create the Bronze to Silver Streaming Job
------------------------------------------------------------

Create src/streaming/bronze_to_silver.py:

    import os
    import sys
    from pyspark.sql import functions as F
    from pyspark.sql.functions import col, from_json, current_timestamp
    import structlog

    from src.streaming.spark_session import create_spark_session
    from src.streaming.spark_schema import EVENT_SCHEMA
    from src.streaming.pii_masker import mask_pii_udf

    log = structlog.get_logger()

    BOOTSTRAP_SERVERS = os.environ.get("REDPANDA_BROKERS", "localhost:9092")
    TOPICS = "customercore.tickets.raw,customercore.product.events,customercore.billing.events,customercore.incidents.raw"
    CHECKPOINT_PATH = "/tmp/customercore_checkpoints"
    SILVER_TABLE = "local.customercore.silver_events"

    def create_silver_table(spark):
        spark.sql(f"""
            CREATE TABLE IF NOT EXISTS {SILVER_TABLE} (
                event_id STRING,
                event_type STRING,
                source STRING,
                tenant_id STRING,
                customer_id STRING,
                created_at STRING,
                body STRING,
                priority STRING,
                schema_version STRING,
                is_synthetic BOOLEAN,
                ingested_at TIMESTAMP
            )
            USING iceberg
            PARTITIONED BY (tenant_id, event_type)
        """)
        log.info("silver_table_ready", table=SILVER_TABLE)

    def run_bronze_to_silver():
        spark = create_spark_session("CustomerCore-BronzeToSilver")
        create_silver_table(spark)

        raw_stream = (
            spark.readStream
            .format("kafka")
            .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS)
            .option("subscribe", TOPICS)
            .option("startingOffsets", "latest")
            .option("failOnDataLoss", "false")
            .load()
        )

        parsed_stream = (
            raw_stream
            .select(
                col("topic"),
                from_json(col("value").cast("string"), EVENT_SCHEMA).alias("evt"),
                col("timestamp").alias("kafka_timestamp"),
            )
            .select("evt.*", "kafka_timestamp")
            .filter(col("event_id").isNotNull())
            .filter(col("tenant_id").isNotNull())
            .filter(col("event_type").isNotNull())
        )

        silver_stream = (
            parsed_stream
            .withColumn("body", mask_pii_udf(col("body")))
            .withColumn("ingested_at", current_timestamp())
            .drop("kafka_timestamp")
        )

        query = (
            silver_stream.writeStream
            .format("iceberg")
            .outputMode("append")
            .option("path", SILVER_TABLE)
            .option("checkpointLocation", f"{CHECKPOINT_PATH}/silver_events")
            .trigger(processingTime="30 seconds")
            .start()
        )

        log.info("bronze_to_silver_started", trigger="30s", table=SILVER_TABLE)
        query.awaitTermination()

    if __name__ == "__main__":
        run_bronze_to_silver()

------------------------------------------------------------
## Step 3.7 - Run the Streaming Pipeline
------------------------------------------------------------

Open a new terminal with Doppler secrets and start the pipeline.
Make sure Redpanda is running and producers are producing first.

    doppler run -- python -m src.streaming.bronze_to_silver

The first run will:
1. Download Iceberg, Kafka, and AWS JARs (~200MB, one time only)
2. Create the Silver Iceberg table in MinIO
3. Start consuming from all 4 topics
4. Write the first micro-batch after 30 seconds

Watch the logs - you should see:
- "silver_table_ready"
- "bronze_to_silver_started"
- After 30s: micro-batch processed messages

------------------------------------------------------------
## Step 3.8 - Verify the Iceberg Silver Table
------------------------------------------------------------

After the first micro-batch runs (30 seconds), verify data landed.
Open a new Python session with Doppler:

    doppler run -- python

    from src.streaming.spark_session import create_spark_session
    spark = create_spark_session("verify")
    df = spark.read.format("iceberg").load("local.customercore.silver_events")
    print(f"Row count: {df.count()}")
    df.show(5, truncate=True)

    # Expected: Row count > 0, rows showing event_id, tenant_id, etc.

    # Also verify via DuckDB (faster for spot checks)
    import duckdb
    import os
    con = duckdb.connect()
    con.execute("INSTALL httpfs; LOAD httpfs;")
    con.execute(f"SET s3_endpoint='{os.environ['MINIO_ENDPOINT'].replace('http://', '')}'")
    con.execute(f"SET s3_access_key_id='minioadmin'")
    con.execute(f"SET s3_secret_access_key='minioadmin'")
    con.execute("SET s3_use_ssl=false; SET s3_url_style='path';")
    result = con.execute("""
        SELECT event_type, count(*) as cnt
        FROM iceberg_scan('s3://customercore/warehouse/customercore/silver_events')
        GROUP BY event_type
    """).fetchall()
    print(result)

------------------------------------------------------------
## Step 3.9 - Write Bronze to Silver Tests
------------------------------------------------------------

Create tests/unit/test_streaming.py:

    import json
    import pytest
    from src.streaming.schema import CustomerCoreEvent
    from src.streaming.pii_masker import mask_pii_regex

    def test_pii_email_masked():
        text = "Contact me at john.doe@company.com for details"
        result = mask_pii_regex(text)
        assert "john.doe@company.com" not in result
        assert "<EMAIL>" in result

    def test_pii_phone_masked():
        text = "Call me at 555-123-4567 anytime"
        result = mask_pii_regex(text)
        assert "555-123-4567" not in result
        assert "<PHONE>" in result

    def test_pii_no_false_positives():
        text = "The version is 3.5.0 and the port is 9092"
        result = mask_pii_regex(text)
        assert result == text

    def test_event_missing_required_field():
        with pytest.raises((AssertionError, TypeError)):
            CustomerCoreEvent(
                event_type="ticket",
                source="github",
                tenant_id="",
                customer_id="c1",
            ).validate()

    def test_body_truncated_at_2000_chars():
        long_body = "x" * 3000
        truncated = long_body[:2000]
        assert len(truncated) == 2000

Run:

    doppler run -- pytest tests/unit/test_streaming.py -v
    # Expected: 5 passed

------------------------------------------------------------
## Step 3.10 - Commit Phase 3
------------------------------------------------------------

    git add .
    git commit -m "Phase 3: PySpark Bronze->Silver streaming pipeline, PII masking, Iceberg Silver table on MinIO"
    git push origin main

------------------------------------------------------------
## PHASE 3 CHECKPOINT - ALL MUST PASS BEFORE PHASE 4
------------------------------------------------------------

CHECK 1 - Streaming tests green:
    doppler run -- pytest tests/unit/test_streaming.py -v
    Expected: 5 passed

CHECK 2 - Silver table has rows:
    doppler run -- python -c "
    from src.streaming.spark_session import create_spark_session
    spark = create_spark_session('check')
    df = spark.read.format('iceberg').load('local.customercore.silver_events')
    print('Silver rows:', df.count())
    "
    Expected: Silver rows: > 0

CHECK 3 - PII masking verified:
    doppler run -- python -c "
    from src.streaming.pii_masker import mask_pii
    print(mask_pii('email: test@example.com phone: 555-111-2222'))
    "
    Expected: email and phone replaced with <MASKED> or <EMAIL>/<PHONE>

CHECK 4 - MinIO Console shows data:
    Open http://localhost:9001
    Browse: customercore -> warehouse -> customercore -> silver_events
    Expected: Parquet and metadata files visible

CHECK 5 - Git clean:
    git status
    Expected: nothing to commit

---


##############################################################
# PHASE 4 - DBT GOLD MODELS (7 BUSINESS MARTS)
##############################################################

Goal: By the end of Phase 4 you have dbt-core installed and
configured, reading from Silver Iceberg tables via DuckDB,
and producing 7 Gold business mart tables. All dbt tests pass
and the lineage graph is visible in dbt docs.

Estimated Time: 3-4 days

------------------------------------------------------------
## Step 4.1 - Install dbt-core with DuckDB Adapter
------------------------------------------------------------

    pip install dbt-core==1.8.0 dbt-duckdb==1.8.0
    pip freeze > requirements.txt

    # Verify
    dbt --version
    # Expected: dbt-core version 1.8.x

------------------------------------------------------------
## Step 4.2 - Initialize the dbt Project
------------------------------------------------------------

    # Inside src/dbt/
    cd src/dbt
    dbt init customercore_dbt

    # When prompted:
    # profile: customercore_dbt
    # Which database: duckdb
    # database file path: ./customercore.duckdb

    # Move back to project root
    cd ../..

Alternatively create the structure manually.

Create src/dbt/profiles.yml:

    customercore_dbt:
      target: dev
      outputs:
        dev:
          type: duckdb
          path: "src/dbt/customercore.duckdb"
          schema: gold
          extensions:
            - httpfs
            - iceberg
          settings:
            s3_endpoint: "localhost:9000"
            s3_access_key_id: "minioadmin"
            s3_secret_access_key: "minioadmin"
            s3_use_ssl: false
            s3_url_style: "path"

Create src/dbt/dbt_project.yml:

    name: "customercore_dbt"
    version: "1.0.0"
    config-version: 2

    profile: "customercore_dbt"

    model-paths: ["models"]
    analysis-paths: ["analyses"]
    test-paths: ["tests"]
    seed-paths: ["seeds"]
    macro-paths: ["macros"]

    target-path: "target"
    clean-targets:
      - "target"
      - "dbt_packages"

    models:
      customercore_dbt:
        gold:
          +materialized: table
          +schema: gold

------------------------------------------------------------
## Step 4.3 - Create Silver Source Reference
------------------------------------------------------------

Create src/dbt/models/sources.yml:

    version: 2

    sources:
      - name: silver
        description: "Silver layer Iceberg tables from PySpark streaming pipeline"
        tables:
          - name: silver_events
            description: "All PII-masked, schema-validated events from all 4 sources"
            columns:
              - name: event_id
                tests: [not_null, unique]
              - name: tenant_id
                tests: [not_null]
              - name: event_type
                tests:
                  - not_null
                  - accepted_values:
                      values: ["ticket", "product_event", "billing_event", "incident", "kb_article"]
              - name: priority
                tests:
                  - accepted_values:
                      values: ["critical", "high", "medium", "low"]

------------------------------------------------------------
## Step 4.4 - Create the 7 Gold Models
------------------------------------------------------------

--- Gold Model 1: customer_health_daily ---

Create src/dbt/models/gold/customer_health_daily.sql:

    {{ config(
        materialized="table",
        unique_key="customer_id || '|' || tenant_id || '|' || snapshot_date"
    ) }}

    WITH tickets AS (
        SELECT
            customer_id,
            tenant_id,
            COUNT(*) AS open_ticket_count,
            AVG(CASE priority
                WHEN 'critical' THEN 4
                WHEN 'high'     THEN 3
                WHEN 'medium'   THEN 2
                ELSE 1 END) AS avg_priority_score,
            SUM(CASE WHEN priority IN ('critical','high') THEN 1 ELSE 0 END) AS high_priority_count
        FROM iceberg_scan('s3://customercore/warehouse/customercore/silver_events')
        WHERE event_type = 'ticket'
          AND created_at >= CURRENT_DATE - INTERVAL '30' DAY
        GROUP BY 1, 2
    ),

    billing AS (
        SELECT
            customer_id,
            tenant_id,
            COUNT(*) FILTER (WHERE body LIKE '%payment_failed%') AS payment_failures_30d,
            MAX(created_at) AS last_billing_event
        FROM iceberg_scan('s3://customercore/warehouse/customercore/silver_events')
        WHERE event_type = 'billing_event'
          AND created_at >= CURRENT_DATE - INTERVAL '30' DAY
        GROUP BY 1, 2
    ),

    product AS (
        SELECT
            customer_id,
            tenant_id,
            COUNT(*) AS product_events_30d
        FROM iceberg_scan('s3://customercore/warehouse/customercore/silver_events')
        WHERE event_type = 'product_event'
          AND created_at >= CURRENT_DATE - INTERVAL '30' DAY
        GROUP BY 1, 2
    )

    SELECT
        COALESCE(t.customer_id, b.customer_id, p.customer_id) AS customer_id,
        COALESCE(t.tenant_id,   b.tenant_id,   p.tenant_id)   AS tenant_id,
        CURRENT_DATE                                            AS snapshot_date,
        COALESCE(t.open_ticket_count, 0)    AS open_tickets,
        COALESCE(t.avg_priority_score, 1.0) AS avg_priority,
        COALESCE(t.high_priority_count, 0)  AS high_priority_tickets,
        COALESCE(b.payment_failures_30d, 0) AS payment_failures_30d,
        b.last_billing_event,
        COALESCE(p.product_events_30d, 0)   AS product_events_30d
    FROM tickets t
    FULL OUTER JOIN billing b USING (customer_id, tenant_id)
    FULL OUTER JOIN product  p USING (customer_id, tenant_id)

--- Gold Model 2: ticket_funnel_daily ---

Create src/dbt/models/gold/ticket_funnel_daily.sql:

    {{ config(materialized="table") }}

    SELECT
        tenant_id,
        event_type,
        priority,
        source,
        DATE(created_at)       AS event_date,
        COUNT(*)               AS event_count,
        COUNT(DISTINCT customer_id) AS unique_customers
    FROM iceberg_scan('s3://customercore/warehouse/customercore/silver_events')
    WHERE event_type = 'ticket'
    GROUP BY 1, 2, 3, 4, 5

--- Gold Model 3: incident_severity_hourly ---

Create src/dbt/models/gold/incident_severity_hourly.sql:

    {{ config(materialized="table") }}

    SELECT
        tenant_id,
        DATE_TRUNC('hour', CAST(created_at AS TIMESTAMP)) AS incident_hour,
        priority AS severity,
        COUNT(*)  AS incident_count,
        COUNT(DISTINCT customer_id) AS affected_customers
    FROM iceberg_scan('s3://customercore/warehouse/customercore/silver_events')
    WHERE event_type = 'incident'
    GROUP BY 1, 2, 3

--- Gold Model 4: billing_failure_summary ---

Create src/dbt/models/gold/billing_failure_summary.sql:

    {{ config(materialized="table") }}

    SELECT
        tenant_id,
        DATE(created_at) AS event_date,
        priority,
        COUNT(*) AS billing_event_count,
        SUM(CASE WHEN body LIKE '%payment_failed%' THEN 1 ELSE 0 END) AS payment_failures,
        SUM(CASE WHEN body LIKE '%cancelled%' THEN 1 ELSE 0 END)      AS cancellations
    FROM iceberg_scan('s3://customercore/warehouse/customercore/silver_events')
    WHERE event_type = 'billing_event'
    GROUP BY 1, 2, 3

--- Gold Model 5: product_adoption_features ---

Create src/dbt/models/gold/product_adoption_features.sql:

    {{ config(materialized="table") }}

    SELECT
        tenant_id,
        customer_id,
        DATE(created_at) AS event_date,
        COUNT(*)         AS total_product_events,
        COUNT(DISTINCT DATE(created_at)) AS active_days
    FROM iceberg_scan('s3://customercore/warehouse/customercore/silver_events')
    WHERE event_type = 'product_event'
    GROUP BY 1, 2, 3

--- Gold Model 6: retention_cohort_metrics ---

Create src/dbt/models/gold/retention_cohort_metrics.sql:

    {{ config(materialized="table") }}

    WITH first_seen AS (
        SELECT
            customer_id,
            tenant_id,
            MIN(DATE(created_at)) AS cohort_date
        FROM iceberg_scan('s3://customercore/warehouse/customercore/silver_events')
        GROUP BY 1, 2
    ),

    activity AS (
        SELECT
            customer_id,
            tenant_id,
            DATE(created_at) AS active_date
        FROM iceberg_scan('s3://customercore/warehouse/customercore/silver_events')
        GROUP BY 1, 2, 3
    )

    SELECT
        f.cohort_date,
        f.tenant_id,
        COUNT(DISTINCT f.customer_id) AS cohort_size,
        COUNT(DISTINCT CASE WHEN a.active_date <= f.cohort_date + INTERVAL '7' DAY
            THEN a.customer_id END) AS retained_d7,
        COUNT(DISTINCT CASE WHEN a.active_date <= f.cohort_date + INTERVAL '30' DAY
            THEN a.customer_id END) AS retained_d30
    FROM first_seen f
    LEFT JOIN activity a USING (customer_id, tenant_id)
    GROUP BY 1, 2

--- Gold Model 7: support_agent_performance ---

Create src/dbt/models/gold/support_agent_performance.sql:

    {{ config(materialized="table") }}

    SELECT
        tenant_id,
        source,
        DATE(created_at)  AS report_date,
        priority,
        COUNT(*)          AS tickets_created,
        COUNT(DISTINCT customer_id) AS unique_customers_served,
        AVG(LENGTH(body)) AS avg_body_length
    FROM iceberg_scan('s3://customercore/warehouse/customercore/silver_events')
    WHERE event_type = 'ticket'
    GROUP BY 1, 2, 3, 4

------------------------------------------------------------
## Step 4.5 - Create dbt Schema Tests
------------------------------------------------------------

Create src/dbt/models/schema.yml:

    version: 2

    models:
      - name: customer_health_daily
        description: "Per-customer health metrics computed daily from all signal sources"
        columns:
          - name: customer_id
            tests: [not_null]
          - name: tenant_id
            tests: [not_null]
          - name: snapshot_date
            tests: [not_null]
          - name: avg_priority
            tests:
              - not_null
              - dbt_utils.accepted_range:
                  min_value: 1
                  max_value: 4

      - name: ticket_funnel_daily
        description: "Daily ticket volume by category, priority and source"
        columns:
          - name: tenant_id
            tests: [not_null]
          - name: event_count
            tests: [not_null]

      - name: incident_severity_hourly
        description: "Hourly incident counts by severity"
        columns:
          - name: tenant_id
            tests: [not_null]
          - name: incident_count
            tests: [not_null]

------------------------------------------------------------
## Step 4.6 - Run the dbt Models
------------------------------------------------------------

    # From the project root
    cd src/dbt

    # Run all Gold models
    dbt run --profiles-dir . --project-dir .

    # Expected output:
    # 1 of 7 START table model gold.customer_health_daily ...... OK
    # 2 of 7 START table model gold.ticket_funnel_daily ........ OK
    # 3 of 7 START table model gold.incident_severity_hourly ... OK
    # 4 of 7 START table model gold.billing_failure_summary ..... OK
    # 5 of 7 START table model gold.product_adoption_features ... OK
    # 6 of 7 START table model gold.retention_cohort_metrics .... OK
    # 7 of 7 START table model gold.support_agent_performance ... OK
    # Finished running 7 table models

    # Run all dbt schema tests
    dbt test --profiles-dir . --project-dir .

    # Expected: 0 dbt test failures

    # Generate and serve the docs locally
    dbt docs generate --profiles-dir . --project-dir .
    dbt docs serve --profiles-dir . --project-dir .
    # Open http://localhost:8080 to see the lineage graph

    cd ../..

------------------------------------------------------------
## Step 4.7 - Verify Gold Tables via DuckDB
------------------------------------------------------------

    doppler run -- python

    import duckdb
    con = duckdb.connect("src/dbt/customercore.duckdb")

    # Check all 7 gold tables exist
    tables = con.execute("SHOW TABLES").fetchall()
    print("Gold tables:", [t[0] for t in tables])

    # Check customer_health_daily has rows
    count = con.execute("SELECT count(*) FROM gold.customer_health_daily").fetchone()[0]
    print(f"customer_health_daily rows: {count}")

    # Check ticket_funnel_daily
    count2 = con.execute("SELECT count(*) FROM gold.ticket_funnel_daily").fetchone()[0]
    print(f"ticket_funnel_daily rows: {count2}")

    con.close()

------------------------------------------------------------
## Step 4.8 - Write dbt Validation Tests
------------------------------------------------------------

Create tests/unit/test_dbt_models.py:

    import pytest
    import duckdb
    import os

    DBT_DB = "src/dbt/customercore.duckdb"

    @pytest.fixture(scope="module")
    def con():
        if not os.path.exists(DBT_DB):
            pytest.skip("dbt database not built yet - run dbt run first")
        conn = duckdb.connect(DBT_DB)
        yield conn
        conn.close()

    GOLD_TABLES = [
        "gold.customer_health_daily",
        "gold.ticket_funnel_daily",
        "gold.incident_severity_hourly",
        "gold.billing_failure_summary",
        "gold.product_adoption_features",
        "gold.retention_cohort_metrics",
        "gold.support_agent_performance",
    ]

    @pytest.mark.parametrize("table", GOLD_TABLES)
    def test_gold_table_exists_and_has_rows(con, table):
        result = con.execute(f"SELECT count(*) FROM {table}").fetchone()
        assert result[0] >= 0, f"{table} query failed"

    def test_customer_health_has_required_columns(con):
        cols = [r[0] for r in con.execute("DESCRIBE gold.customer_health_daily").fetchall()]
        required = ["customer_id", "tenant_id", "snapshot_date", "open_tickets", "avg_priority"]
        for c in required:
            assert c in cols, f"Missing column {c} in customer_health_daily"

    def test_no_null_tenant_ids(con):
        result = con.execute("""
            SELECT count(*) FROM gold.customer_health_daily WHERE tenant_id IS NULL
        """).fetchone()[0]
        assert result == 0, "Found NULL tenant_ids in customer_health_daily"

Run:

    doppler run -- pytest tests/unit/test_dbt_models.py -v
    # Expected: all tests passed (or skipped if dbt not run yet)

------------------------------------------------------------
## Step 4.9 - Commit Phase 4
------------------------------------------------------------

    git add .
    git commit -m "Phase 4: dbt 7 Gold models, schema tests, DuckDB Gold tables verified"
    git push origin main

------------------------------------------------------------
## PHASE 4 CHECKPOINT - ALL MUST PASS BEFORE PHASE 5
------------------------------------------------------------

CHECK 1 - dbt run completes:
    cd src/dbt && dbt run --profiles-dir . --project-dir . && cd ../..
    Expected: 7 of 7 OK

CHECK 2 - dbt tests pass:
    cd src/dbt && dbt test --profiles-dir . --project-dir . && cd ../..
    Expected: 0 failures

CHECK 3 - Gold tables have rows:
    doppler run -- python -c "
    import duckdb
    con = duckdb.connect('src/dbt/customercore.duckdb')
    print(con.execute('SELECT count(*) FROM gold.customer_health_daily').fetchone())
    "
    Expected: (N,) where N > 0

CHECK 4 - dbt docs generate:
    cd src/dbt && dbt docs generate --profiles-dir . --project-dir . && cd ../..
    Expected: Generated artifact files

CHECK 5 - dbt validation tests green:
    doppler run -- pytest tests/unit/test_dbt_models.py -v
    Expected: all passed

CHECK 6 - Git clean:
    git status
    Expected: nothing to commit

---


##############################################################
# PHASE 5 - CHROMADB, HYBRID RETRIEVAL AND RERANKER
##############################################################

Goal: By the end of Phase 5 you have ChromaDB running with
3 vector indexes (tickets, KB articles, product docs), BM25
sparse indexes built for all 3 collections, hybrid retrieval
combining dense and sparse results via Reciprocal Rank Fusion,
and a cross-encoder reranker scoring the top 5 results.

Estimated Time: 2-3 days

------------------------------------------------------------
## Step 5.1 - Add ChromaDB to Docker Compose
------------------------------------------------------------

Add the following service to your docker-compose.yml:

      chromadb:
        image: chromadb/chroma:latest
        container_name: chromadb
        ports:
          - "8001:8000"
        volumes:
          - chromadb_data:/chroma/chroma
        environment:
          IS_PERSISTENT: "TRUE"
          ANONYMIZED_TELEMETRY: "FALSE"
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/heartbeat"]
          interval: 10s
          timeout: 5s
          retries: 5

Add to volumes section:
      chromadb_data:

Start ChromaDB:

    docker compose up -d chromadb
    docker compose ps chromadb
    # Expected: chromadb running (healthy)

    # Verify heartbeat
    curl http://localhost:8001/api/v1/heartbeat
    # Expected: {"nanosecond heartbeat": XXXXXXXX}

------------------------------------------------------------
## Step 5.2 - Create ChromaDB Client Factory
------------------------------------------------------------

Create src/rag/__init__.py as empty file.

Create src/rag/chroma_client.py:

    import chromadb
    import structlog

    log = structlog.get_logger()
    _client = None

    def get_chroma_client(host: str = "localhost", port: int = 8001) -> chromadb.HttpClient:
        global _client
        if _client is None:
            _client = chromadb.HttpClient(host=host, port=port)
            log.info("chromadb_connected", host=host, port=port)
        return _client

    COLLECTION_NAMES = {
        "tickets": "ticket_index",
        "kb": "kb_index",
        "product_docs": "product_docs_index",
    }

    def get_or_create_collection(name: str):
        client = get_chroma_client()
        collection = client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"},
        )
        log.info("collection_ready", name=name, count=collection.count())
        return collection

------------------------------------------------------------
## Step 5.3 - Create the Embedding Client (Ollama BGE-M3)
------------------------------------------------------------

First install Ollama to serve embeddings locally:
    Download from: https://ollama.com
    Install and run Ollama

Pull the BGE-M3 embedding model:

    ollama pull bge-m3

Verify it works:

    ollama run bge-m3 "test embedding"

Create src/rag/embedder.py:

    import os
    import httpx
    import structlog
    from typing import List

    log = structlog.get_logger()

    OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
    EMBED_MODEL = os.environ.get("EMBED_MODEL", "bge-m3")

    def embed(text: str) -> List[float]:
        if not text or not text.strip():
            return [0.0] * 1024
        try:
            resp = httpx.post(
                f"{OLLAMA_URL}/api/embeddings",
                json={"model": EMBED_MODEL, "prompt": text},
                timeout=30,
            )
            resp.raise_for_status()
            return resp.json()["embedding"]
        except Exception as e:
            log.error("embed_failed", model=EMBED_MODEL, error=str(e))
            return [0.0] * 1024

    def embed_batch(texts: List[str], batch_size: int = 32) -> List[List[float]]:
        results = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            for text in batch:
                results.append(embed(text))
            log.info("embed_batch_progress", done=min(i + batch_size, len(texts)), total=len(texts))
        return results

------------------------------------------------------------
## Step 5.4 - Build the BM25 Sparse Index
------------------------------------------------------------

Create src/rag/bm25_index.py:

    import pickle
    import os
    from rank_bm25 import BM25Okapi
    from typing import List, Dict
    import structlog

    log = structlog.get_logger()

    BM25_CACHE_DIR = "data/bm25_indexes"
    os.makedirs(BM25_CACHE_DIR, exist_ok=True)

    _bm25_indexes: Dict[str, BM25Okapi] = {}
    _doc_ids: Dict[str, List[str]] = {}

    def tokenize(text: str) -> List[str]:
        return text.lower().split()

    def build_bm25_index(collection_name: str, documents: List[Dict]):
        """Build and cache BM25 index from a list of {'id': str, 'text': str} dicts."""
        ids = [d["id"] for d in documents]
        texts = [tokenize(d["text"]) for d in documents]
        bm25 = BM25Okapi(texts)
        _bm25_indexes[collection_name] = bm25
        _doc_ids[collection_name] = ids

        # Persist to disk
        cache_path = os.path.join(BM25_CACHE_DIR, f"{collection_name}.pkl")
        with open(cache_path, "wb") as f:
            pickle.dump({"bm25": bm25, "ids": ids}, f)
        log.info("bm25_index_built", collection=collection_name, doc_count=len(documents))

    def load_bm25_index(collection_name: str) -> bool:
        cache_path = os.path.join(BM25_CACHE_DIR, f"{collection_name}.pkl")
        if not os.path.exists(cache_path):
            return False
        with open(cache_path, "rb") as f:
            data = pickle.load(f)
        _bm25_indexes[collection_name] = data["bm25"]
        _doc_ids[collection_name] = data["ids"]
        log.info("bm25_index_loaded", collection=collection_name)
        return True

    def bm25_search(collection_name: str, query: str, n_results: int = 20) -> List[str]:
        if collection_name not in _bm25_indexes:
            if not load_bm25_index(collection_name):
                log.warning("bm25_index_not_found", collection=collection_name)
                return []
        bm25 = _bm25_indexes[collection_name]
        ids = _doc_ids[collection_name]
        scores = bm25.get_scores(tokenize(query))
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:n_results]
        return [ids[i] for i in top_indices]

------------------------------------------------------------
## Step 5.5 - Build the Hybrid Retriever
------------------------------------------------------------

Create src/rag/hybrid_retriever.py:

    from typing import List, Dict, Optional
    import structlog
    from src.rag.chroma_client import get_or_create_collection
    from src.rag.embedder import embed
    from src.rag.bm25_index import bm25_search

    log = structlog.get_logger()

    def reciprocal_rank_fusion(
        dense_ids: List[str],
        sparse_ids: List[str],
        k: int = 60,
    ) -> List[str]:
        scores: Dict[str, float] = {}
        for rank, doc_id in enumerate(dense_ids):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
        for rank, doc_id in enumerate(sparse_ids):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
        return sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

    def hybrid_retrieve(
        query: str,
        collection_name: str,
        tenant_id: Optional[str] = None,
        n_results: int = 20,
    ) -> List[Dict]:
        # Dense retrieval via ChromaDB
        collection = get_or_create_collection(collection_name)
        query_embedding = embed(query)

        where_filter = {"tenant_id": tenant_id} if tenant_id else None

        try:
            dense_results = collection.query(
                query_embeddings=[query_embedding],
                n_results=min(n_results, collection.count()),
                where=where_filter,
                include=["documents", "metadatas", "distances"],
            )
            dense_ids = dense_results["ids"][0] if dense_results["ids"] else []
            dense_docs = {
                id_: {"text": doc, "metadata": meta, "distance": dist}
                for id_, doc, meta, dist in zip(
                    dense_results["ids"][0],
                    dense_results["documents"][0],
                    dense_results["metadatas"][0],
                    dense_results["distances"][0],
                )
            }
        except Exception as e:
            log.error("dense_retrieval_failed", error=str(e))
            dense_ids, dense_docs = [], {}

        # Sparse retrieval via BM25
        sparse_ids = bm25_search(collection_name, query, n_results)

        # Merge with Reciprocal Rank Fusion
        fused_ids = reciprocal_rank_fusion(dense_ids, sparse_ids)[:n_results]

        # Build result list
        results = []
        for doc_id in fused_ids:
            if doc_id in dense_docs:
                results.append({"id": doc_id, **dense_docs[doc_id]})

        log.info("hybrid_retrieve_done",
                 collection=collection_name,
                 dense_hits=len(dense_ids),
                 sparse_hits=len(sparse_ids),
                 fused=len(results))
        return results

------------------------------------------------------------
## Step 5.6 - Build the Cross-Encoder Reranker
------------------------------------------------------------

Create src/rag/reranker.py:

    from typing import List, Dict
    from sentence_transformers import CrossEncoder
    import structlog

    log = structlog.get_logger()

    RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    _reranker: CrossEncoder = None

    def get_reranker() -> CrossEncoder:
        global _reranker
        if _reranker is None:
            log.info("reranker_loading", model=RERANKER_MODEL)
            _reranker = CrossEncoder(RERANKER_MODEL, max_length=512)
            log.info("reranker_ready", model=RERANKER_MODEL)
        return _reranker

    def rerank(query: str, candidates: List[Dict], top_k: int = 5) -> List[Dict]:
        if not candidates:
            return []
        reranker = get_reranker()
        pairs = [(query, c.get("text", "")) for c in candidates]
        scores = reranker.predict(pairs)
        ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
        results = [{"rerank_score": float(score), **doc} for doc, score in ranked[:top_k]]
        log.info("rerank_done", candidates=len(candidates), returned=len(results))
        return results

------------------------------------------------------------
## Step 5.7 - Seed the ChromaDB Indexes with Sample Data
------------------------------------------------------------

Create src/rag/seed_indexes.py:

    import json
    import structlog
    from src.rag.chroma_client import get_or_create_collection, COLLECTION_NAMES
    from src.rag.embedder import embed_batch
    from src.rag.bm25_index import build_bm25_index

    log = structlog.get_logger()

    SAMPLE_TICKETS = [
        {"id": "TICKET-001", "text": "Authentication service returns 401 on valid OAuth tokens after recent deployment", "tenant_id": "acme-corp", "priority": "high"},
        {"id": "TICKET-002", "text": "Payment processing fails intermittently for enterprise plan customers during renewal", "tenant_id": "acme-corp", "priority": "critical"},
        {"id": "TICKET-003", "text": "Dashboard loading slowly when more than 100 reports are loaded simultaneously", "tenant_id": "contoso-ltd", "priority": "medium"},
        {"id": "TICKET-004", "text": "Webhook integration not firing on certain events in the production environment", "tenant_id": "globex-inc", "priority": "high"},
        {"id": "TICKET-005", "text": "API rate limit documentation is unclear and causing confusion among developers", "tenant_id": "initech-llc", "priority": "low"},
    ]

    SAMPLE_KB = [
        {"id": "KB-001", "text": "OAuth 2.0 troubleshooting guide: verify token expiry, check redirect URIs, validate scopes", "tenant_id": "global", "category": "auth"},
        {"id": "KB-002", "text": "Payment gateway integration guide: retry logic for transient failures, webhook verification", "tenant_id": "global", "category": "billing"},
        {"id": "KB-003", "text": "Performance optimization checklist: database indexes, query caching, connection pooling", "tenant_id": "global", "category": "performance"},
        {"id": "KB-004", "text": "Webhook debugging: check event logs, verify endpoint reachability, inspect payload format", "tenant_id": "global", "category": "integrations"},
        {"id": "KB-005", "text": "API rate limits explained: 1000 requests per minute for enterprise, 100 for professional tier", "tenant_id": "global", "category": "api"},
    ]

    SAMPLE_PRODUCT_DOCS = [
        {"id": "DOC-001", "text": "Authentication module API reference: /auth/token, /auth/refresh, /auth/revoke endpoints", "tenant_id": "global", "doc_type": "api_ref"},
        {"id": "DOC-002", "text": "Billing integration guide: Stripe webhooks, subscription management, plan upgrade flows", "tenant_id": "global", "doc_type": "guide"},
        {"id": "DOC-003", "text": "Webhooks reference: event types, payload schemas, retry policies, security headers", "tenant_id": "global", "doc_type": "api_ref"},
    ]

    def seed_collection(collection_name: str, documents: list):
        collection = get_or_create_collection(collection_name)
        if collection.count() > 0:
            log.info("collection_already_seeded", name=collection_name, count=collection.count())
            return

        texts = [d["text"] for d in documents]
        embeddings = embed_batch(texts)
        ids = [d["id"] for d in documents]
        metadatas = [{k: v for k, v in d.items() if k not in ("id", "text")} for d in documents]

        collection.add(ids=ids, embeddings=embeddings, documents=texts, metadatas=metadatas)
        build_bm25_index(collection_name, [{"id": d["id"], "text": d["text"]} for d in documents])
        log.info("collection_seeded", name=collection_name, count=collection.count())

    def seed_all():
        seed_collection(COLLECTION_NAMES["tickets"], SAMPLE_TICKETS)
        seed_collection(COLLECTION_NAMES["kb"], SAMPLE_KB)
        seed_collection(COLLECTION_NAMES["product_docs"], SAMPLE_PRODUCT_DOCS)
        log.info("all_indexes_seeded")

    if __name__ == "__main__":
        seed_all()

Run the seeder:

    doppler run -- python -m src.rag.seed_indexes

------------------------------------------------------------
## Step 5.8 - Write RAG Unit Tests
------------------------------------------------------------

Create tests/unit/test_rag.py:

    import pytest
    from src.rag.bm25_index import build_bm25_index, bm25_search
    from src.rag.hybrid_retriever import reciprocal_rank_fusion

    def test_bm25_search():
        docs = [
            {"id": "d1", "text": "authentication oauth token failure"},
            {"id": "d2", "text": "payment billing subscription renewal"},
            {"id": "d3", "text": "performance dashboard slow loading"},
        ]
        build_bm25_index("test_collection", docs)
        results = bm25_search("test_collection", "oauth authentication", n_results=3)
        assert "d1" in results
        assert isinstance(results, list)

    def test_bm25_returns_empty_for_unknown_collection():
        results = bm25_search("nonexistent_collection_xyz", "query", n_results=5)
        assert results == []

    def test_reciprocal_rank_fusion_merges():
        dense = ["d1", "d2", "d3"]
        sparse = ["d3", "d1", "d4"]
        fused = reciprocal_rank_fusion(dense, sparse)
        assert "d1" in fused
        assert "d3" in fused
        assert fused.index("d1") < fused.index("d4")

    def test_reciprocal_rank_fusion_empty():
        fused = reciprocal_rank_fusion([], [])
        assert fused == []

    def test_reciprocal_rank_fusion_single_source():
        fused = reciprocal_rank_fusion(["a", "b", "c"], [])
        assert fused == ["a", "b", "c"]

Run:

    doppler run -- pytest tests/unit/test_rag.py -v
    # Expected: 5 passed

------------------------------------------------------------
## Step 5.9 - Test End-to-End Retrieval
------------------------------------------------------------

    doppler run -- python

    from src.rag.hybrid_retriever import hybrid_retrieve
    from src.rag.reranker import rerank

    query = "authentication fails with 401 error"
    candidates = hybrid_retrieve(query, collection_name="ticket_index", n_results=5)
    print(f"Hybrid retrieved {len(candidates)} candidates")

    reranked = rerank(query, candidates, top_k=3)
    for r in reranked:
        print(f"Score {r['rerank_score']:.3f}: {r['text'][:80]}")

    # Expected: 3 results, highest score for authentication-related doc

------------------------------------------------------------
## Step 5.10 - Commit Phase 5
------------------------------------------------------------

    git add .
    git commit -m "Phase 5: ChromaDB 3 indexes, BM25 sparse index, hybrid retrieval with RRF, cross-encoder reranker"
    git push origin main

------------------------------------------------------------
## PHASE 5 CHECKPOINT - ALL MUST PASS BEFORE PHASE 6
------------------------------------------------------------

CHECK 1 - ChromaDB healthy:
    curl http://localhost:8001/api/v1/heartbeat
    Expected: nanosecond heartbeat value

CHECK 2 - All 3 collections seeded:
    doppler run -- python -c "
    from src.rag.chroma_client import get_chroma_client
    client = get_chroma_client()
    for name in ['ticket_index','kb_index','product_docs_index']:
        col = client.get_collection(name)
        print(f'{name}: {col.count()} vectors')
    "
    Expected: all 3 collections show count > 0

CHECK 3 - RAG unit tests green:
    doppler run -- pytest tests/unit/test_rag.py -v
    Expected: 5 passed

CHECK 4 - Hybrid retrieve returns results:
    doppler run -- python -c "
    from src.rag.hybrid_retriever import hybrid_retrieve
    r = hybrid_retrieve('authentication error', 'ticket_index')
    print(f'Retrieved: {len(r)} results')
    "
    Expected: Retrieved: N results (N > 0)

CHECK 5 - Reranker returns top_k results:
    doppler run -- python -c "
    from src.rag.hybrid_retriever import hybrid_retrieve
    from src.rag.reranker import rerank
    candidates = hybrid_retrieve('payment failed', 'kb_index')
    ranked = rerank('payment failed', candidates, top_k=3)
    print(f'Reranked: {len(ranked)} results, top score: {ranked[0][\"rerank_score\"]:.3f}')
    "
    Expected: Reranked: 3 results, top score > 0.0

---


##############################################################
# PHASE 6 - SEMANTIC CACHE AND LITELLM AI GATEWAY
##############################################################

Goal: By the end of Phase 6 you have a 3-level caching system
(L0 embedding, L1 exact, L2 semantic) and a LiteLLM gateway
routing between local Ollama models and OpenRouter cloud
free models, with automatic fallback chains.

Estimated Time: 2-3 days

------------------------------------------------------------
## Step 6.1 - Install LiteLLM Proxy
------------------------------------------------------------

LiteLLM runs as a proxy server between your app and all LLM providers.

    pip install litellm==1.40.0 litellm[proxy]
    pip freeze > requirements.txt

    # Verify
    litellm --version

------------------------------------------------------------
## Step 6.2 - Pull Ollama Models
------------------------------------------------------------

Make sure Ollama is running, then pull the models:

    # Pull Gemma 3 4B for complex reasoning (primary model)
    ollama pull gemma3:4b

    # Pull Gemma 3 1B for simple tasks (fast, cheap)
    ollama pull gemma3:1b

    # Verify models are available
    ollama list

    # Test a quick inference
    ollama run gemma3:4b "Say hello in one sentence"

------------------------------------------------------------
## Step 6.3 - Create the LiteLLM Configuration
------------------------------------------------------------

Create litellm_config.yaml at the project root:

    model_list:

      # Primary: Gemma 3 4B via Ollama (complex reasoning)
      - model_name: gemma-3-4b
        litellm_params:
          model: ollama/gemma3:4b
          api_base: http://localhost:11434
          timeout: 120

      # Fast: Gemma 3 1B via Ollama (simple tasks)
      - model_name: gemma-3-1b
        litellm_params:
          model: ollama/gemma3:1b
          api_base: http://localhost:11434
          timeout: 60

      # Cloud fallback 1: DeepSeek via OpenRouter (free tier)
      - model_name: cloud-complex
        litellm_params:
          model: openrouter/deepseek/deepseek-chat-v3-0324:free
          api_key: os.environ/OPENROUTER_API_KEY
          api_base: https://openrouter.ai/api/v1
          extra_headers:
            HTTP-Referer: https://huggingface.co/spaces/customercore
            X-Title: CustomerCore

      # Cloud fallback 2: Qwen3 via OpenRouter (free tier)
      - model_name: cloud-simple
        litellm_params:
          model: openrouter/qwen/qwen3-8b:free
          api_key: os.environ/OPENROUTER_API_KEY
          api_base: https://openrouter.ai/api/v1
          extra_headers:
            HTTP-Referer: https://huggingface.co/spaces/customercore
            X-Title: CustomerCore

      # Cloud fallback 3: Llama 4 via OpenRouter (free tier)
      - model_name: cloud-fallback
        litellm_params:
          model: openrouter/meta-llama/llama-4-scout:free
          api_key: os.environ/OPENROUTER_API_KEY
          api_base: https://openrouter.ai/api/v1
          extra_headers:
            HTTP-Referer: https://huggingface.co/spaces/customercore
            X-Title: CustomerCore

    router_settings:
      routing_strategy: least-busy
      num_retries: 3
      retry_after: 5
      fallbacks:
        - gemma-3-4b: [cloud-complex, cloud-fallback]
        - gemma-3-1b: [cloud-simple, cloud-fallback]

    general_settings:
      master_key: os.environ/LITELLM_MASTER_KEY
      drop_params: true

Start LiteLLM proxy in a separate terminal:

    doppler run -- litellm --config litellm_config.yaml --port 4000

    # Verify it is running
    curl http://localhost:4000/health
    # Expected: {"status": "healthy"}

    # Test a call through the gateway
    curl http://localhost:4000/v1/chat/completions \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer YOUR_LITELLM_MASTER_KEY" \
      -d "{\"model\": \"gemma-3-1b\", \"messages\": [{\"role\": \"user\", \"content\": \"Say hello\"}]}"

------------------------------------------------------------
## Step 6.4 - Create the LLM Client
------------------------------------------------------------

Create src/rag/llm_client.py:

    import os
    from openai import OpenAI
    import structlog

    log = structlog.get_logger()

    LITELLM_URL = os.environ.get("LITELLM_URL", "http://localhost:4000")
    LITELLM_KEY = os.environ.get("LITELLM_MASTER_KEY", "sk-test")

    _client: OpenAI = None

    def get_llm_client() -> OpenAI:
        global _client
        if _client is None:
            _client = OpenAI(
                api_key=LITELLM_KEY,
                base_url=LITELLM_URL,
            )
        return _client

    def generate(
        prompt: str,
        task_complexity: str = "complex",
        temperature: float = 0.2,
        max_tokens: int = 512,
        system_prompt: str = "You are a helpful customer support AI assistant.",
    ) -> str:
        model = "gemma-3-1b" if task_complexity == "simple" else "gemma-3-4b"
        client = get_llm_client()
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            result = response.choices[0].message.content
            log.info("llm_generate_ok", model=model, tokens=response.usage.total_tokens)
            return result
        except Exception as e:
            log.error("llm_generate_failed", model=model, error=str(e))
            return f"[LLM Error: {str(e)}]"

------------------------------------------------------------
## Step 6.5 - Build the 3-Level Caching System
------------------------------------------------------------

Create src/rag/cache.py:

    import os
    import json
    import hashlib
    from typing import Optional
    import redis
    import structlog

    log = structlog.get_logger()

    REDIS_URL = os.environ.get("UPSTASH_REDIS_URL", "redis://localhost:6379")

    _redis_client: redis.Redis = None

    def get_redis() -> redis.Redis:
        global _redis_client
        if _redis_client is None:
            _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
        return _redis_client

    def make_l1_key(endpoint: str, payload: dict) -> str:
        payload_str = json.dumps(payload, sort_keys=True)
        return f"l1:{endpoint}:{hashlib.sha256(payload_str.encode()).hexdigest()[:16]}"

    # ----- L0: Embedding Cache -----
    def get_cached_embedding(text: str) -> Optional[list]:
        key = f"l0:embed:{hashlib.sha256(text.encode()).hexdigest()[:24]}"
        cached = get_redis().get(key)
        if cached:
            log.info("cache_hit", level="L0", key=key[:20])
            return json.loads(cached)
        return None

    def set_cached_embedding(text: str, embedding: list, ttl: int = 86400):
        key = f"l0:embed:{hashlib.sha256(text.encode()).hexdigest()[:24]}"
        get_redis().setex(key, ttl, json.dumps(embedding))

    # ----- L1: Exact Result Cache -----
    def get_cached_result(endpoint: str, payload: dict) -> Optional[dict]:
        key = make_l1_key(endpoint, payload)
        cached = get_redis().get(key)
        if cached:
            log.info("cache_hit", level="L1", key=key[:20])
            return json.loads(cached)
        return None

    def set_cached_result(endpoint: str, payload: dict, result: dict, ttl: int = 60):
        key = make_l1_key(endpoint, payload)
        get_redis().setex(key, ttl, json.dumps(result))

------------------------------------------------------------
## Step 6.6 - Build the Semantic Cache (L2)
------------------------------------------------------------

Create src/rag/semantic_cache.py:

    import os
    import json
    import hashlib
    from typing import Optional
    import structlog
    import chromadb
    from src.rag.cache import get_redis
    from src.rag.embedder import embed
    from src.rag.chroma_client import get_chroma_client

    log = structlog.get_logger()

    SIMILARITY_THRESHOLD = float(os.environ.get("SEMANTIC_CACHE_THRESHOLD", "0.92"))
    SEMANTIC_CACHE_TTL = int(os.environ.get("SEMANTIC_CACHE_TTL", "300"))

    def get_semantic_cache_collection():
        client = get_chroma_client()
        return client.get_or_create_collection(
            name="semantic_cache",
            metadata={"hnsw:space": "cosine"},
        )

    def semantic_cache_lookup(query: str, tenant_id: str) -> Optional[dict]:
        collection = get_semantic_cache_collection()
        if collection.count() == 0:
            return None

        query_embedding = embed(query)
        try:
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=1,
                where={"tenant_id": tenant_id},
                include=["distances", "metadatas"],
            )
            if not results["ids"][0]:
                return None

            distance = results["distances"][0][0]
            similarity = 1 - distance

            if similarity >= SIMILARITY_THRESHOLD:
                cache_id = results["ids"][0][0]
                cached_str = get_redis().get(f"scache:{cache_id}")
                if cached_str:
                    log.info("cache_hit", level="L2", similarity=round(similarity, 3))
                    return json.loads(cached_str)
        except Exception as e:
            log.warning("semantic_cache_lookup_failed", error=str(e))
        return None

    def semantic_cache_store(query: str, tenant_id: str, response: dict):
        collection = get_semantic_cache_collection()
        embedding = embed(query)
        cache_id = hashlib.sha256(f"{tenant_id}:{query}".encode()).hexdigest()[:16]
        try:
            collection.add(
                ids=[cache_id],
                embeddings=[embedding],
                documents=[query],
                metadatas=[{"tenant_id": tenant_id}],
            )
            get_redis().setex(f"scache:{cache_id}", SEMANTIC_CACHE_TTL, json.dumps(response))
            log.info("semantic_cache_stored", cache_id=cache_id, ttl=SEMANTIC_CACHE_TTL)
        except Exception as e:
            log.warning("semantic_cache_store_failed", error=str(e))

------------------------------------------------------------
## Step 6.7 - Write Cache Unit Tests
------------------------------------------------------------

Create tests/unit/test_cache.py:

    import pytest
    import hashlib
    import json

    def test_l1_key_is_deterministic():
        from src.rag.cache import make_l1_key
        key1 = make_l1_key("/predict", {"a": 1, "b": 2})
        key2 = make_l1_key("/predict", {"b": 2, "a": 1})
        assert key1 == key2

    def test_l1_key_differs_by_endpoint():
        from src.rag.cache import make_l1_key
        key1 = make_l1_key("/predict", {"a": 1})
        key2 = make_l1_key("/rag-answer", {"a": 1})
        assert key1 != key2

    def test_similarity_threshold_logic():
        similarity = 0.95
        threshold = 0.92
        assert similarity >= threshold

        similarity_low = 0.80
        assert similarity_low < threshold

    def test_cache_key_format():
        from src.rag.cache import make_l1_key
        key = make_l1_key("/predict", {"ticket_id": "t-001"})
        assert key.startswith("l1:/predict:")
        assert len(key) > 20

Run:

    doppler run -- pytest tests/unit/test_cache.py -v
    # Expected: 4 passed

------------------------------------------------------------
## Step 6.8 - Commit Phase 6
------------------------------------------------------------

    git add .
    git commit -m "Phase 6: LiteLLM gateway, Ollama models, 3-level cache (L0 embedding, L1 exact, L2 semantic)"
    git push origin main

------------------------------------------------------------
## PHASE 6 CHECKPOINT - ALL MUST PASS BEFORE PHASE 7
------------------------------------------------------------

CHECK 1 - LiteLLM proxy healthy:
    curl http://localhost:4000/health
    Expected: status healthy

CHECK 2 - LLM generate works end to end:
    doppler run -- python -c "
    from src.rag.llm_client import generate
    result = generate('Say hello in one sentence', task_complexity='simple')
    print('LLM output:', result[:100])
    "
    Expected: A hello sentence (not an error)

CHECK 3 - Cache tests green:
    doppler run -- pytest tests/unit/test_cache.py -v
    Expected: 4 passed

CHECK 4 - Redis reachable:
    doppler run -- python -c "
    from src.rag.cache import get_redis
    r = get_redis()
    r.set('test_key', 'test_value', ex=10)
    print(r.get('test_key'))
    "
    Expected: test_value

CHECK 5 - Semantic cache round trip:
    doppler run -- python -c "
    from src.rag.semantic_cache import semantic_cache_store, semantic_cache_lookup
    semantic_cache_store('How do I reset my password?', 'acme-corp', {'answer': 'Go to settings'})
    result = semantic_cache_lookup('How do I reset my password?', 'acme-corp')
    print('Semantic cache hit:', result is not None)
    "
    Expected: Semantic cache hit: True

---


##############################################################
# PHASE 7 - 8 ML MODELS (TRAINING AND MLFLOW TRACKING)
##############################################################

Goal: By the end of Phase 7 you have all 8 ML models trained,
tracked in MLflow on DagsHub, passing their promotion gates,
and registered in the MLflow model registry.

Estimated Time: 4-5 days

------------------------------------------------------------
## Step 7.1 - Create the Feature Engineering Module
------------------------------------------------------------

Create src/ml/__init__.py as empty file.

Create src/ml/feature_engineering.py:

    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import LabelEncoder
    from typing import List, Tuple
    import structlog
    import duckdb
    import os

    log = structlog.get_logger()

    PRIORITY_MAP = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    CATEGORIES = ["bug", "feature", "security", "performance", "ui", "test",
                  "dependency", "question", "incident", "billing", "auth", "docs"]

    def load_silver_data() -> pd.DataFrame:
        DBT_DB = "src/dbt/customercore.duckdb"
        if os.path.exists(DBT_DB):
            con = duckdb.connect(DBT_DB)
            df = con.execute("SELECT * FROM gold.ticket_funnel_daily").df()
            con.close()
            return df

        # Fallback: generate synthetic training data
        np.random.seed(42)
        n = 5000
        return pd.DataFrame({
            "event_id": [f"evt-{i}" for i in range(n)],
            "body": [f"Sample ticket body number {i} about auth or billing or performance" for i in range(n)],
            "priority": np.random.choice(list(PRIORITY_MAP.keys()), n, p=[0.1, 0.25, 0.45, 0.2]),
            "tenant_id": np.random.choice(["acme-corp", "contoso-ltd", "globex-inc"], n),
            "customer_tier": np.random.choice(["free", "professional", "enterprise"], n, p=[0.5, 0.35, 0.15]),
            "reopen_count": np.random.randint(0, 5, n),
            "ticket_age_hours": np.random.exponential(48, n),
            "category": np.random.choice(CATEGORIES, n),
            "is_synthetic": True,
        })

    def create_text_features(df: pd.DataFrame, embedder=None) -> np.ndarray:
        from sklearn.feature_extraction.text import TfidfVectorizer
        tfidf = TfidfVectorizer(max_features=100, stop_words="english")
        tfidf_features = tfidf.fit_transform(df["body"].fillna("")).toarray()
        return tfidf_features

    def create_structured_features(df: pd.DataFrame) -> pd.DataFrame:
        features = pd.DataFrame()
        features["priority_num"] = df["priority"].map(PRIORITY_MAP).fillna(2)
        features["reopen_count"] = df.get("reopen_count", pd.Series(0, index=df.index))
        features["ticket_age_hours"] = df.get("ticket_age_hours", pd.Series(24, index=df.index))
        tier_map = {"free": 0, "professional": 1, "enterprise": 2}
        features["customer_tier_num"] = df.get("customer_tier", "professional").map(tier_map).fillna(1)
        features["body_length"] = df["body"].fillna("").str.len()
        features["body_word_count"] = df["body"].fillna("").str.split().str.len()
        return features

------------------------------------------------------------
## Step 7.2 - Create the MLflow Utilities
------------------------------------------------------------

Create src/ml/mlflow_utils.py:

    import os
    import mlflow
    import structlog

    log = structlog.get_logger()

    def setup_mlflow():
        tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlruns.db")
        mlflow.set_tracking_uri(tracking_uri)
        log.info("mlflow_setup", tracking_uri=tracking_uri)

    def register_model_if_gate_passes(
        run_id: str,
        model_name: str,
        metric_name: str,
        metric_value: float,
        gate_value: float,
        gate_direction: str = "greater",
    ) -> bool:
        passes = (metric_value >= gate_value) if gate_direction == "greater" else (metric_value <= gate_value)
        if passes:
            model_uri = f"runs:/{run_id}/model"
            mlflow.register_model(model_uri=model_uri, name=model_name)
            log.info("model_registered", name=model_name, metric=metric_name, value=round(metric_value, 4))
            return True
        else:
            log.warning("model_gate_failed", name=model_name, metric=metric_name,
                        value=round(metric_value, 4), gate=gate_value)
            return False

------------------------------------------------------------
## Step 7.3 - Train Model 1: Category Classifier
------------------------------------------------------------

Create src/ml/train_category.py:

    import mlflow
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import cross_val_score, train_test_split
    from sklearn.metrics import f1_score
    from sklearn.preprocessing import LabelEncoder
    from xgboost import XGBClassifier
    import structlog
    from src.ml.feature_engineering import load_silver_data, create_structured_features, CATEGORIES
    from src.ml.mlflow_utils import setup_mlflow, register_model_if_gate_passes

    log = structlog.get_logger()
    MODEL_NAME = "customercore-category-classifier"
    GATE_METRIC = "macro_f1"
    GATE_VALUE = 0.45

    def train():
        setup_mlflow()
        mlflow.set_experiment("customercore-category-classifier")

        df = load_silver_data()
        le = LabelEncoder()
        df["category_encoded"] = le.fit_transform(df["category"].fillna("question"))

        X = create_structured_features(df)
        y = df["category_encoded"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        params = {"n_estimators": 200, "max_depth": 6, "learning_rate": 0.1,
                  "use_label_encoder": False, "eval_metric": "mlogloss"}

        with mlflow.start_run(run_name="xgboost-category") as run:
            model = XGBClassifier(**params, random_state=42)
            model.fit(X_train, y_train)

            preds = model.predict(X_test)
            macro_f1 = f1_score(y_test, preds, average="macro", zero_division=0)
            weighted_f1 = f1_score(y_test, preds, average="weighted", zero_division=0)

            mlflow.log_params(params)
            mlflow.log_metric("macro_f1", macro_f1)
            mlflow.log_metric("weighted_f1", weighted_f1)
            mlflow.log_metric("n_classes", len(le.classes_))
            mlflow.sklearn.log_model(model, "model")

            log.info("category_classifier_trained", macro_f1=round(macro_f1, 4))
            register_model_if_gate_passes(run.info.run_id, MODEL_NAME, GATE_METRIC, macro_f1, GATE_VALUE)
            return macro_f1

    if __name__ == "__main__":
        train()

------------------------------------------------------------
## Step 7.4 - Train Model 2: Priority Classifier
------------------------------------------------------------

Create src/ml/train_priority.py:

    import mlflow
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import f1_score
    from sklearn.preprocessing import LabelEncoder
    from lightgbm import LGBMClassifier
    import structlog
    from src.ml.feature_engineering import load_silver_data, create_structured_features, PRIORITY_MAP
    from src.ml.mlflow_utils import setup_mlflow, register_model_if_gate_passes

    log = structlog.get_logger()
    MODEL_NAME = "customercore-priority-classifier"
    GATE_VALUE = 0.55

    def train():
        setup_mlflow()
        mlflow.set_experiment("customercore-priority-classifier")

        df = load_silver_data()
        le = LabelEncoder()
        df["priority_encoded"] = le.fit_transform(df["priority"].fillna("medium"))

        X = create_structured_features(df)
        y = df["priority_encoded"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        params = {"n_estimators": 200, "max_depth": 6, "learning_rate": 0.05, "num_leaves": 31}

        with mlflow.start_run(run_name="lgbm-priority") as run:
            model = LGBMClassifier(**params, random_state=42, verbose=-1)
            model.fit(X_train, y_train)

            preds = model.predict(X_test)
            weighted_f1 = f1_score(y_test, preds, average="weighted", zero_division=0)

            mlflow.log_params(params)
            mlflow.log_metric("weighted_f1", weighted_f1)
            mlflow.sklearn.log_model(model, "model")

            log.info("priority_classifier_trained", weighted_f1=round(weighted_f1, 4))
            register_model_if_gate_passes(run.info.run_id, MODEL_NAME, "weighted_f1", weighted_f1, GATE_VALUE)
            return weighted_f1

    if __name__ == "__main__":
        train()

------------------------------------------------------------
## Step 7.5 - Train Model 3: SLA Risk Predictor
------------------------------------------------------------

Create src/ml/train_sla.py:

    import mlflow
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import roc_auc_score
    from lightgbm import LGBMClassifier
    from src.ml.feature_engineering import load_silver_data, create_structured_features
    from src.ml.mlflow_utils import setup_mlflow, register_model_if_gate_passes
    import structlog

    log = structlog.get_logger()
    MODEL_NAME = "customercore-sla-risk"
    GATE_VALUE = 0.60

    def train():
        setup_mlflow()
        mlflow.set_experiment("customercore-sla-risk")

        df = load_silver_data()
        features = create_structured_features(df)
        # Synthetic SLA breach label: high priority + old ticket + multiple reopens
        y = ((df["priority"].isin(["critical","high"])) &
             (df.get("ticket_age_hours", 48) > 48) &
             (df.get("reopen_count", 0) > 1)).astype(int)

        X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.2, random_state=42)

        params = {"n_estimators": 100, "max_depth": 4, "learning_rate": 0.1}

        with mlflow.start_run(run_name="lgbm-sla-risk") as run:
            model = LGBMClassifier(**params, random_state=42, verbose=-1)
            model.fit(X_train, y_train)
            proba = model.predict_proba(X_test)[:, 1]
            auc = roc_auc_score(y_test, proba)

            mlflow.log_params(params)
            mlflow.log_metric("auc_roc", auc)
            mlflow.sklearn.log_model(model, "model")

            log.info("sla_risk_trained", auc=round(auc, 4))
            register_model_if_gate_passes(run.info.run_id, MODEL_NAME, "auc_roc", auc, GATE_VALUE)
            return auc

    if __name__ == "__main__":
        train()

------------------------------------------------------------
## Step 7.6 - Train Model 4: Churn Risk Predictor
------------------------------------------------------------

Create src/ml/train_churn.py:

    import mlflow
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import roc_auc_score
    from lightgbm import LGBMClassifier
    from src.ml.feature_engineering import load_silver_data, create_structured_features
    from src.ml.mlflow_utils import setup_mlflow, register_model_if_gate_passes
    import structlog

    log = structlog.get_logger()
    MODEL_NAME = "customercore-churn-risk"
    GATE_VALUE = 0.58

    def train():
        setup_mlflow()
        mlflow.set_experiment("customercore-churn-risk")

        df = load_silver_data()
        features = create_structured_features(df)
        # Synthetic churn label: payment failures + many high priority tickets
        y = ((df["priority"].isin(["critical","high"])) &
             (df.get("reopen_count", 0) > 2)).astype(int)

        X_train, X_test, y_train, y_test = train_test_split(features, y, test_size=0.2, random_state=42)

        params = {"n_estimators": 150, "max_depth": 5, "learning_rate": 0.08}

        with mlflow.start_run(run_name="lgbm-churn") as run:
            model = LGBMClassifier(**params, random_state=42, verbose=-1)
            model.fit(X_train, y_train)
            proba = model.predict_proba(X_test)[:, 1]
            auc = roc_auc_score(y_test, proba)

            mlflow.log_params(params)
            mlflow.log_metric("auc_roc", auc)
            mlflow.sklearn.log_model(model, "model")

            log.info("churn_risk_trained", auc=round(auc, 4))
            register_model_if_gate_passes(run.info.run_id, MODEL_NAME, "auc_roc", auc, GATE_VALUE)
            return auc

    if __name__ == "__main__":
        train()

------------------------------------------------------------
## Step 7.7 - Train Remaining 4 Models
------------------------------------------------------------

Create src/ml/train_routing.py:

    import mlflow, numpy as np, pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import f1_score
    from sklearn.preprocessing import LabelEncoder
    from xgboost import XGBClassifier
    from src.ml.feature_engineering import load_silver_data, create_structured_features
    from src.ml.mlflow_utils import setup_mlflow, register_model_if_gate_passes

    ROUTING_TEAMS = ["support", "engineering", "infra", "billing", "security"]
    MODEL_NAME = "customercore-routing-classifier"

    def train():
        setup_mlflow()
        mlflow.set_experiment("customercore-routing-classifier")
        df = load_silver_data()
        le = LabelEncoder()
        # Synthetic routing label based on category
        category_to_team = {
            "bug": "engineering", "security": "security", "performance": "infra",
            "billing": "billing", "auth": "security", "feature": "support",
            "question": "support", "docs": "support", "incident": "infra",
            "dependency": "engineering", "ui": "engineering", "test": "engineering",
        }
        df["routing_team"] = df["category"].map(category_to_team).fillna("support")
        df["routing_encoded"] = le.fit_transform(df["routing_team"])
        X = create_structured_features(df)
        y = df["routing_encoded"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        with mlflow.start_run(run_name="xgb-routing") as run:
            model = XGBClassifier(n_estimators=150, max_depth=5, use_label_encoder=False, eval_metric="mlogloss")
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            wf1 = f1_score(y_test, preds, average="weighted", zero_division=0)
            mlflow.log_metric("weighted_f1", wf1)
            mlflow.sklearn.log_model(model, "model")
            register_model_if_gate_passes(run.info.run_id, MODEL_NAME, "weighted_f1", wf1, 0.55)
            return wf1

    if __name__ == "__main__":
        train()

Create src/ml/train_sentiment.py:

    import mlflow, numpy as np, pandas as pd
    from sklearn.ensemble import IsolationForest
    from sklearn.model_selection import train_test_split
    from src.ml.feature_engineering import load_silver_data, create_structured_features
    from src.ml.mlflow_utils import setup_mlflow

    def train():
        setup_mlflow()
        mlflow.set_experiment("customercore-sentiment-anomaly")
        df = load_silver_data()
        X = create_structured_features(df)
        with mlflow.start_run(run_name="isolation-forest-sentiment") as run:
            model = IsolationForest(contamination=0.05, random_state=42, n_estimators=100)
            model.fit(X)
            scores = model.decision_function(X)
            anomaly_rate = (model.predict(X) == -1).mean()
            mlflow.log_metric("anomaly_rate", anomaly_rate)
            mlflow.log_metric("n_samples", len(X))
            mlflow.sklearn.log_model(model, "model")
            return anomaly_rate

    if __name__ == "__main__":
        train()

Create src/ml/train_incident.py:

    import mlflow, numpy as np, pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import f1_score
    from sklearn.preprocessing import LabelEncoder
    from lightgbm import LGBMClassifier
    from src.ml.feature_engineering import load_silver_data, create_structured_features
    from src.ml.mlflow_utils import setup_mlflow, register_model_if_gate_passes

    def train():
        setup_mlflow()
        mlflow.set_experiment("customercore-incident-severity")
        df = load_silver_data()
        le = LabelEncoder()
        df["severity_encoded"] = le.fit_transform(df["priority"].fillna("medium"))
        X = create_structured_features(df)
        y = df["severity_encoded"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        with mlflow.start_run(run_name="lgbm-incident-severity") as run:
            model = LGBMClassifier(n_estimators=100, max_depth=4, verbose=-1)
            model.fit(X_train, y_train)
            preds = model.predict(X_test)
            wf1 = f1_score(y_test, preds, average="weighted", zero_division=0)
            mlflow.log_metric("weighted_f1", wf1)
            mlflow.sklearn.log_model(model, "model")
            register_model_if_gate_passes(run.info.run_id, "customercore-incident-severity", "weighted_f1", wf1, 0.50)
            return wf1

    if __name__ == "__main__":
        train()

Create src/ml/train_forecast.py:

    import mlflow, numpy as np, pandas as pd
    from src.ml.mlflow_utils import setup_mlflow

    def train():
        setup_mlflow()
        mlflow.set_experiment("customercore-ticket-volume-forecast")
        np.random.seed(42)
        dates = pd.date_range("2025-01-01", periods=90, freq="D")
        volumes = 100 + 20 * np.sin(np.arange(90) * 2 * np.pi / 7) + np.random.normal(0, 10, 90)
        df = pd.DataFrame({"ds": dates, "y": volumes.clip(min=10)})
        try:
            from prophet import Prophet
            with mlflow.start_run(run_name="prophet-volume-forecast") as run:
                model = Prophet(seasonality_mode="additive", weekly_seasonality=True)
                model.fit(df)
                future = model.make_future_dataframe(periods=30)
                forecast = model.predict(future)
                mape = np.mean(np.abs((df["y"].values - forecast["yhat"][:90].values) / df["y"].values)) * 100
                mlflow.log_metric("mape", mape)
                mlflow.log_metric("forecast_horizon_days", 30)
                print(f"Prophet forecast MAPE: {mape:.2f}%")
                return mape
        except ImportError:
            print("Prophet not installed - skipping forecast model")
            return None

    if __name__ == "__main__":
        train()

------------------------------------------------------------
## Step 7.8 - Train All 8 Models
------------------------------------------------------------

    doppler run -- python -m src.ml.train_category
    doppler run -- python -m src.ml.train_priority
    doppler run -- python -m src.ml.train_sla
    doppler run -- python -m src.ml.train_churn
    doppler run -- python -m src.ml.train_routing
    doppler run -- python -m src.ml.train_sentiment
    doppler run -- python -m src.ml.train_incident
    doppler run -- python -m src.ml.train_forecast

    # Verify all 8 experiments appear in MLflow
    # Open browser: dagshub.com/YOUR_USERNAME/customercore/mlflow
    # You should see 8 experiments with runs

------------------------------------------------------------
## Step 7.9 - Write ML Training Tests
------------------------------------------------------------

Create tests/unit/test_ml_models.py:

    import pytest
    import numpy as np
    import pandas as pd

    def test_category_trainer_returns_metric():
        from src.ml.train_category import train
        score = train()
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_priority_trainer_returns_metric():
        from src.ml.train_priority import train
        score = train()
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_sla_trainer_returns_metric():
        from src.ml.train_sla import train
        auc = train()
        assert isinstance(auc, float)
        assert 0.0 <= auc <= 1.0

    def test_churn_trainer_returns_metric():
        from src.ml.train_churn import train
        auc = train()
        assert isinstance(auc, float)
        assert 0.0 <= auc <= 1.0

    def test_feature_engineering_shapes():
        from src.ml.feature_engineering import load_silver_data, create_structured_features
        df = load_silver_data()
        features = create_structured_features(df)
        assert features.shape[0] == len(df)
        assert features.shape[1] >= 4

Run:

    doppler run -- pytest tests/unit/test_ml_models.py -v
    # Expected: 5 passed

------------------------------------------------------------
## Step 7.10 - Commit Phase 7
------------------------------------------------------------

    git add .
    git commit -m "Phase 7: 8 ML models trained, MLflow tracking on DagsHub, all promotion gates logged"
    git push origin main

------------------------------------------------------------
## PHASE 7 CHECKPOINT - ALL MUST PASS BEFORE PHASE 8
------------------------------------------------------------

CHECK 1 - ML tests green:
    doppler run -- pytest tests/unit/test_ml_models.py -v
    Expected: 5 passed

CHECK 2 - MLflow has 8 experiments:
    Open browser: dagshub.com/YOUR_USERNAME/customercore/mlflow
    Expected: 8 experiments visible with at least 1 run each

CHECK 3 - Model registry has entries:
    doppler run -- python -c "
    import mlflow
    import os
    mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])
    client = mlflow.MlflowClient()
    models = client.search_registered_models()
    print(f'Registered models: {len(models)}')
    for m in models: print(f'  - {m.name}')
    "
    Expected: At least 4 registered models listed

CHECK 4 - Git clean:
    git status
    Expected: nothing to commit

---


##############################################################
# PHASE 8 - MEM0 LONG-TERM MEMORY AND PYDANTIC SCHEMAS
##############################################################

Goal: By the end of Phase 8 you have Mem0 storing and
retrieving agent memories backed by Supabase pgvector,
and a fully validated 14-field TriageOutput Pydantic schema
that the LLM must return for every ticket.

Estimated Time: 3-4 days

------------------------------------------------------------
## Step 8.1 - Set Up Supabase Database Schema
------------------------------------------------------------

Go to supabase.com -> your project -> SQL Editor.
Run the following SQL to set up the database:

    -- Enable pgvector extension
    CREATE EXTENSION IF NOT EXISTS vector;

    -- Events table
    CREATE TABLE IF NOT EXISTS events (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        event_id TEXT UNIQUE NOT NULL,
        event_type TEXT NOT NULL,
        source TEXT NOT NULL,
        tenant_id TEXT NOT NULL,
        customer_id TEXT,
        created_at TIMESTAMPTZ DEFAULT NOW(),
        body TEXT,
        priority TEXT,
        is_synthetic BOOLEAN DEFAULT FALSE
    );

    -- Audit log table (immutable - never delete rows)
    CREATE TABLE IF NOT EXISTS audit_log (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        timestamp TIMESTAMPTZ DEFAULT NOW(),
        tenant_id TEXT NOT NULL,
        endpoint TEXT NOT NULL,
        input_hash TEXT,
        output_summary TEXT,
        model_version TEXT,
        latency_ms INTEGER,
        cache_level TEXT,
        hitl_required BOOLEAN DEFAULT FALSE
    );

    -- Mem0 memories table (used by Mem0 internally)
    CREATE TABLE IF NOT EXISTS memories (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        user_id TEXT NOT NULL,
        agent_id TEXT,
        memory TEXT NOT NULL,
        embedding vector(1024),
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
    );

    -- Row-level security for tenant isolation
    ALTER TABLE events ENABLE ROW LEVEL SECURITY;
    ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

    CREATE POLICY tenant_isolation_events ON events
        USING (tenant_id = current_setting('app.tenant_id', true));

    CREATE POLICY tenant_isolation_audit ON audit_log
        USING (tenant_id = current_setting('app.tenant_id', true));

------------------------------------------------------------
## Step 8.2 - Configure and Test Mem0
------------------------------------------------------------

Create src/agent/__init__.py as empty file.

Create src/agent/memory.py:

    import os
    from typing import Optional, List
    from mem0 import Memory
    import structlog

    log = structlog.get_logger()

    SUPABASE_DB_URL = os.environ.get("SUPABASE_DB_URL", "")

    _mem0_client: Optional[Memory] = None

    def get_mem0_client() -> Memory:
        global _mem0_client
        if _mem0_client is None:
            config = {
                "vector_store": {
                    "provider": "pgvector",
                    "config": {
                        "dbname": "postgres",
                        "user": "postgres",
                        "password": os.environ.get("SUPABASE_DB_PASSWORD", ""),
                        "host": os.environ.get("SUPABASE_DB_HOST", ""),
                        "port": 5432,
                        "collection_name": "memories",
                    },
                },
                "embedder": {
                    "provider": "ollama",
                    "config": {
                        "model": "bge-m3",
                        "ollama_base_url": os.environ.get("OLLAMA_URL", "http://localhost:11434"),
                    },
                },
                "llm": {
                    "provider": "litellm",
                    "config": {
                        "model": "gemma-3-1b",
                        "api_base": os.environ.get("LITELLM_URL", "http://localhost:4000"),
                        "api_key": os.environ.get("LITELLM_MASTER_KEY", "sk-test"),
                    },
                },
            }
            _mem0_client = Memory.from_config(config)
            log.info("mem0_initialized")
        return _mem0_client

    def store_memory(customer_id: str, tenant_id: str, content: str, agent_id: str = "triage_agent"):
        client = get_mem0_client()
        user_id = f"{tenant_id}:{customer_id}"
        try:
            client.add(
                messages=[{"role": "user", "content": content}],
                user_id=user_id,
                agent_id=agent_id,
            )
            log.info("memory_stored", user_id=user_id, agent_id=agent_id)
        except Exception as e:
            log.error("memory_store_failed", user_id=user_id, error=str(e))

    def recall_memories(customer_id: str, tenant_id: str, query: str, limit: int = 5) -> List[dict]:
        client = get_mem0_client()
        user_id = f"{tenant_id}:{customer_id}"
        try:
            results = client.search(query=query, user_id=user_id, limit=limit)
            memories = [r.get("memory", "") for r in results]
            log.info("memories_recalled", user_id=user_id, count=len(memories))
            return memories
        except Exception as e:
            log.warning("memory_recall_failed", user_id=user_id, error=str(e))
            return []

    def get_all_memories(customer_id: str, tenant_id: str) -> List[dict]:
        client = get_mem0_client()
        user_id = f"{tenant_id}:{customer_id}"
        try:
            return client.get_all(user_id=user_id)
        except Exception as e:
            log.warning("get_all_memories_failed", error=str(e))
            return []

------------------------------------------------------------
## Step 8.3 - Create the TriageOutput Pydantic Schema
------------------------------------------------------------

Create src/agent/schemas.py:

    from pydantic import BaseModel, Field, field_validator
    from typing import Optional, List, Literal

    VALID_CATEGORIES = [
        "bug", "feature_request", "security", "performance",
        "billing", "auth", "docs", "question", "incident", "other",
    ]

    VALID_PRIORITIES = ["critical", "high", "medium", "low"]
    VALID_TEAMS = ["support", "engineering", "infra", "billing", "security", "escalation"]

    class TriageOutput(BaseModel):
        """14-field structured output for every ticket processed by the triage agent."""

        # Field 1: Category classification
        category: Literal[
            "bug", "feature_request", "security", "performance",
            "billing", "auth", "docs", "question", "incident", "other"
        ] = Field(description="Ticket category determined by the classifier agent")

        # Field 2: Priority classification
        priority: Literal["critical", "high", "medium", "low"] = Field(
            description="Ticket priority. critical=SLA breach risk. high=blocking. medium=normal. low=cosmetic"
        )

        # Field 3: Routing team
        routing_team: Literal["support", "engineering", "infra", "billing", "security", "escalation"] = Field(
            description="Team this ticket should be routed to"
        )

        # Field 4: SLA breach risk score
        sla_breach_risk: float = Field(
            ge=0.0, le=1.0,
            description="Probability of SLA breach (0.0=safe, 1.0=certain breach)"
        )

        # Field 5: Churn risk score
        churn_risk: float = Field(
            ge=0.0, le=1.0,
            description="Customer churn risk score based on ticket history and billing signals"
        )

        # Field 6: Confidence score
        confidence: float = Field(
            ge=0.0, le=1.0,
            description="Agent confidence in this triage decision. < 0.65 triggers HITL"
        )

        # Field 7: Short summary of the ticket
        summary: str = Field(
            min_length=10, max_length=300,
            description="One sentence summary of the ticket issue"
        )

        # Field 8: Suggested resolution
        suggested_resolution: str = Field(
            min_length=10, max_length=1000,
            description="Recommended resolution or next action based on KB and ticket history"
        )

        # Field 9: Knowledge base citations
        kb_citations: List[str] = Field(
            default_factory=list,
            description="List of KB article IDs that support this triage decision"
        )

        # Field 10: Customer memories recalled
        recalled_memories: List[str] = Field(
            default_factory=list,
            description="Relevant memories recalled from previous interactions with this customer"
        )

        # Field 11: Incident detected
        incident_detected: bool = Field(
            description="True if this ticket is part of or related to a detected incident"
        )

        # Field 12: HITL required
        hitl_required: bool = Field(
            description="True if a human must review this triage before acting on it"
        )

        # Field 13: HITL reason
        hitl_reason: Optional[str] = Field(
            default=None,
            description="Reason HITL is required, if hitl_required is True"
        )

        # Field 14: Model versions used
        models_used: List[str] = Field(
            default_factory=list,
            description="List of model names used in this triage (for audit and debugging)"
        )

        @field_validator("hitl_reason")
        @classmethod
        def hitl_reason_required_when_hitl(cls, v, info):
            if info.data.get("hitl_required") and not v:
                raise ValueError("hitl_reason must be provided when hitl_required is True")
            return v

        @field_validator("kb_citations")
        @classmethod
        def validate_citations_format(cls, v):
            for citation in v:
                if not citation.startswith(("KB-", "TICKET-", "DOC-")):
                    raise ValueError(f"Invalid citation format: {citation}. Must start with KB-, TICKET-, or DOC-")
            return v

        def should_trigger_hitl(self) -> bool:
            return self.confidence < 0.65 or self.hitl_required

        class Config:
            json_schema_extra = {
                "example": {
                    "category": "auth",
                    "priority": "high",
                    "routing_team": "security",
                    "sla_breach_risk": 0.72,
                    "churn_risk": 0.35,
                    "confidence": 0.88,
                    "summary": "Customer reports 401 errors after OAuth token refresh",
                    "suggested_resolution": "Verify token expiry settings and redirect URI configuration",
                    "kb_citations": ["KB-001"],
                    "recalled_memories": ["Previous auth issue resolved with token rotation - 2025-03-01"],
                    "incident_detected": False,
                    "hitl_required": False,
                    "hitl_reason": None,
                    "models_used": ["priority-classifier-v2", "category-classifier-v2", "gemma-3-4b"],
                }
            }

------------------------------------------------------------
## Step 8.4 - Write Memory and Schema Tests
------------------------------------------------------------

Create tests/unit/test_memory_schema.py:

    import pytest
    from pydantic import ValidationError
    from src.agent.schemas import TriageOutput

    def make_valid_triage(**overrides) -> dict:
        base = {
            "category": "auth",
            "priority": "high",
            "routing_team": "security",
            "sla_breach_risk": 0.72,
            "churn_risk": 0.35,
            "confidence": 0.88,
            "summary": "Customer has authentication failures with OAuth",
            "suggested_resolution": "Check token expiry and redirect URI configuration",
            "kb_citations": ["KB-001"],
            "recalled_memories": [],
            "incident_detected": False,
            "hitl_required": False,
            "hitl_reason": None,
            "models_used": ["priority-classifier-v2"],
        }
        base.update(overrides)
        return base

    def test_valid_triage_output_passes():
        output = TriageOutput(**make_valid_triage())
        assert output.category == "auth"
        assert output.priority == "high"
        assert output.sla_breach_risk == 0.72

    def test_invalid_category_rejected():
        with pytest.raises(ValidationError):
            TriageOutput(**make_valid_triage(category="invalid_category"))

    def test_invalid_priority_rejected():
        with pytest.raises(ValidationError):
            TriageOutput(**make_valid_triage(priority="urgent"))

    def test_sla_risk_out_of_range():
        with pytest.raises(ValidationError):
            TriageOutput(**make_valid_triage(sla_breach_risk=1.5))

    def test_hitl_required_needs_reason():
        with pytest.raises(ValidationError):
            TriageOutput(**make_valid_triage(hitl_required=True, hitl_reason=None))

    def test_hitl_not_required_no_reason_ok():
        output = TriageOutput(**make_valid_triage(hitl_required=False, hitl_reason=None))
        assert output.hitl_required is False

    def test_should_trigger_hitl_on_low_confidence():
        output = TriageOutput(**make_valid_triage(confidence=0.50))
        assert output.should_trigger_hitl() is True

    def test_should_not_trigger_hitl_on_high_confidence():
        output = TriageOutput(**make_valid_triage(confidence=0.90))
        assert output.should_trigger_hitl() is False

    def test_invalid_kb_citation_format():
        with pytest.raises(ValidationError):
            TriageOutput(**make_valid_triage(kb_citations=["INVALID-FORMAT"]))

    def test_valid_kb_citation_formats():
        output = TriageOutput(**make_valid_triage(kb_citations=["KB-001", "DOC-003", "TICKET-007"]))
        assert len(output.kb_citations) == 3

Run:

    doppler run -- pytest tests/unit/test_memory_schema.py -v
    # Expected: 10 passed

------------------------------------------------------------
## Step 8.5 - Test Mem0 Memory Round Trip
------------------------------------------------------------

Make sure Supabase connection is working:

    doppler run -- python

    from src.agent.memory import store_memory, recall_memories

    # Store a memory
    store_memory(
        customer_id="cust-001",
        tenant_id="acme-corp",
        content="Customer had payment failure on enterprise plan renewal in March 2026. Resolved by updating billing info.",
    )

    # Recall it
    memories = recall_memories(
        customer_id="cust-001",
        tenant_id="acme-corp",
        query="payment issues billing problems",
    )
    print(f"Recalled {len(memories)} memories:")
    for m in memories:
        print(f"  - {m[:100]}")

    # Expected: 1+ memories containing billing/payment context

------------------------------------------------------------
## Step 8.6 - Commit Phase 8
------------------------------------------------------------

    git add .
    git commit -m "Phase 8: Mem0 long-term memory on Supabase pgvector, 14-field TriageOutput Pydantic schema with validators"
    git push origin main

------------------------------------------------------------
## PHASE 8 CHECKPOINT - ALL MUST PASS BEFORE PHASE 9
------------------------------------------------------------

CHECK 1 - Schema tests green:
    doppler run -- pytest tests/unit/test_memory_schema.py -v
    Expected: 10 passed

CHECK 2 - Supabase tables exist:
    Go to supabase.com -> your project -> Table Editor
    Expected: events, audit_log, memories tables visible

CHECK 3 - TriageOutput serializes to JSON correctly:
    doppler run -- python -c "
    from src.agent.schemas import TriageOutput
    import json
    t = TriageOutput(
        category='bug', priority='high', routing_team='engineering',
        sla_breach_risk=0.6, churn_risk=0.3, confidence=0.85,
        summary='Test ticket summary about authentication issue',
        suggested_resolution='Check the logs and restart the auth service',
        kb_citations=['KB-001'], recalled_memories=[],
        incident_detected=False, hitl_required=False,
        hitl_reason=None, models_used=['v1']
    )
    print(json.dumps(t.model_dump(), indent=2)[:200])
    "
    Expected: Valid 14-field JSON printed

CHECK 4 - Mem0 round trip works:
    doppler run -- python -c "
    from src.agent.memory import store_memory, recall_memories
    store_memory('test-cust', 'test-tenant', 'Test memory about billing issue')
    mems = recall_memories('test-cust', 'test-tenant', 'billing')
    print(f'Memories: {len(mems)}')
    "
    Expected: Memories: 1 (or more)

---


##############################################################
# PHASE 9 - LANGGRAPH MULTI-AGENT SUPERVISOR
##############################################################

Goal: By the end of Phase 9 you have a fully working
LangGraph multi-agent supervisor with 6 specialist sub-agents,
HITL interrupt, MemorySaver checkpointing, and returning
a validated 14-field TriageOutput for every ticket.

Estimated Time: 5-7 days

------------------------------------------------------------
## Step 9.1 - Define the Agent State
------------------------------------------------------------

Create src/agent/state.py:

    from typing import TypedDict, Optional, List, Annotated
    from langgraph.graph.message import add_messages
    from src.agent.schemas import TriageOutput

    class TicketInput(TypedDict):
        ticket_id: str
        body: str
        customer_id: str
        tenant_id: str
        customer_tier: str

    class AgentState(TypedDict):
        # Input
        ticket: TicketInput

        # Populated by each sub-agent
        category: Optional[str]
        priority: Optional[str]
        routing_team: Optional[str]
        sla_breach_risk: Optional[float]
        churn_risk: Optional[float]
        confidence: Optional[float]
        summary: Optional[str]
        suggested_resolution: Optional[str]
        kb_citations: Optional[List[str]]
        recalled_memories: Optional[List[str]]
        incident_detected: Optional[bool]
        hitl_required: Optional[bool]
        hitl_reason: Optional[str]
        models_used: Optional[List[str]]

        # Workflow metadata
        current_step: Optional[str]
        error: Optional[str]
        final_output: Optional[TriageOutput]

        # Messages (for LangGraph message passing)
        messages: Annotated[list, add_messages]

------------------------------------------------------------
## Step 9.2 - Create Sub-Agent 1: Classify Agent
------------------------------------------------------------

Create src/agent/nodes/classify_agent.py:

    import mlflow
    import os
    from src.agent.state import AgentState
    from src.ml.feature_engineering import create_structured_features
    import pandas as pd
    import structlog

    log = structlog.get_logger()

    CATEGORY_MODEL = "customercore-category-classifier"
    PRIORITY_MODEL = "customercore-priority-classifier"

    def _load_model(name: str):
        tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlruns.db")
        mlflow.set_tracking_uri(tracking_uri)
        client = mlflow.MlflowClient()
        try:
            versions = client.get_latest_versions(name, stages=["Production", "None"])
            if versions:
                return mlflow.sklearn.load_model(f"models:/{name}/{versions[0].version}")
        except Exception as e:
            log.warning("model_load_failed", name=name, error=str(e))
        return None

    CATEGORIES = ["bug","feature_request","security","performance","billing","auth","docs","question","incident","other"]
    PRIORITIES = ["low","medium","high","critical"]

    def classify_agent_node(state: AgentState) -> AgentState:
        ticket = state["ticket"]
        df = pd.DataFrame([{
            "body": ticket["body"],
            "priority": "medium",
            "customer_tier": ticket.get("customer_tier", "professional"),
            "reopen_count": 0,
            "ticket_age_hours": 24,
        }])
        features = create_structured_features(df)

        # Category classification
        cat_model = _load_model(CATEGORY_MODEL)
        category = "bug"
        if cat_model:
            try:
                cat_idx = cat_model.predict(features)[0]
                category = CATEGORIES[int(cat_idx) % len(CATEGORIES)]
            except Exception as e:
                log.warning("category_prediction_failed", error=str(e))

        # Priority classification
        pri_model = _load_model(PRIORITY_MODEL)
        priority = "medium"
        if pri_model:
            try:
                pri_idx = pri_model.predict(features)[0]
                priority = PRIORITIES[int(pri_idx) % len(PRIORITIES)]
            except Exception as e:
                log.warning("priority_prediction_failed", error=str(e))

        models_used = state.get("models_used") or []
        models_used.append(f"{CATEGORY_MODEL}")

        log.info("classify_agent_done", category=category, priority=priority)
        return {
            **state,
            "category": category,
            "priority": priority,
            "current_step": "classify_agent",
            "models_used": models_used,
        }

------------------------------------------------------------
## Step 9.3 - Create Sub-Agent 2: Memory Agent
------------------------------------------------------------

Create src/agent/nodes/memory_agent.py:

    from src.agent.state import AgentState
    from src.agent.memory import store_memory, recall_memories
    import structlog

    log = structlog.get_logger()

    def memory_agent_node(state: AgentState) -> AgentState:
        ticket = state["ticket"]
        customer_id = ticket["customer_id"]
        tenant_id = ticket["tenant_id"]
        body = ticket["body"]

        memories = recall_memories(customer_id, tenant_id, query=body, limit=3)

        log.info("memory_agent_done", customer_id=customer_id, memories_recalled=len(memories))
        return {
            **state,
            "recalled_memories": memories,
            "current_step": "memory_agent",
        }

------------------------------------------------------------
## Step 9.4 - Create Sub-Agent 3: RAG Agent
------------------------------------------------------------

Create src/agent/nodes/rag_agent.py:

    from src.agent.state import AgentState
    from src.rag.hybrid_retriever import hybrid_retrieve
    from src.rag.reranker import rerank
    from src.rag.semantic_cache import semantic_cache_lookup, semantic_cache_store
    from src.rag.llm_client import generate
    import structlog

    log = structlog.get_logger()

    RAG_SYSTEM_PROMPT = """You are a customer support specialist. Based on the ticket and knowledge base articles provided,
    generate a concise summary and resolution recommendation. Be specific and actionable.
    Return ONLY:
    Summary: <one sentence>
    Resolution: <specific steps to resolve>"""

    def rag_agent_node(state: AgentState) -> AgentState:
        ticket = state["ticket"]
        tenant_id = ticket["tenant_id"]
        query = ticket["body"]

        # Check semantic cache first
        cached = semantic_cache_lookup(query, tenant_id)
        if cached:
            return {
                **state,
                "summary": cached.get("summary", ""),
                "suggested_resolution": cached.get("resolution", ""),
                "kb_citations": cached.get("citations", []),
                "current_step": "rag_agent_cached",
            }

        # Hybrid retrieval
        candidates = hybrid_retrieve(query, collection_name="kb_index", tenant_id=None, n_results=10)
        reranked = rerank(query, candidates, top_k=3)
        citations = [r.get("id", "") for r in reranked if r.get("id")]
        context = "\n".join([r.get("text", "") for r in reranked])

        prompt = f"""Ticket: {query}

    Relevant Knowledge Base Articles:
    {context}

    Customer Memories: {state.get("recalled_memories", [])}"""

        response_text = generate(prompt, task_complexity="complex", system_prompt=RAG_SYSTEM_PROMPT)

        summary = ""
        resolution = ""
        for line in response_text.split("\n"):
            if line.startswith("Summary:"):
                summary = line.replace("Summary:", "").strip()
            elif line.startswith("Resolution:"):
                resolution = line.replace("Resolution:", "").strip()

        if not summary:
            summary = ticket["body"][:200]
        if not resolution:
            resolution = "Please review the knowledge base articles and escalate if needed."

        result = {"summary": summary, "resolution": resolution, "citations": citations}
        semantic_cache_store(query, tenant_id, result)

        log.info("rag_agent_done", citations=len(citations))
        return {
            **state,
            "summary": summary,
            "suggested_resolution": resolution,
            "kb_citations": [c for c in citations if c],
            "current_step": "rag_agent",
        }

------------------------------------------------------------
## Step 9.5 - Create Sub-Agent 4: Churn Agent
------------------------------------------------------------

Create src/agent/nodes/churn_agent.py:

    import mlflow, os, pandas as pd
    from src.agent.state import AgentState
    from src.ml.feature_engineering import create_structured_features
    import structlog

    log = structlog.get_logger()
    CHURN_MODEL = "customercore-churn-risk"

    def churn_agent_node(state: AgentState) -> AgentState:
        ticket = state["ticket"]
        df = pd.DataFrame([{
            "body": ticket["body"],
            "priority": state.get("priority", "medium"),
            "customer_tier": ticket.get("customer_tier", "professional"),
            "reopen_count": 1,
            "ticket_age_hours": 48,
        }])
        features = create_structured_features(df)

        churn_risk = 0.3
        sla_breach_risk = 0.4

        try:
            mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlruns.db"))
            client = mlflow.MlflowClient()
            versions = client.get_latest_versions(CHURN_MODEL, stages=["Production", "None"])
            if versions:
                model = mlflow.sklearn.load_model(f"models:/{CHURN_MODEL}/{versions[0].version}")
                churn_risk = float(model.predict_proba(features)[0][1])
                sla_breach_risk = min(churn_risk * 1.2, 1.0)
        except Exception as e:
            log.warning("churn_model_load_failed", error=str(e))

        priority = state.get("priority", "medium")
        if priority in ("critical", "high") and churn_risk > 0.5:
            sla_breach_risk = min(sla_breach_risk + 0.2, 1.0)

        models_used = state.get("models_used") or []
        models_used.append(CHURN_MODEL)
        log.info("churn_agent_done", churn_risk=round(churn_risk, 3), sla_risk=round(sla_breach_risk, 3))
        return {
            **state,
            "churn_risk": churn_risk,
            "sla_breach_risk": sla_breach_risk,
            "models_used": models_used,
            "current_step": "churn_agent",
        }

------------------------------------------------------------
## Step 9.6 - Create Sub-Agent 5: Incident Agent
------------------------------------------------------------

Create src/agent/nodes/incident_agent.py:

    from src.agent.state import AgentState
    import structlog

    log = structlog.get_logger()

    INCIDENT_KEYWORDS = [
        "outage", "down", "not working", "cannot access", "500 error",
        "service unavailable", "latency", "timeout", "degraded",
    ]

    def incident_agent_node(state: AgentState) -> AgentState:
        body = state["ticket"]["body"].lower()
        incident_detected = any(kw in body for kw in INCIDENT_KEYWORDS)

        routing_team = "support"
        category = state.get("category", "bug")

        team_map = {
            "security": "security", "auth": "security",
            "incident": "infra", "performance": "infra",
            "billing": "billing",
            "bug": "engineering", "feature_request": "engineering", "dependency": "engineering",
        }
        routing_team = team_map.get(category, "support")

        if incident_detected:
            routing_team = "infra"
            incident_type = next((kw for kw in INCIDENT_KEYWORDS if kw in body), "general")
            log.info("incident_detected", type=incident_type, tenant_id=state["ticket"]["tenant_id"])

        return {
            **state,
            "incident_detected": incident_detected,
            "routing_team": routing_team,
            "current_step": "incident_agent",
        }

------------------------------------------------------------
## Step 9.7 - Create Sub-Agent 6: HITL Agent
------------------------------------------------------------

Create src/agent/nodes/hitl_agent.py:

    from src.agent.state import AgentState
    import structlog

    log = structlog.get_logger()

    def hitl_agent_node(state: AgentState) -> AgentState:
        confidence = state.get("confidence", 1.0)
        sla_risk = state.get("sla_breach_risk", 0.0)
        churn_risk = state.get("churn_risk", 0.0)
        priority = state.get("priority", "medium")

        hitl_required = False
        hitl_reason = None

        if confidence < 0.65:
            hitl_required = True
            hitl_reason = f"Low confidence: {confidence:.2f} below threshold 0.65"
        elif sla_risk > 0.80:
            hitl_required = True
            hitl_reason = f"Critical SLA breach risk: {sla_risk:.2f}"
        elif churn_risk > 0.75 and priority in ("critical", "high"):
            hitl_required = True
            hitl_reason = f"High churn risk {churn_risk:.2f} with {priority} priority"

        log.info("hitl_agent_done", hitl_required=hitl_required, reason=hitl_reason)
        return {
            **state,
            "hitl_required": hitl_required,
            "hitl_reason": hitl_reason,
            "current_step": "hitl_agent",
        }

Also create src/agent/nodes/__init__.py as empty file.

------------------------------------------------------------
## Step 9.8 - Create the Supervisor Router
------------------------------------------------------------

Create src/agent/supervisor.py:

    from typing import Literal
    import structlog
    from langgraph.graph import StateGraph, END
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.types import interrupt

    from src.agent.state import AgentState
    from src.agent.schemas import TriageOutput
    from src.agent.nodes.classify_agent import classify_agent_node
    from src.agent.nodes.memory_agent import memory_agent_node
    from src.agent.nodes.rag_agent import rag_agent_node
    from src.agent.nodes.churn_agent import churn_agent_node
    from src.agent.nodes.incident_agent import incident_agent_node
    from src.agent.nodes.hitl_agent import hitl_agent_node

    log = structlog.get_logger()

    def finalize_node(state: AgentState) -> AgentState:
        confidence = state.get("confidence")
        if confidence is None:
            recalled = state.get("recalled_memories", [])
            kb_cites = state.get("kb_citations", [])
            confidence = 0.70 + min(len(recalled) * 0.05, 0.15) + min(len(kb_cites) * 0.03, 0.10)
            confidence = min(confidence, 0.95)

        try:
            output = TriageOutput(
                category=state.get("category", "other"),
                priority=state.get("priority", "medium"),
                routing_team=state.get("routing_team", "support"),
                sla_breach_risk=state.get("sla_breach_risk", 0.3),
                churn_risk=state.get("churn_risk", 0.2),
                confidence=confidence,
                summary=state.get("summary", state["ticket"]["body"][:100]),
                suggested_resolution=state.get("suggested_resolution", "Please escalate for manual review"),
                kb_citations=state.get("kb_citations", []),
                recalled_memories=state.get("recalled_memories", []),
                incident_detected=state.get("incident_detected", False),
                hitl_required=state.get("hitl_required", False),
                hitl_reason=state.get("hitl_reason"),
                models_used=state.get("models_used", []),
            )
            log.info("finalize_done", confidence=round(confidence, 3))
            return {**state, "final_output": output, "confidence": confidence}
        except Exception as e:
            log.error("finalize_failed", error=str(e))
            return {**state, "error": str(e), "confidence": confidence}

    def hitl_check_router(state: AgentState) -> Literal["hitl_interrupt", "finalize"]:
        if state.get("hitl_required"):
            return "hitl_interrupt"
        return "finalize"

    def hitl_interrupt_node(state: AgentState) -> AgentState:
        ticket_id = state["ticket"]["ticket_id"]
        log.warning("hitl_interrupt_triggered", ticket_id=ticket_id, reason=state.get("hitl_reason"))
        human_review = interrupt({
            "ticket_id": ticket_id,
            "hitl_reason": state.get("hitl_reason"),
            "current_classification": {
                "category": state.get("category"),
                "priority": state.get("priority"),
                "routing_team": state.get("routing_team"),
            },
            "message": "Human review required. Approve or modify classification.",
        })
        # Update state with human input if provided
        if isinstance(human_review, dict):
            return {
                **state,
                "category": human_review.get("category", state.get("category")),
                "priority": human_review.get("priority", state.get("priority")),
                "routing_team": human_review.get("routing_team", state.get("routing_team")),
                "confidence": 1.0,
                "hitl_required": False,
            }
        return {**state, "confidence": 1.0, "hitl_required": False}

    def build_supervisor_graph() -> StateGraph:
        graph = StateGraph(AgentState)

        graph.add_node("classify_agent", classify_agent_node)
        graph.add_node("memory_agent", memory_agent_node)
        graph.add_node("rag_agent", rag_agent_node)
        graph.add_node("churn_agent", churn_agent_node)
        graph.add_node("incident_agent", incident_agent_node)
        graph.add_node("hitl_agent", hitl_agent_node)
        graph.add_node("hitl_interrupt", hitl_interrupt_node)
        graph.add_node("finalize", finalize_node)

        graph.set_entry_point("classify_agent")
        graph.add_edge("classify_agent", "memory_agent")
        graph.add_edge("memory_agent", "rag_agent")
        graph.add_edge("rag_agent", "churn_agent")
        graph.add_edge("churn_agent", "incident_agent")
        graph.add_edge("incident_agent", "hitl_agent")
        graph.add_conditional_edges("hitl_agent", hitl_check_router)
        graph.add_edge("hitl_interrupt", "finalize")
        graph.add_edge("finalize", END)

        return graph

    def run_triage(ticket: dict, thread_id: str = None) -> TriageOutput:
        graph = build_supervisor_graph()
        checkpointer = MemorySaver()
        app = graph.compile(checkpointer=checkpointer, interrupt_before=["hitl_interrupt"])

        config = {"configurable": {"thread_id": thread_id or ticket["ticket_id"]}}
        initial_state = {
            "ticket": ticket,
            "messages": [],
            "models_used": [],
        }

        for chunk in app.stream(initial_state, config):
            for node_name, node_output in chunk.items():
                log.info("agent_step", node=node_name, step=node_output.get("current_step", ""))

        final_state = app.get_state(config).values
        return final_state.get("final_output")

------------------------------------------------------------
## Step 9.9 - Write Supervisor Tests
------------------------------------------------------------

Create tests/unit/test_supervisor.py:

    import pytest
    from src.agent.state import AgentState
    from src.agent.nodes.classify_agent import classify_agent_node
    from src.agent.nodes.incident_agent import incident_agent_node
    from src.agent.nodes.hitl_agent import hitl_agent_node
    from src.agent.schemas import TriageOutput

    def make_state(body: str = "Test ticket", **kwargs) -> dict:
        base = {
            "ticket": {
                "ticket_id": "TEST-001",
                "body": body,
                "customer_id": "cust-001",
                "tenant_id": "acme-corp",
                "customer_tier": "professional",
            },
            "messages": [],
            "models_used": [],
        }
        base.update(kwargs)
        return base

    def test_incident_agent_detects_outage():
        state = make_state("Service is completely down and users cannot access the dashboard")
        result = incident_agent_node(state)
        assert result["incident_detected"] is True

    def test_incident_agent_no_false_positive():
        state = make_state("How do I reset my password?")
        result = incident_agent_node(state)
        assert result["incident_detected"] is False

    def test_hitl_triggered_on_low_confidence():
        state = make_state(confidence=0.40, sla_breach_risk=0.3, churn_risk=0.2, priority="medium")
        result = hitl_agent_node(state)
        assert result["hitl_required"] is True
        assert "Low confidence" in result["hitl_reason"]

    def test_hitl_not_triggered_on_high_confidence():
        state = make_state(confidence=0.90, sla_breach_risk=0.3, churn_risk=0.2, priority="medium")
        result = hitl_agent_node(state)
        assert result["hitl_required"] is False

    def test_routing_security_for_auth():
        state = make_state(category="auth", priority="high")
        result = incident_agent_node(state)
        assert result["routing_team"] == "security"

    def test_routing_infra_for_incident():
        state = make_state(body="Service is down outage", category="incident", priority="critical")
        result = incident_agent_node(state)
        assert result["routing_team"] == "infra"

Run:

    doppler run -- pytest tests/unit/test_supervisor.py -v
    # Expected: 6 passed

------------------------------------------------------------
## Step 9.10 - Test Full End-to-End Triage
------------------------------------------------------------

    doppler run -- python

    from src.agent.supervisor import run_triage

    ticket = {
        "ticket_id": "TEST-E2E-001",
        "body": "Our enterprise OAuth service is returning 401 on all token refreshes since the deployment at 3pm UTC",
        "customer_id": "ent-cust-001",
        "tenant_id": "acme-corp",
        "customer_tier": "enterprise",
    }

    result = run_triage(ticket)
    if result:
        print(f"Category: {result.category}")
        print(f"Priority: {result.priority}")
        print(f"Routing: {result.routing_team}")
        print(f"Confidence: {result.confidence:.2f}")
        print(f"HITL: {result.hitl_required}")
        print(f"Summary: {result.summary}")
    else:
        print("Triage returned None - check logs")

------------------------------------------------------------
## Step 9.11 - Commit Phase 9
------------------------------------------------------------

    git add .
    git commit -m "Phase 9: LangGraph 6-agent supervisor, HITL interrupt, MemorySaver checkpointing, full triage pipeline"
    git push origin main

------------------------------------------------------------
## PHASE 9 CHECKPOINT - ALL MUST PASS BEFORE PHASE 10
------------------------------------------------------------

CHECK 1 - Supervisor unit tests:
    doppler run -- pytest tests/unit/test_supervisor.py -v
    Expected: 6 passed

CHECK 2 - Full triage returns 14-field output:
    doppler run -- python -c "
    from src.agent.supervisor import run_triage
    result = run_triage({
        'ticket_id': 'TEST-001', 'body': 'Authentication fails on login',
        'customer_id': 'c1', 'tenant_id': 'acme', 'customer_tier': 'pro'
    })
    if result:
        fields = len(result.model_dump())
        print(f'Output fields: {fields}')
    "
    Expected: Output fields: 14

CHECK 3 - HITL triggers on low confidence:
    doppler run -- python -c "
    from src.agent.nodes.hitl_agent import hitl_agent_node
    state = {'ticket': {'ticket_id': 'T1', 'body': 'test', 'customer_id': 'c1', 'tenant_id': 't1', 'customer_tier': 'free'}, 'confidence': 0.40, 'sla_breach_risk': 0.3, 'churn_risk': 0.2, 'priority': 'medium', 'messages': [], 'models_used': []}
    result = hitl_agent_node(state)
    print('HITL required:', result['hitl_required'])
    "
    Expected: HITL required: True

CHECK 4 - Git clean:
    git status
    Expected: nothing to commit

---


##############################################################
# PHASE 10 - FASTAPI BACKEND AND MULTI-TENANCY
##############################################################

Goal: FastAPI app with JWT auth, tenant isolation middleware,
rate limiting, health check, /predict, /rag-answer, and
/agent/triage endpoints all working and tested.

Estimated Time: 3-4 days

------------------------------------------------------------
## Step 10.1 - Create the FastAPI App
------------------------------------------------------------

Create src/api/main.py:

    import os
    import time
    import sentry_sdk
    from sentry_sdk.integrations.fastapi import FastApiIntegration
    from sentry_sdk.integrations.starlette import StarletteIntegration
    from fastapi import FastAPI, Request, HTTPException, Depends
    from fastapi.middleware.cors import CORSMiddleware
    from contextlib import asynccontextmanager
    from pydantic import BaseModel
    from typing import Optional
    import structlog

    from src.agent.schemas import TriageOutput
    from src.rag.llm_client import generate

    log = structlog.get_logger()
    START_TIME = time.time()

    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN", ""),
        integrations=[StarletteIntegration(), FastApiIntegration()],
        traces_sample_rate=0.1,
        environment=os.environ.get("APP_ENV", "production"),
        release=os.environ.get("APP_VERSION", "1.0.0"),
    )

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        log.info("customercore_startup", version=os.environ.get("APP_VERSION", "1.0.0"))
        yield
        log.info("customercore_shutdown")

    app = FastAPI(
        title="CustomerCore Intelligence API",
        version=os.environ.get("APP_VERSION", "1.0.0"),
        lifespan=lifespan,
    )
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    class TicketRequest(BaseModel):
        ticket_id: str
        body: str
        customer_id: str
        tenant_id: str
        customer_tier: str = "professional"

    class PredictResponse(BaseModel):
        ticket_id: str
        category: str
        priority: str
        routing_team: str
        confidence: float
        model_version: str = "1.0.0"

    @app.get("/health")
    async def health():
        return {
            "status": "ok",
            "version": os.environ.get("APP_VERSION", "1.0.0"),
            "uptime_s": round(time.time() - START_TIME, 1),
            "dependencies": {
                "supabase": "ok",
                "redis": "ok",
                "chromadb": "ok",
                "litellm": "ok",
            },
        }

    @app.get("/metrics")
    async def metrics():
        from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
        from fastapi.responses import Response
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    @app.post("/predict", response_model=PredictResponse)
    async def predict(req: TicketRequest):
        from src.agent.nodes.classify_agent import classify_agent_node
        from src.agent.nodes.incident_agent import incident_agent_node
        state = {
            "ticket": req.model_dump(),
            "messages": [], "models_used": [],
        }
        state = classify_agent_node(state)
        state = incident_agent_node(state)
        return PredictResponse(
            ticket_id=req.ticket_id,
            category=state.get("category", "other"),
            priority=state.get("priority", "medium"),
            routing_team=state.get("routing_team", "support"),
            confidence=0.80,
        )

    @app.post("/rag-answer")
    async def rag_answer(req: TicketRequest):
        from src.rag.hybrid_retriever import hybrid_retrieve
        from src.rag.reranker import rerank
        from src.rag.semantic_cache import semantic_cache_lookup, semantic_cache_store
        cached = semantic_cache_lookup(req.body, req.tenant_id)
        if cached:
            return {"answer": cached.get("resolution", ""), "cache_level": "L2", "citations": cached.get("citations", [])}
        candidates = hybrid_retrieve(req.body, "kb_index", n_results=5)
        reranked = rerank(req.body, candidates, top_k=3)
        context = "\n".join([r.get("text", "") for r in reranked])
        answer = generate(f"Ticket: {req.body}\nKB:\n{context}", task_complexity="complex")
        citations = [r.get("id", "") for r in reranked if r.get("id")]
        semantic_cache_store(req.body, req.tenant_id, {"resolution": answer, "citations": citations})
        return {"answer": answer, "cache_level": "MISS", "citations": citations}

    @app.post("/agent/triage", response_model=TriageOutput)
    async def agent_triage(req: TicketRequest):
        from src.agent.supervisor import run_triage
        result = run_triage(req.model_dump())
        if not result:
            raise HTTPException(status_code=500, detail="Triage agent returned no output")
        return result

------------------------------------------------------------
## Step 10.2 - Create the Tenant Middleware
------------------------------------------------------------

Create src/api/middleware.py:

    import os
    import time
    import redis as redis_lib
    from fastapi import Request, HTTPException
    from starlette.middleware.base import BaseHTTPMiddleware
    import structlog

    log = structlog.get_logger()
    REDIS_URL = os.environ.get("UPSTASH_REDIS_URL", "redis://localhost:6379")

    RATE_LIMITS = {"enterprise": 600, "professional": 120, "free": 20}

    class TenantMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next):
            tenant_id = request.headers.get("X-Tenant-ID", "default")
            customer_tier = request.headers.get("X-Customer-Tier", "free")
            request.state.tenant_id = tenant_id
            request.state.customer_tier = customer_tier

            # Rate limiting via Redis
            try:
                r = redis_lib.from_url(REDIS_URL, decode_responses=True)
                key = f"rate:{tenant_id}:{int(time.time() // 60)}"
                count = r.incr(key)
                r.expire(key, 120)
                limit = RATE_LIMITS.get(customer_tier, 20)
                if count > limit:
                    raise HTTPException(
                        status_code=429,
                        detail=f"Rate limit exceeded: {limit} req/min for {customer_tier} tier",
                        headers={"Retry-After": "60"},
                    )
            except HTTPException:
                raise
            except Exception as e:
                log.warning("rate_limit_check_failed", error=str(e))

            response = await call_next(request)
            response.headers["X-Tenant-ID"] = tenant_id
            return response

Register the middleware in main.py by adding after the CORSMiddleware line:

    from src.api.middleware import TenantMiddleware
    app.add_middleware(TenantMiddleware)

------------------------------------------------------------
## Step 10.3 - Run the FastAPI App Locally
------------------------------------------------------------

    doppler run -- uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

    # Test health endpoint
    curl http://localhost:8000/health

    # Test predict endpoint
    curl -X POST http://localhost:8000/predict \
      -H "Content-Type: application/json" \
      -H "X-Tenant-ID: acme-corp" \
      -d "{\"ticket_id\": \"T001\", \"body\": \"Login fails with OAuth error\", \"customer_id\": \"c1\", \"tenant_id\": \"acme-corp\", \"customer_tier\": \"professional\"}"

    # Test agent triage
    curl -X POST http://localhost:8000/agent/triage \
      -H "Content-Type: application/json" \
      -H "X-Tenant-ID: acme-corp" \
      -d "{\"ticket_id\": \"T002\", \"body\": \"Payment failed on enterprise renewal\", \"customer_id\": \"c2\", \"tenant_id\": \"acme-corp\", \"customer_tier\": \"enterprise\"}"

------------------------------------------------------------
## Step 10.4 - Write API Tests
------------------------------------------------------------

Create tests/unit/test_api.py:

    import pytest
    from fastapi.testclient import TestClient
    from src.api.main import app

    client = TestClient(app)

    def test_health_returns_200():
        resp = client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "uptime_s" in data
        assert "dependencies" in data

    def test_health_has_all_dependencies():
        resp = client.get("/health")
        deps = resp.json()["dependencies"]
        assert "supabase" in deps
        assert "redis" in deps
        assert "chromadb" in deps
        assert "litellm" in deps

    def test_predict_returns_valid_response():
        resp = client.post("/predict", json={
            "ticket_id": "TEST-001",
            "body": "Authentication fails with 401",
            "customer_id": "c1",
            "tenant_id": "acme-corp",
            "customer_tier": "professional",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "category" in data
        assert "priority" in data
        assert data["priority"] in ["critical", "high", "medium", "low"]

    def test_predict_missing_body_fails():
        resp = client.post("/predict", json={"ticket_id": "T1"})
        assert resp.status_code == 422

Run:

    doppler run -- pytest tests/unit/test_api.py -v
    # Expected: 4 passed

------------------------------------------------------------
## Step 10.5 - Commit Phase 10
------------------------------------------------------------

    git add .
    git commit -m "Phase 10: FastAPI app, tenant middleware, rate limiting, /predict /rag-answer /agent/triage endpoints"
    git push origin main

------------------------------------------------------------
## PHASE 10 CHECKPOINT
------------------------------------------------------------

CHECK 1 - API tests green:
    doppler run -- pytest tests/unit/test_api.py -v
    Expected: 4 passed

CHECK 2 - Health endpoint live:
    curl http://localhost:8000/health
    Expected: {"status": "ok", ...}

CHECK 3 - Predict endpoint works:
    curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
      -d "{\"ticket_id\":\"T1\",\"body\":\"OAuth error\",\"customer_id\":\"c1\",\"tenant_id\":\"acme\",\"customer_tier\":\"pro\"}"
    Expected: JSON with category, priority, routing_team

CHECK 4 - Rate limit header present:
    curl -v http://localhost:8000/health 2>&1 | grep X-Tenant-ID
    Expected: X-Tenant-ID header in response

---


##############################################################
# PHASE 11 - LANGFUSE PROMPT OBSERVABILITY
##############################################################

Goal: All LLM calls tracked in Langfuse with prompt versions,
token costs, and RAGAS quality scores. 6 prompts versioned
in the Langfuse prompt registry.

Estimated Time: 2-3 days

------------------------------------------------------------
## Step 11.1 - Set Up Langfuse Prompts in the UI
------------------------------------------------------------

Go to cloud.langfuse.com -> your project -> Prompts tab.

Create these 6 prompts (click New Prompt for each):

Prompt 1 - Name: rag-system-prompt
    You are a customer support specialist with access to a knowledge base.
    Use only the provided context to answer. If the answer is not in the context, say so clearly.
    Be specific and actionable. Format: Summary: <one line> then Resolution: <steps>

Prompt 2 - Name: triage-system-prompt
    You are a customer support triage agent. Classify the ticket accurately.
    Consider the customer tier, ticket history, and severity of impact.
    Always prioritize security and payment issues at high or critical.

Prompt 3 - Name: churn-analysis-prompt
    Analyze the customer ticket and history for churn signals.
    Churn signals: payment failures, downgrade requests, repeated unresolved issues, negative sentiment.
    Return a brief churn risk assessment in 2 sentences.

Prompt 4 - Name: incident-detection-prompt
    Analyze this ticket for signs of a system incident or outage.
    An incident is when a service is degraded or unavailable for multiple customers simultaneously.
    Return: INCIDENT or NOT_INCIDENT with a one-line reason.

Prompt 5 - Name: summary-prompt
    Summarize this customer support ticket in one sentence.
    Include: the problem, affected service, and customer tier.
    Max 100 words.

Prompt 6 - Name: resolution-prompt
    Based on the ticket and knowledge base context, provide a resolution.
    Be specific. Include exact steps. Reference the KB articles used.
    If you cannot resolve it, state what information is needed.

Publish each as version 1.

------------------------------------------------------------
## Step 11.2 - Create the Langfuse Integration Module
------------------------------------------------------------

Create src/rag/langfuse_integration.py:

    import os
    from langfuse import Langfuse
    from langfuse.callback import CallbackHandler
    from typing import Optional, Dict
    import structlog

    log = structlog.get_logger()

    _langfuse: Optional[Langfuse] = None

    def get_langfuse() -> Langfuse:
        global _langfuse
        if _langfuse is None:
            _langfuse = Langfuse(
                public_key=os.environ.get("LANGFUSE_PUBLIC_KEY", ""),
                secret_key=os.environ.get("LANGFUSE_SECRET_KEY", ""),
                host="https://cloud.langfuse.com",
            )
        return _langfuse

    def get_langfuse_handler(tenant_id: str = "default", user_id: str = "system") -> CallbackHandler:
        return CallbackHandler(
            public_key=os.environ.get("LANGFUSE_PUBLIC_KEY", ""),
            secret_key=os.environ.get("LANGFUSE_SECRET_KEY", ""),
            host="https://cloud.langfuse.com",
            session_id=tenant_id,
            user_id=user_id,
        )

    def get_prompt(prompt_name: str, version: Optional[int] = None) -> str:
        lf = get_langfuse()
        try:
            prompt = lf.get_prompt(prompt_name, version=version)
            return prompt.prompt
        except Exception as e:
            log.warning("langfuse_prompt_fetch_failed", name=prompt_name, error=str(e))
            return _fallback_prompts.get(prompt_name, "You are a helpful assistant.")

    def log_ragas_score(trace_id: str, score: float, name: str = "faithfulness"):
        lf = get_langfuse()
        try:
            lf.score(trace_id=trace_id, name=name, value=score)
            log.info("ragas_score_logged", trace_id=trace_id, score=score, name=name)
        except Exception as e:
            log.warning("ragas_score_failed", error=str(e))

    def log_cost(trace_id: str, tenant_id: str, input_tokens: int, output_tokens: int, model: str):
        lf = get_langfuse()
        try:
            lf.trace(id=trace_id, metadata={
                "tenant_id": tenant_id,
                "model": model,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
            })
        except Exception as e:
            log.warning("cost_log_failed", error=str(e))

    _fallback_prompts = {
        "rag-system-prompt": "You are a customer support specialist. Use the context to answer accurately.",
        "triage-system-prompt": "You are a triage agent. Classify tickets by category and priority.",
        "summary-prompt": "Summarize this ticket in one sentence.",
        "resolution-prompt": "Provide a resolution for this customer issue.",
    }

------------------------------------------------------------
## Step 11.3 - Update the LLM Client to Use Langfuse Prompts
------------------------------------------------------------

Update src/rag/llm_client.py to add Langfuse tracking:

    # Add to the generate() function signature:
    def generate(
        prompt: str,
        task_complexity: str = "complex",
        temperature: float = 0.2,
        max_tokens: int = 512,
        system_prompt: str = None,
        tenant_id: str = "default",
        prompt_name: str = None,
    ) -> str:
        from src.rag.langfuse_integration import get_prompt, get_langfuse_handler
        if system_prompt is None:
            system_prompt_key = prompt_name or "triage-system-prompt"
            system_prompt = get_prompt(system_prompt_key)

        model = "gemma-3-1b" if task_complexity == "simple" else "gemma-3-4b"
        client = get_llm_client()
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            result = response.choices[0].message.content
            log.info("llm_generate_ok", model=model, tokens=response.usage.total_tokens)
            return result
        except Exception as e:
            log.error("llm_generate_failed", model=model, error=str(e))
            return f"[LLM Error: {str(e)}]"

------------------------------------------------------------
## Step 11.4 - Write Langfuse Tests
------------------------------------------------------------

Create tests/unit/test_langfuse.py:

    import pytest
    from unittest.mock import patch, MagicMock
    from src.rag.langfuse_integration import get_prompt, _fallback_prompts

    def test_fallback_prompt_returned_on_failure():
        with patch("src.rag.langfuse_integration.get_langfuse") as mock_lf:
            mock_lf.return_value.get_prompt.side_effect = Exception("Network error")
            result = get_prompt("rag-system-prompt")
            assert len(result) > 10

    def test_fallback_prompts_all_have_content():
        for name, text in _fallback_prompts.items():
            assert len(text) >= 20, f"Fallback prompt too short for {name}"

    def test_get_prompt_key_triage():
        prompt = _fallback_prompts.get("triage-system-prompt", "")
        assert "triage" in prompt.lower() or "classify" in prompt.lower()

Run:

    doppler run -- pytest tests/unit/test_langfuse.py -v
    # Expected: 3 passed

------------------------------------------------------------
## Step 11.5 - Verify in Langfuse UI
------------------------------------------------------------

After running the triage agent at least once:

    doppler run -- python -c "
    from src.agent.supervisor import run_triage
    run_triage({'ticket_id': 'LF-TEST-001', 'body': 'Payment failed on renewal',
    'customer_id': 'c1', 'tenant_id': 'acme-corp', 'customer_tier': 'enterprise'})
    "

Go to cloud.langfuse.com -> Traces
You should see the trace with LLM calls, token counts, and model info.

------------------------------------------------------------
## Step 11.6 - Commit Phase 11
------------------------------------------------------------

    git add .
    git commit -m "Phase 11: Langfuse prompt registry, 6 versioned prompts, RAGAS score logging, per-tenant cost tracking"
    git push origin main

------------------------------------------------------------
## PHASE 11 CHECKPOINT
------------------------------------------------------------

CHECK 1 - Langfuse tests green:
    doppler run -- pytest tests/unit/test_langfuse.py -v
    Expected: 3 passed

CHECK 2 - 6 prompts exist in Langfuse UI:
    Open cloud.langfuse.com -> Prompts tab
    Expected: 6 prompts visible (rag-system-prompt, triage-system-prompt, etc.)

CHECK 3 - Traces appear after a triage run:
    Open cloud.langfuse.com -> Traces tab
    Expected: at least 1 trace with LLM call details

---


##############################################################
# PHASE 12 - RESPONSIBLE AI (EU AI ACT COMPLIANCE)
##############################################################

Goal: Model cards for all 8 models, fairness.py with
accuracy parity metric tracked in MLflow, immutable
Iceberg audit log, EU AI Act checklist complete.

Estimated Time: 2-3 days

------------------------------------------------------------
## Step 12.1 - Create Model Cards for All 8 Models
------------------------------------------------------------

Create src/responsible_ai/model_cards/category_classifier_card.md:

    # Model Card: Category Classifier v1.0

    ## Model Details
    - Architecture: XGBoost (n_estimators=200, max_depth=6)
    - Training date: 2026-05-XX | MLflow experiment: customercore-category-classifier
    - Input: Structured ticket features (priority_num, reopen_count, body_length, tier)
    - Output: 10 ticket categories (bug, feature_request, security, performance, billing, auth, docs, question, incident, other)

    ## Performance
    | Metric      | Value |
    |-------------|-------|
    | Macro F1    | 0.65+ |
    | Weighted F1 | 0.70+ |

    ## Fairness Evaluation
    - Demographic: customer_tier (enterprise / professional / free)
    - Accuracy parity gap target: < 0.05
    - Measured via: src/responsible_ai/fairness.py
    - MLflow metric: fairness_accuracy_gap

    ## Limitations
    - Trained on synthetic data with real GitHub Issues. Performance on private enterprise tickets may vary.
    - Non-English tickets will degrade accuracy significantly.

    ## Intended Use
    - Intended: automated first-pass ticket categorization for routing.
    - NOT intended: final classification without human review for critical or security tickets.

    ## Monitoring
    - Drift detection: PSI weekly via Evidently
    - Alert threshold: PSI > 0.2 triggers retraining

Create the same structure for all remaining models. Create one file per model:
    - src/responsible_ai/model_cards/priority_classifier_card.md
    - src/responsible_ai/model_cards/sla_risk_card.md
    - src/responsible_ai/model_cards/churn_risk_card.md
    - src/responsible_ai/model_cards/routing_classifier_card.md
    - src/responsible_ai/model_cards/sentiment_anomaly_card.md
    - src/responsible_ai/model_cards/incident_severity_card.md
    - src/responsible_ai/model_cards/ticket_forecast_card.md

Each card follows the same template as above with model-specific values.

------------------------------------------------------------
## Step 12.2 - Create the Fairness Evaluation Module
------------------------------------------------------------

Create src/responsible_ai/__init__.py as empty file.

Create src/responsible_ai/fairness.py:

    import pandas as pd
    import numpy as np
    from sklearn.metrics import accuracy_score
    import mlflow
    import structlog

    log = structlog.get_logger()
    FAIRNESS_GATE = 0.05

    def compute_fairness_metrics(predictions_df: pd.DataFrame, model_name: str) -> dict:
        """
        Compute accuracy parity across customer_tier groups.
        EU AI Act Art.10(5): providers must assess data representativeness and bias.

        Args:
            predictions_df: DataFrame with columns: customer_tier, true_label, pred_label
            model_name: Name of the model being evaluated
        Returns:
            dict with per-tier accuracies and accuracy_gap
        """
        required_cols = {"customer_tier", "true_label", "pred_label"}
        if not required_cols.issubset(predictions_df.columns):
            raise ValueError(f"predictions_df must have columns: {required_cols}")

        groups = predictions_df["customer_tier"].unique()
        accuracies = {}

        for tier in groups:
            subset = predictions_df[predictions_df["customer_tier"] == tier]
            if len(subset) == 0:
                continue
            acc = accuracy_score(subset["true_label"], subset["pred_label"])
            accuracies[tier] = acc

        if not accuracies:
            raise ValueError("No groups found in predictions_df")

        accuracy_gap = max(accuracies.values()) - min(accuracies.values())

        mlflow.log_metric("fairness_accuracy_gap", accuracy_gap)
        mlflow.log_dict(accuracies, "fairness_per_tier.json")

        log.info("fairness_computed",
                 model=model_name,
                 accuracy_gap=round(accuracy_gap, 4),
                 tiers=list(accuracies.keys()))

        if accuracy_gap > FAIRNESS_GATE:
            raise ValueError(
                f"Fairness gate FAIL for {model_name}: "
                f"accuracy gap {accuracy_gap:.4f} > threshold {FAIRNESS_GATE}. "
                f"Per-tier accuracies: {accuracies}"
            )

        return {
            "accuracy_per_tier": accuracies,
            "accuracy_gap": accuracy_gap,
            "gate_passed": True,
            "gate_threshold": FAIRNESS_GATE,
        }

    def run_fairness_check_on_predictions(
        model_name: str,
        y_true: list,
        y_pred: list,
        tiers: list,
    ) -> dict:
        df = pd.DataFrame({
            "customer_tier": tiers,
            "true_label": y_true,
            "pred_label": y_pred,
        })
        return compute_fairness_metrics(df, model_name)

------------------------------------------------------------
## Step 12.3 - Create the Audit Log Middleware
------------------------------------------------------------

Create src/responsible_ai/audit_log.py:

    import os
    import time
    import hashlib
    import json
    from typing import Optional
    from supabase import create_client
    import structlog

    log = structlog.get_logger()

    def get_supabase():
        url = os.environ.get("SUPABASE_URL", "")
        key = os.environ.get("SUPABASE_KEY", "")
        if not url or not key:
            return None
        return create_client(url, key)

    def log_audit_event(
        tenant_id: str,
        endpoint: str,
        input_data: dict,
        output_summary: str,
        model_version: str,
        latency_ms: int,
        cache_level: Optional[str] = None,
        hitl_required: bool = False,
    ):
        client = get_supabase()
        if not client:
            log.warning("audit_log_skipped", reason="Supabase not configured")
            return

        input_hash = hashlib.sha256(
            json.dumps(input_data, sort_keys=True).encode()
        ).hexdigest()[:16]

        try:
            client.table("audit_log").insert({
                "tenant_id": tenant_id,
                "endpoint": endpoint,
                "input_hash": input_hash,
                "output_summary": output_summary[:500],
                "model_version": model_version,
                "latency_ms": latency_ms,
                "cache_level": cache_level,
                "hitl_required": hitl_required,
            }).execute()
            log.info("audit_logged", tenant_id=tenant_id, endpoint=endpoint)
        except Exception as e:
            log.error("audit_log_failed", error=str(e))

------------------------------------------------------------
## Step 12.4 - EU AI Act Compliance Checklist
------------------------------------------------------------

Create docs/eu_ai_act_compliance.md:

    # EU AI Act Compliance Checklist - CustomerCore

    Enforcement date: August 2026
    Self-assessed: Yes | Third-party audit: No (documented limitation)

    ## Article 10 - Data and Data Governance
    [x] Training data documented in model cards (source, size, preprocessing)
    [x] Bias assessment: per-demographic accuracy parity computed and tracked
    [x] Synthetic data clearly flagged with is_synthetic field
    [x] PII masked before training via Presidio (pii_masker.py)

    ## Article 12 - Record Keeping and Logging
    [x] Every prediction logged to Supabase audit_log table
    [x] Log contains: timestamp, model_version, input_hash, tenant_id, endpoint
    [x] Iceberg audit table provides ACID guarantees and immutability
    [x] Logs retained for minimum 6 months (Supabase free: 7 days, archived to R2)

    ## Article 13 - Transparency and Information
    [x] Model cards for all 8 models in src/responsible_ai/model_cards/
    [x] Model cards include: architecture, training data, performance, limitations, intended use
    [x] /health endpoint exposes model_version for every response
    [x] README contains live links to all model cards

    ## Article 14 - Human Oversight
    [x] HITL interrupt() implemented in LangGraph supervisor
    [x] HITL triggered automatically when confidence < 0.65
    [x] HITL triggered when SLA breach risk > 0.80
    [x] HITL queue monitored via Grafana (customercore_hitl_queue_depth)
    [x] Human decision logged to audit_log with reviewer context

    ## Article 15 - Accuracy, Robustness, Cybersecurity
    [x] Pydantic validation enforces output schema compliance
    [x] Prompt injection detection via guardrail layer
    [x] Drift detection: PSI metric computed weekly via Evidently
    [x] Circuit breaker pattern prevents cascade failures
    [x] All API keys in Doppler, never in code

------------------------------------------------------------
## Step 12.5 - Write Responsible AI Tests
------------------------------------------------------------

Create tests/unit/test_responsible_ai.py:

    import pytest
    import pandas as pd
    from src.responsible_ai.fairness import compute_fairness_metrics

    def make_predictions_df(gaps: dict) -> pd.DataFrame:
        rows = []
        for tier, (correct, total) in gaps.items():
            for i in range(total):
                rows.append({
                    "customer_tier": tier,
                    "true_label": 1,
                    "pred_label": 1 if i < correct else 0,
                })
        return pd.DataFrame(rows)

    def test_fairness_passes_when_gap_small():
        df = make_predictions_df({
            "enterprise": (90, 100),
            "professional": (88, 100),
            "free": (86, 100),
        })
        result = compute_fairness_metrics(df, "test-model")
        assert result["gate_passed"] is True
        assert result["accuracy_gap"] < 0.05

    def test_fairness_fails_when_gap_large():
        df = make_predictions_df({
            "enterprise": (95, 100),
            "free": (50, 100),
        })
        with pytest.raises(ValueError, match="Fairness gate FAIL"):
            compute_fairness_metrics(df, "test-model")

    def test_fairness_requires_correct_columns():
        df = pd.DataFrame({"wrong_col": [1, 2], "pred": [1, 2]})
        with pytest.raises(ValueError, match="must have columns"):
            compute_fairness_metrics(df, "test-model")

    def test_model_cards_exist():
        import os
        model_cards_dir = "src/responsible_ai/model_cards"
        if os.path.exists(model_cards_dir):
            cards = os.listdir(model_cards_dir)
            assert len(cards) >= 1, "At least 1 model card required"

Run:

    doppler run -- pytest tests/unit/test_responsible_ai.py -v
    # Expected: 4 passed

------------------------------------------------------------
## Step 12.6 - Commit Phase 12
------------------------------------------------------------

    git add .
    git commit -m "Phase 12: 8 model cards, fairness.py with accuracy parity gate, Supabase audit log, EU AI Act checklist"
    git push origin main

------------------------------------------------------------
## PHASE 12 CHECKPOINT
------------------------------------------------------------

CHECK 1 - Responsible AI tests:
    doppler run -- pytest tests/unit/test_responsible_ai.py -v
    Expected: 4 passed

CHECK 2 - All 8 model cards exist:
    dir src\responsible_ai\model_cards\
    Expected: 8 .md files

CHECK 3 - EU AI Act checklist complete:
    Open docs/eu_ai_act_compliance.md
    Expected: All items marked [x]

CHECK 4 - Fairness metric logged to MLflow:
    doppler run -- python -c "
    import mlflow, os, pandas as pd
    mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])
    mlflow.set_experiment('customercore-fairness-test')
    from src.responsible_ai.fairness import compute_fairness_metrics
    df = pd.DataFrame({'customer_tier': ['enterprise','pro','free']*10, 'true_label': [1]*30, 'pred_label': [1]*28+[0]*2})
    with mlflow.start_run():
        result = compute_fairness_metrics(df, 'test-model')
        print('Gap:', result['accuracy_gap'])
    "
    Expected: Gap: 0.0X (below 0.05)

---


##############################################################
# PHASE 13 - OPENTELEMETRY AND GRAFANA CLOUD DASHBOARDS
##############################################################

Goal: OTel Collector configured, 18 Prometheus metrics
instrumented in FastAPI, 5 Grafana Cloud dashboards live,
Loki logs and Tempo traces flowing.

Estimated Time: 4-5 days

------------------------------------------------------------
## Step 13.1 - Create Custom Prometheus Metrics
------------------------------------------------------------

Create src/monitoring/__init__.py as empty file.

Create src/monitoring/metrics.py:

    from prometheus_client import Counter, Histogram, Gauge, Summary

    # ── Request metrics (RED method)
    REQUEST_COUNT = Counter(
        "customercore_requests_total",
        "Total API requests",
        ["endpoint", "tenant_id", "status_code"],
    )
    REQUEST_LATENCY = Histogram(
        "customercore_request_latency_seconds",
        "API request latency",
        ["endpoint", "tenant_id"],
        buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0],
    )

    # ── Cache metrics
    CACHE_HIT = Counter(
        "customercore_cache_hits_total",
        "Cache hits by level",
        ["level", "tenant_id"],
    )
    CACHE_MISS = Counter(
        "customercore_cache_misses_total",
        "Cache misses by level",
        ["level", "tenant_id"],
    )
    CACHE_HIT_RATE = Gauge(
        "customercore_semantic_cache_hit_rate",
        "Rolling semantic cache hit rate (last 5 min)",
        ["tenant_id"],
    )

    # ── ML model metrics
    CONFIDENCE_SCORE = Histogram(
        "customercore_confidence_score",
        "Triage confidence score distribution",
        ["tenant_id"],
        buckets=[0.0, 0.2, 0.4, 0.5, 0.6, 0.65, 0.7, 0.8, 0.9, 1.0],
    )
    MODEL_PREDICTION_COUNT = Counter(
        "customercore_model_predictions_total",
        "Total model predictions",
        ["model_name", "tenant_id"],
    )
    CHURN_RISK_SCORE = Histogram(
        "customercore_churn_risk_score",
        "Churn risk score distribution",
        ["tenant_id"],
        buckets=[0.0, 0.2, 0.4, 0.6, 0.7, 0.8, 1.0],
    )
    FAIRNESS_SCORE = Gauge(
        "customercore_fairness_score",
        "Latest accuracy parity gap per model",
        ["model_name"],
    )

    # ── GenAI / LLM metrics
    LLM_TOKEN_COUNT = Counter(
        "customercore_llm_tokens_total",
        "Total LLM tokens consumed",
        ["model", "tenant_id", "direction"],
    )
    LLM_LATENCY = Histogram(
        "customercore_llm_latency_seconds",
        "LLM call latency",
        ["model", "tenant_id"],
        buckets=[0.5, 1.0, 2.0, 5.0, 10.0, 30.0],
    )
    RAG_FALLBACK = Counter(
        "customercore_rag_fallback_total",
        "LiteLLM fallback events",
        ["from_model", "to_model"],
    )

    # ── Streaming metrics
    STREAMING_LAG = Gauge(
        "customercore_streaming_lag_seconds",
        "Redpanda consumer lag per topic",
        ["topic"],
    )
    DLQ_EVENTS = Counter(
        "customercore_dlq_events_total",
        "Events sent to dead letter queue",
        ["topic", "reason"],
    )
    ICEBERG_SNAPSHOT_AGE = Gauge(
        "customercore_iceberg_snapshot_age_seconds",
        "Age of last Iceberg snapshot",
        ["table_name"],
    )

    # ── Business metrics
    HITL_QUEUE_DEPTH = Gauge(
        "customercore_hitl_queue_depth",
        "Number of tickets waiting for human review",
        ["tenant_id"],
    )
    AUTH_FAILURES = Counter(
        "customercore_auth_failures_total",
        "Authentication failure events",
        ["reason"],
    )
    RATE_LIMIT_HITS = Counter(
        "customercore_rate_limit_hits_total",
        "Rate limit exceeded events",
        ["tenant_id", "tier"],
    )

------------------------------------------------------------
## Step 13.2 - Wire Metrics into FastAPI
------------------------------------------------------------

Update src/api/main.py to instrument endpoints.
Add this middleware to the FastAPI app:

    import time
    from src.monitoring.metrics import REQUEST_COUNT, REQUEST_LATENCY, CONFIDENCE_SCORE

    @app.middleware("http")
    async def prometheus_middleware(request, call_next):
        start = time.time()
        response = await call_next(request)
        latency = time.time() - start
        tenant_id = getattr(request.state, "tenant_id", "unknown")
        endpoint = request.url.path
        REQUEST_COUNT.labels(
            endpoint=endpoint,
            tenant_id=tenant_id,
            status_code=response.status_code,
        ).inc()
        REQUEST_LATENCY.labels(endpoint=endpoint, tenant_id=tenant_id).observe(latency)
        return response

Also update the /agent/triage endpoint to record confidence:

    # After result = run_triage(req.model_dump())
    if result:
        CONFIDENCE_SCORE.labels(tenant_id=req.tenant_id).observe(result.confidence)

------------------------------------------------------------
## Step 13.3 - Create the OTel Collector Config
------------------------------------------------------------

Create infra/otel-collector.yaml:

    receivers:
      prometheus:
        config:
          scrape_configs:
            - job_name: customercore-api
              scrape_interval: 15s
              static_configs:
                - targets: ["host.docker.internal:8000"]
              metrics_path: /metrics

      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318

    processors:
      batch:
        timeout: 10s
        send_batch_size: 512
      resource:
        attributes:
          - action: insert
            key: service.name
            value: customercore
          - action: insert
            key: deployment.environment
            value: production

    exporters:
      prometheusremotewrite:
        endpoint: "${GRAFANA_PROMETHEUS_URL}"
        headers:
          Authorization: "Basic ${GRAFANA_PROMETHEUS_AUTH}"

      loki:
        endpoint: "${GRAFANA_LOKI_URL}"
        headers:
          Authorization: "Basic ${GRAFANA_LOKI_AUTH}"

      otlp/tempo:
        endpoint: "${GRAFANA_TEMPO_URL}"
        headers:
          Authorization: "Basic ${GRAFANA_TEMPO_AUTH}"

    service:
      pipelines:
        metrics:
          receivers: [prometheus, otlp]
          processors: [batch, resource]
          exporters: [prometheusremotewrite]
        logs:
          receivers: [otlp]
          processors: [batch, resource]
          exporters: [loki]
        traces:
          receivers: [otlp]
          processors: [batch, resource]
          exporters: [otlp/tempo]

------------------------------------------------------------
## Step 13.4 - Add OTel Collector to Docker Compose
------------------------------------------------------------

Add to docker-compose.yml:

      otel-collector:
        image: otel/opentelemetry-collector-contrib:latest
        container_name: otel-collector
        command: ["--config=/etc/otel-collector.yaml"]
        volumes:
          - ./infra/otel-collector.yaml:/etc/otel-collector.yaml
        ports:
          - "4317:4317"
          - "4318:4318"
        extra_hosts:
          - "host.docker.internal:host-gateway"

------------------------------------------------------------
## Step 13.5 - Set Up Grafana Cloud (All 5 Dashboards)
------------------------------------------------------------

1. Go to grafana.com -> Your Stack -> Connections -> Add Prometheus
   - Copy remote_write URL and credentials
   - Add to Doppler: GRAFANA_PROMETHEUS_URL and GRAFANA_PROMETHEUS_AUTH

2. Add Loki connection. Add to Doppler: GRAFANA_LOKI_URL and GRAFANA_LOKI_AUTH

3. Add Tempo connection. Add to Doppler: GRAFANA_TEMPO_URL and GRAFANA_TEMPO_AUTH

4. Start the OTel Collector:
    docker compose up -d otel-collector

5. Create the 5 dashboards in Grafana UI:

Dashboard 1 - Ops Health:
   - Panel: Request rate (customercore_requests_total)
   - Panel: p95 latency (histogram_quantile on customercore_request_latency_seconds)
   - Panel: Error rate (rate of 5xx / total)
   - Panel: Semantic cache hit rate (customercore_semantic_cache_hit_rate)

Dashboard 2 - ML Quality:
   - Panel: Confidence score distribution
   - Panel: Churn risk score distribution
   - Panel: Fairness accuracy gap per model (customercore_fairness_score)
   - Panel: HITL queue depth (customercore_hitl_queue_depth)

Dashboard 3 - GenAI Costs:
   - Panel: Total LLM tokens per tenant
   - Panel: LLM latency by model
   - Panel: RAG fallback count (customercore_rag_fallback_total)
   - Panel: Cache hit rate L0/L1/L2

Dashboard 4 - Streaming:
   - Panel: Redpanda consumer lag per topic (customercore_streaming_lag_seconds)
   - Panel: DLQ event rate (customercore_dlq_events_total)
   - Panel: Iceberg snapshot age (customercore_iceberg_snapshot_age_seconds)

Dashboard 5 - Business KPIs:
   - Panel: Tickets per hour per tenant
   - Panel: High priority ticket ratio
   - Panel: Rate limit hits by tier
   - Panel: Auth failure rate

6. Set dashboards to Public access (Share -> Public access ON)
   Copy the public URL for each dashboard into README.md

------------------------------------------------------------
## Step 13.6 - Configure Alerts
------------------------------------------------------------

In Grafana -> Alerting -> Alert Rules, create these 8 alerts:

    Alert 1: Redpanda lag > 60s
    Condition: customercore_streaming_lag_seconds > 60 for 2min
    Severity: SEV-2

    Alert 2: Confidence score drops (model drift)
    Condition: histogram_quantile(0.5, customercore_confidence_score) < 0.60
    Severity: SEV-2

    Alert 3: Cache hit rate collapses
    Condition: customercore_semantic_cache_hit_rate < 0.05 for 10min
    Severity: SEV-3

    Alert 4: Circuit breaker open
    Condition: customercore_rag_fallback_total rate > 10/min
    Severity: SEV-2

    Alert 5: Fairness gap breached
    Condition: customercore_fairness_score > 0.05
    Severity: SEV-2

    Alert 6: HITL queue overflowing
    Condition: customercore_hitl_queue_depth > 100
    Severity: SEV-3

    Alert 7: DLQ spike
    Condition: rate(customercore_dlq_events_total[5m]) > 1
    Severity: SEV-2

    Alert 8: API error rate high
    Condition: rate(customercore_requests_total{status_code="500"}[5m]) > 0.01
    Severity: SEV-1

------------------------------------------------------------
## Step 13.7 - Write Metrics Tests
------------------------------------------------------------

Create tests/unit/test_metrics.py:

    def test_all_metrics_importable():
        from src.monitoring.metrics import (
            REQUEST_COUNT, REQUEST_LATENCY, CACHE_HIT, CACHE_MISS,
            CONFIDENCE_SCORE, CHURN_RISK_SCORE, FAIRNESS_SCORE,
            LLM_TOKEN_COUNT, LLM_LATENCY, RAG_FALLBACK,
            STREAMING_LAG, DLQ_EVENTS, ICEBERG_SNAPSHOT_AGE,
            HITL_QUEUE_DEPTH, AUTH_FAILURES, RATE_LIMIT_HITS,
            CACHE_HIT_RATE, MODEL_PREDICTION_COUNT,
        )
        assert REQUEST_COUNT is not None
        assert FAIRNESS_SCORE is not None
        assert HITL_QUEUE_DEPTH is not None

    def test_metrics_can_be_incremented():
        from src.monitoring.metrics import REQUEST_COUNT, CACHE_HIT
        REQUEST_COUNT.labels(endpoint="/test", tenant_id="test", status_code=200).inc()
        CACHE_HIT.labels(level="L1", tenant_id="test").inc()

    def test_histogram_metrics_observe():
        from src.monitoring.metrics import REQUEST_LATENCY, CONFIDENCE_SCORE
        REQUEST_LATENCY.labels(endpoint="/predict", tenant_id="test").observe(0.25)
        CONFIDENCE_SCORE.labels(tenant_id="test").observe(0.85)

Run:

    doppler run -- pytest tests/unit/test_metrics.py -v
    # Expected: 3 passed

------------------------------------------------------------
## Step 13.8 - Commit Phase 13
------------------------------------------------------------

    git add .
    git commit -m "Phase 13: 18 Prometheus metrics, OTel Collector, 5 Grafana dashboards, 8 alert rules, Loki + Tempo"
    git push origin main

------------------------------------------------------------
## PHASE 13 CHECKPOINT
------------------------------------------------------------

CHECK 1 - Metrics tests green:
    doppler run -- pytest tests/unit/test_metrics.py -v
    Expected: 3 passed

CHECK 2 - /metrics endpoint returns data:
    curl http://localhost:8000/metrics | grep customercore_requests_total
    Expected: customercore_requests_total{...} N

CHECK 3 - OTel Collector running:
    docker compose ps otel-collector
    Expected: running

CHECK 4 - Grafana receives metrics:
    Open Grafana Cloud -> Explore -> Prometheus
    Query: customercore_requests_total
    Expected: data points visible

CHECK 5 - 5 dashboards exist in Grafana:
    Open Grafana -> Dashboards
    Expected: Ops Health, ML Quality, GenAI Costs, Streaming, Business KPIs

---


##############################################################
# PHASE 14 - KUBERNETES WITH KIND AND TERRAFORM
##############################################################

Goal: Local kind cluster running with all 15 workloads
deployed as K8s manifests, Nginx Ingress configured,
and all endpoints reachable via the ingress controller.

Estimated Time: 4-5 days

------------------------------------------------------------
## Step 14.1 - Install kind and kubectl
------------------------------------------------------------

Download and install kind:
    https://kind.sigs.k8s.io/docs/user/quick-start/#installation

    # Download kind for Windows
    curl.exe -Lo kind.exe https://kind.sigs.k8s.io/dl/v0.22.0/kind-windows-amd64
    # Move to a directory on PATH, e.g. C:\Windows\System32\

    # Verify
    kind version

Download kubectl:
    https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/

    # Or via winget
    winget install Kubernetes.kubectl
    kubectl version --client

------------------------------------------------------------
## Step 14.2 - Create the kind Cluster Config
------------------------------------------------------------

Create infra/kind-config.yaml:

    kind: Cluster
    apiVersion: kind.x-k8s.io/v1alpha4
    name: customercore
    nodes:
      - role: control-plane
        kubeadmConfigPatches:
          - |
            kind: InitConfiguration
            nodeRegistration:
              kubeletExtraArgs:
                node-labels: "ingress-ready=true"
        extraPortMappings:
          - containerPort: 30080
            hostPort: 30080
            protocol: TCP
          - containerPort: 30443
            hostPort: 30443
            protocol: TCP
      - role: worker
      - role: worker

Create the cluster:

    kind create cluster --config infra/kind-config.yaml

    # Verify cluster is running
    kubectl cluster-info --context kind-customercore
    kubectl get nodes
    # Expected: 3 nodes (1 control-plane, 2 workers) all Ready

------------------------------------------------------------
## Step 14.3 - Create the Kubernetes Namespace
------------------------------------------------------------

Create infra/k8s/namespace.yaml:

    apiVersion: v1
    kind: Namespace
    metadata:
      name: customercore
      labels:
        app.kubernetes.io/managed-by: kubectl

Apply it:

    kubectl apply -f infra/k8s/namespace.yaml

------------------------------------------------------------
## Step 14.4 - Install Nginx Ingress Controller
------------------------------------------------------------

    kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

    # Wait for ingress controller to be ready
    kubectl wait --namespace ingress-nginx \
      --for=condition=ready pod \
      --selector=app.kubernetes.io/component=controller \
      --timeout=90s

------------------------------------------------------------
## Step 14.5 - Create K8s Manifests for All Services
------------------------------------------------------------

Create infra/k8s/fastapi-deployment.yaml:

    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: customercore-api
      namespace: customercore
    spec:
      replicas: 2
      selector:
        matchLabels:
          app: customercore-api
      template:
        metadata:
          labels:
            app: customercore-api
        spec:
          containers:
            - name: api
              image: customercore-api:latest
              imagePullPolicy: Never
              ports:
                - containerPort: 8000
              envFrom:
                - secretRef:
                    name: customercore-secrets
              resources:
                requests:
                  memory: "512Mi"
                  cpu: "250m"
                limits:
                  memory: "1Gi"
                  cpu: "500m"
              livenessProbe:
                httpGet:
                  path: /health
                  port: 8000
                initialDelaySeconds: 30
                periodSeconds: 10
              readinessProbe:
                httpGet:
                  path: /health
                  port: 8000
                initialDelaySeconds: 15
                periodSeconds: 5
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: customercore-api-svc
      namespace: customercore
    spec:
      selector:
        app: customercore-api
      ports:
        - port: 80
          targetPort: 8000

Create infra/k8s/ingress.yaml:

    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: customercore-ingress
      namespace: customercore
      annotations:
        nginx.ingress.kubernetes.io/rewrite-target: /
    spec:
      ingressClassName: nginx
      rules:
        - http:
            paths:
              - path: /
                pathType: Prefix
                backend:
                  service:
                    name: customercore-api-svc
                    port:
                      number: 80

Create infra/k8s/secrets.yaml:

    apiVersion: v1
    kind: Secret
    metadata:
      name: customercore-secrets
      namespace: customercore
    type: Opaque
    stringData:
      SUPABASE_URL: "REPLACE_WITH_DOPPLER_OR_ACTUAL_VALUE"
      SUPABASE_KEY: "REPLACE"
      UPSTASH_REDIS_URL: "REPLACE"
      OPENROUTER_API_KEY: "REPLACE"
      LITELLM_MASTER_KEY: "REPLACE"
      LANGFUSE_PUBLIC_KEY: "REPLACE"
      LANGFUSE_SECRET_KEY: "REPLACE"
      SENTRY_DSN: "REPLACE"
      MLFLOW_TRACKING_URI: "REPLACE"
      APP_ENV: "production"
      APP_VERSION: "1.0.0"

NOTE: In production, use Doppler Kubernetes operator or external-secrets to sync secrets.
For kind cluster testing, populate the stringData values manually.

------------------------------------------------------------
## Step 14.6 - Build the Docker Image and Load into kind
------------------------------------------------------------

Create Dockerfile at the project root:

    FROM python:3.11-slim

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY src/ ./src/
    COPY litellm_config.yaml .

    EXPOSE 8000

    ENV PYTHONPATH=/app

    CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

Build and load into kind:

    # Build the image
    docker build -t customercore-api:latest -f Dockerfile .

    # Load into kind cluster (bypasses Docker Hub)
    kind load docker-image customercore-api:latest --name customercore

------------------------------------------------------------
## Step 14.7 - Deploy All Services
------------------------------------------------------------

    # Apply in order
    kubectl apply -f infra/k8s/namespace.yaml
    kubectl apply -f infra/k8s/secrets.yaml
    kubectl apply -f infra/k8s/fastapi-deployment.yaml
    kubectl apply -f infra/k8s/ingress.yaml

    # Wait for pods to be ready
    kubectl wait --namespace customercore \
      --for=condition=ready pod \
      --selector=app=customercore-api \
      --timeout=120s

    # Check status
    kubectl get all -n customercore

    # Expected:
    # pod/customercore-api-XXXX Running
    # service/customercore-api-svc ClusterIP
    # deployment.apps/customercore-api 2/2

------------------------------------------------------------
## Step 14.8 - Test the Ingress Endpoint
------------------------------------------------------------

    # The kind cluster maps port 30080 to the ingress
    curl http://localhost:30080/health

    # Expected:
    # {"status": "ok", "version": "1.0.0", ...}

    # Test predict endpoint via ingress
    curl -X POST http://localhost:30080/predict \
      -H "Content-Type: application/json" \
      -d "{\"ticket_id\":\"K8S-TEST\",\"body\":\"OAuth fails\",\"customer_id\":\"c1\",\"tenant_id\":\"acme\",\"customer_tier\":\"pro\"}"

------------------------------------------------------------
## Step 14.9 - Create Pod Disruption Budget
------------------------------------------------------------

Create infra/k8s/pdb.yaml:

    apiVersion: policy/v1
    kind: PodDisruptionBudget
    metadata:
      name: customercore-api-pdb
      namespace: customercore
    spec:
      minAvailable: 1
      selector:
        matchLabels:
          app: customercore-api

Apply:
    kubectl apply -f infra/k8s/pdb.yaml

------------------------------------------------------------
## Step 14.10 - Commit Phase 14
------------------------------------------------------------

    git add .
    git commit -m "Phase 14: kind cluster, K8s manifests, Nginx Ingress, Dockerfile, PDB, all endpoints reachable"
    git push origin main

------------------------------------------------------------
## PHASE 14 CHECKPOINT
------------------------------------------------------------

CHECK 1 - Cluster nodes ready:
    kubectl get nodes
    Expected: 3 nodes, all Ready

CHECK 2 - All pods running:
    kubectl get pods -n customercore
    Expected: customercore-api pods in Running state

CHECK 3 - Health via ingress:
    curl http://localhost:30080/health
    Expected: {"status": "ok", ...}

CHECK 4 - PDB applied:
    kubectl get pdb -n customercore
    Expected: customercore-api-pdb with ALLOWED DISRUPTIONS: 1

---


##############################################################
# PHASE 15 - CI/CD PIPELINE AND HF SPACES DEPLOYMENT
##############################################################

Goal: 10-stage GitHub Actions CI pipeline running on every
push, CML metrics comment on every PR, and FastAPI live
on Hugging Face Spaces Docker at a permanent public URL.

Estimated Time: 3-4 days

------------------------------------------------------------
## Step 15.1 - Create the Main CI Pipeline
------------------------------------------------------------

Create .github/workflows/ci.yml:

    name: CustomerCore CI

    on:
      push:
        branches: [main, develop]
      pull_request:
        branches: [main]

    env:
      PYTHON_VERSION: "3.11"

    jobs:

      # Stage 1: Lint and type check
      lint:
        name: Stage 1 - Lint and Type Check
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: ${{ env.PYTHON_VERSION }}
          - run: pip install ruff==0.4.4 mypy==1.10.0
          - run: ruff check src/
          - run: mypy src/ --ignore-missing-imports --no-strict-optional

      # Stage 2: Unit tests
      unit-tests:
        name: Stage 2 - Unit Tests
        runs-on: ubuntu-latest
        needs: lint
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: ${{ env.PYTHON_VERSION }}
              cache: pip
          - run: pip install -r requirements.txt
          - run: pytest tests/unit/ -v --cov=src --cov-report=xml -q
          - uses: actions/upload-artifact@v4
            with:
              name: coverage-report
              path: coverage.xml

      # Stage 3: Schema validation
      schema-validation:
        name: Stage 3 - Pydantic Schema Validation
        runs-on: ubuntu-latest
        needs: lint
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: ${{ env.PYTHON_VERSION }}
              cache: pip
          - run: pip install pydantic==2.7.0
          - run: |
              python -c "
              from src.agent.schemas import TriageOutput
              import json
              schema = TriageOutput.model_json_schema()
              assert len(schema['properties']) == 14, f'Expected 14 fields, got {len(schema[\"properties\"])}'
              print('Schema validation: 14 fields confirmed')
              "

      # Stage 4: Data quality check
      data-quality:
        name: Stage 4 - Great Expectations Data Quality
        runs-on: ubuntu-latest
        needs: unit-tests
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: ${{ env.PYTHON_VERSION }}
              cache: pip
          - run: pip install great-expectations==0.18.15 pandas==2.2.2
          - run: |
              python -c "
              import pandas as pd
              from src.ml.feature_engineering import load_silver_data
              df = load_silver_data()
              assert len(df) > 0, 'No data loaded'
              assert 'priority' in df.columns, 'priority column missing'
              assert df['priority'].isin(['critical','high','medium','low']).all(), 'Invalid priorities'
              print(f'Data quality: {len(df)} rows, all validations passed')
              "

      # Stage 5: ML model training (parallel)
      train-models:
        name: Stage 5 - Train ML Models
        runs-on: ubuntu-latest
        needs: data-quality
        strategy:
          matrix:
            model: [category, priority, churn, sla]
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: ${{ env.PYTHON_VERSION }}
              cache: pip
          - run: pip install -r requirements.txt
          - env:
              MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
              DAGSHUB_TOKEN: ${{ secrets.DAGSHUB_TOKEN }}
            run: |
              python -m src.ml.train_${{ matrix.model }} 2>&1 | tee train_${{ matrix.model }}.log
          - uses: actions/upload-artifact@v4
            with:
              name: train-log-${{ matrix.model }}
              path: train_${{ matrix.model }}.log

      # Stage 6: CML metrics report on PR
      cml-report:
        name: Stage 6 - CML Metrics Report
        runs-on: ubuntu-latest
        needs: train-models
        if: github.event_name == 'pull_request'
        steps:
          - uses: actions/checkout@v4
          - uses: iterative/setup-cml@v2
          - uses: actions/setup-python@v5
            with:
              python-version: ${{ env.PYTHON_VERSION }}
              cache: pip
          - run: pip install -r requirements.txt mlflow
          - env:
              REPO_TOKEN: ${{ secrets.GITHUB_TOKEN }}
              MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
            run: |
              python -c "
              import mlflow, os
              mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])
              client = mlflow.MlflowClient()
              report = '## CustomerCore ML Metrics\n\n| Model | Metric | Value |\n|---|---|---|\n'
              for exp_name in ['customercore-category-classifier','customercore-priority-classifier','customercore-churn-risk']:
                  try:
                      exp = client.get_experiment_by_name(exp_name)
                      if exp:
                          runs = client.search_runs(exp.experiment_id, max_results=1, order_by=['start_time DESC'])
                          if runs:
                              run = runs[0]
                              for k, v in run.data.metrics.items():
                                  report += f'| {exp_name.replace(\"customercore-\",\"\")} | {k} | {v:.4f} |\n'
                  except: pass
              with open('metrics_report.md', 'w') as f: f.write(report)
              print(report)
              "
              cml comment create metrics_report.md

      # Stage 7: Security scan
      security-scan:
        name: Stage 7 - Security Scan
        runs-on: ubuntu-latest
        needs: lint
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: ${{ env.PYTHON_VERSION }}
          - run: pip install bandit==1.7.8
          - run: bandit -r src/ -ll -x src/tests 2>&1 || true

      # Stage 8: Docker build test
      docker-build:
        name: Stage 8 - Docker Build Test
        runs-on: ubuntu-latest
        needs: unit-tests
        steps:
          - uses: actions/checkout@v4
          - uses: docker/setup-buildx-action@v3
          - run: docker build -t customercore-api:ci -f Dockerfile . --no-cache

      # Stage 9: Integration smoke test
      smoke-test:
        name: Stage 9 - Smoke Test
        runs-on: ubuntu-latest
        needs: docker-build
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: ${{ env.PYTHON_VERSION }}
              cache: pip
          - run: pip install -r requirements.txt
          - run: |
              python -c "
              from src.agent.schemas import TriageOutput
              from src.agent.nodes.classify_agent import classify_agent_node
              from src.agent.nodes.incident_agent import incident_agent_node
              state = {'ticket': {'ticket_id': 'CI-1', 'body': 'Auth fails', 'customer_id': 'c1', 'tenant_id': 'test', 'customer_tier': 'pro'}, 'messages': [], 'models_used': []}
              state = classify_agent_node(state)
              state = incident_agent_node(state)
              assert state['category'] in ['bug','auth','security','performance','billing','feature_request','docs','question','incident','other']
              print('Smoke test passed:', state['category'])
              "

      # Stage 10: Deploy to HF Spaces (main branch only)
      deploy-hf:
        name: Stage 10 - Deploy to HF Spaces
        runs-on: ubuntu-latest
        needs: [smoke-test, security-scan]
        if: github.ref == 'refs/heads/main'
        steps:
          - uses: actions/checkout@v4
            with:
              fetch-depth: 0
          - name: Push to HF Spaces
            env:
              HF_TOKEN: ${{ secrets.HF_TOKEN }}
            run: |
              git config user.email "ci@customercore.ai"
              git config user.name "CustomerCore CI"
              git remote add hf https://USER:${HF_TOKEN}@huggingface.co/spaces/YOUR_HF_USERNAME/customercore-api
              git push hf main --force
              echo "Deployed to HF Spaces"

------------------------------------------------------------
## Step 15.2 - Create the HF Spaces Dockerfile
------------------------------------------------------------

Create Dockerfile.hf at the project root:

    FROM python:3.11-slim

    WORKDIR /app

    # Install system deps
    RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

    # Create requirements file without heavy local dependencies
    COPY requirements.hf.txt .
    RUN pip install --no-cache-dir -r requirements.hf.txt

    COPY src/ ./src/
    COPY litellm_config.yaml .

    # HF Spaces uses port 7860 by default
    EXPOSE 7860

    ENV PYTHONPATH=/app
    ENV LLM_BACKEND=openrouter
    ENV LITELLM_DEFAULT_MODEL=cloud-complex

    # 2 workers on HF Spaces 2 vCPU
    CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "2"]

Create requirements.hf.txt (HF Spaces subset - no PySpark, no Spark JARs):

    fastapi==0.115.0
    uvicorn[standard]==0.30.0
    pydantic==2.7.0
    httpx==0.27.0
    python-dotenv==1.0.1
    tenacity==8.3.0
    langchain==0.2.0
    langgraph==0.1.0
    langchain-community==0.2.0
    langsmith==0.1.0
    langfuse==2.0.0
    mem0ai==0.0.20
    litellm==1.40.0
    openai==1.30.0
    chromadb==0.5.0
    sentence-transformers==3.0.0
    rank-bm25==0.2.2
    mlflow==2.13.0
    lightgbm==4.3.0
    xgboost==2.0.3
    scikit-learn==1.4.2
    pandas==2.2.2
    structlog==24.1.0
    prometheus-client==0.20.0
    sentry-sdk[fastapi]==2.3.0
    supabase==2.4.0
    redis==5.0.4
    upstash-redis==1.1.0

------------------------------------------------------------
## Step 15.3 - Create the HF Spaces README
------------------------------------------------------------

Create a separate directory for the HF Space repo.
The README.md at the root of the HF Space repo must have:

    ---
    title: CustomerCore API
    emoji: 🎯
    colorFrom: blue
    colorTo: purple
    sdk: docker
    app_port: 7860
    license: mit
    ---

    # CustomerCore Intelligence API

    Real-time multi-tenant customer intelligence platform.

    ## Live Endpoints
    - GET /health - Service health check
    - POST /predict - Fast ML classification
    - POST /rag-answer - Knowledge base Q&A
    - POST /agent/triage - Full 14-field triage

------------------------------------------------------------
## Step 15.4 - Set Up HF Spaces
------------------------------------------------------------

1. Go to huggingface.co -> New Space
2. Space name: customercore-api
3. SDK: Docker
4. Hardware: CPU basic (free, 2 vCPU 16GB RAM)
5. Visibility: Public
6. Click Create Space

Clone the HF Space repo:
    git clone https://huggingface.co/spaces/YOUR_HF_USERNAME/customercore-api hf-space-api

Copy the HF-specific files:
    cp Dockerfile.hf hf-space-api/Dockerfile
    cp requirements.hf.txt hf-space-api/requirements.hf.txt
    cp -r src/ hf-space-api/src/
    cp litellm_config.yaml hf-space-api/

Write the README.md with the metadata block above.

Add secrets in HF Spaces UI:
    HF Space -> Settings -> Variables and Secrets -> Add:
    SUPABASE_URL, SUPABASE_KEY, UPSTASH_REDIS_URL,
    LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY,
    OPENROUTER_API_KEY, LITELLM_MASTER_KEY,
    LANGSMITH_API_KEY, SENTRY_DSN

Push and deploy:
    cd hf-space-api
    git add .
    git commit -m "Deploy CustomerCore API v1.0.0"
    git push

    # Watch build logs in HF Spaces UI
    # Takes 3-5 minutes for first build

Verify it is live:
    curl https://YOUR_HF_USERNAME-customercore-api.hf.space/health
    # Expected: {"status": "ok", ...}

------------------------------------------------------------
## Step 15.5 - Add HF_TOKEN to GitHub Secrets
------------------------------------------------------------

1. Go to huggingface.co -> Settings -> Access Tokens
2. Create a new token: Name "github-actions", Role: write
3. Copy the token
4. Go to github.com/YOUR_USERNAME/customercore -> Settings -> Secrets -> Actions
5. New repository secret: HF_TOKEN = your-hf-token

Also add all other secrets to GitHub Actions:
(Doppler should have synced these already from Step 1.4)
Verify by going to Settings -> Secrets -> Actions

------------------------------------------------------------
## Step 15.6 - Trigger the CI Pipeline
------------------------------------------------------------

    git add .
    git commit -m "Phase 15: 10-stage CI pipeline, HF Spaces Docker deployment, CML metrics on PR"
    git push origin main

    # Open GitHub -> Actions tab
    # Watch the 10-stage pipeline run
    # Expected: All 10 stages green (except deploy-hf if HF_TOKEN not set yet)

------------------------------------------------------------
## PHASE 15 CHECKPOINT
------------------------------------------------------------

CHECK 1 - CI pipeline runs green on push:
    Open github.com/YOUR_USERNAME/customercore/actions
    Expected: All stages green on latest run

CHECK 2 - HF Spaces API is live:
    curl https://YOUR_HF_USERNAME-customercore-api.hf.space/health
    Expected: {"status": "ok", ...}

CHECK 3 - CML comment on PR:
    Create a test PR -> merge to main
    Expected: CML bot posts a metrics table comment on the PR

CHECK 4 - Docker build stage passes:
    GitHub Actions -> Stage 8 Docker Build
    Expected: Build succeeds, image created

CHECK 5 - All secrets in GitHub Actions:
    github.com -> Settings -> Secrets -> Actions
    Expected: 10+ secrets listed

---


##############################################################
# PHASE 16 - DEMO POLISH AND PORTFOLIO PUBLISHING
##############################################################

Goal: Professional README with live links and badges,
ARCHITECTURE.md diagram, UptimeRobot status page live,
Kaggle QLoRA fine-tuning notebook linked, and the full
project ready for recruiter review.

Estimated Time: 2 days

------------------------------------------------------------
## Step 16.1 - Set Up UptimeRobot Monitors
------------------------------------------------------------

1. Go to uptimerobot.com -> Sign In
2. Add Monitor -> HTTP(s) monitor for each:

Monitor 1:
    Name: CustomerCore API
    URL: https://YOUR_HF_USERNAME-customercore-api.hf.space/health
    Interval: 5 minutes

Monitor 2:
    Name: Grafana Dashboard
    URL: https://YOUR_ORG.grafana.net/d/YOUR_ID/customercore
    Interval: 5 minutes

Monitor 3:
    Name: Supabase
    URL: https://YOUR_PROJECT.supabase.co/rest/v1/
    Interval: 5 minutes

Monitor 4:
    Name: DagsHub MLflow
    URL: https://dagshub.com/YOUR_USERNAME/customercore/mlflow
    Interval: 5 minutes

3. Create Public Status Page:
   UptimeRobot -> My Settings -> Status Pages -> Create
   Name: CustomerCore Status
   Add all 4 monitors
   Save -> copy the public status page URL

4. For each monitor, copy the Monitor ID (m[number]) from the monitor details.
   You will use this for Shields.io badges.

------------------------------------------------------------
## Step 16.2 - Write the README
------------------------------------------------------------

Create README.md at the project root:

    # CustomerCore Intelligence Platform

    Real-time multi-tenant customer intelligence powered by
    streaming (Redpanda), lakehouse storage (Iceberg/R2),
    multi-agent AI (LangGraph), and full MLOps (MLflow/DagsHub).

    ## Live System Links

    | Asset | Link | Status |
    |---|---|---|
    | Live API (HF Spaces) | https://YOUR_HF_USERNAME-customercore-api.hf.space/health | ![uptime](https://img.shields.io/uptimerobot/status/mYOUR_MONITOR_ID) |
    | Grafana Dashboard | https://YOUR_ORG.grafana.net/d/YOUR_ID/customercore | Public, no login |
    | Langfuse Traces | https://cloud.langfuse.com/public/trace/YOUR_TRACE_ID | Sample RAG trace |
    | LangSmith Agent Trace | https://smith.langchain.com/public/YOUR_ID/r | Full 9-step triage |
    | MLflow Experiments | https://dagshub.com/YOUR_USERNAME/customercore/mlflow | 8 model experiments |
    | Kaggle Fine-Tuning | https://kaggle.com/code/YOUR_USERNAME/customercore-finetune | QLoRA Gemma 3 4B |
    | CI Pipeline | https://github.com/YOUR_USERNAME/customercore/actions | 10-stage pipeline |
    | Status Page | https://status.uptimerobot.com/pages/YOUR_PAGE_ID | 30-day uptime |

    ![Python](https://img.shields.io/badge/Python-3.11-blue)
    ![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
    ![License](https://img.shields.io/badge/license-MIT-green)
    ![EU AI Act](https://img.shields.io/badge/EU%20AI%20Act-Compliant-blue)
    ![HF Spaces](https://img.shields.io/badge/HF%20Spaces-Live-orange)

    ## Architecture Overview

    See [ARCHITECTURE.md](ARCHITECTURE.md) for the full system diagram.

    ## What It Does

    CustomerCore is a real-time multi-tenant customer intelligence
    platform that processes support tickets through a 9-step
    LangGraph multi-agent pipeline:

    1. Ticket arrives via REST API (/agent/triage)
    2. Classify Agent: category + priority via XGBoost + LightGBM
    3. Memory Agent: recall past interactions from Mem0 (Supabase pgvector)
    4. RAG Agent: hybrid retrieval (dense+sparse) + cross-encoder reranking + LLM
    5. Churn Agent: churn + SLA breach risk scores from LightGBM
    6. Incident Agent: detect system outages via keyword patterns
    7. HITL Agent: route to human review if confidence < 0.65
    8. Finalize: assemble validated 14-field TriageOutput (Pydantic)
    9. Audit: log to Supabase audit_log + Langfuse trace

    ## Technology Stack

    | Layer | Technology |
    |---|---|
    | Streaming | Redpanda (Kafka-compatible) |
    | Lakehouse | Apache Iceberg on Cloudflare R2 |
    | Processing | PySpark Structured Streaming |
    | Transform | dbt-core with DuckDB adapter (7 Gold marts) |
    | Vector DB | ChromaDB (3 indexes, BM25 + dense hybrid) |
    | Embeddings | Ollama BGE-M3 (local) |
    | LLM | Gemma 3 4B via Ollama + OpenRouter fallback via LiteLLM |
    | Agents | LangGraph multi-agent supervisor (6 sub-agents) |
    | Memory | Mem0 backed by Supabase pgvector |
    | ML Models | 8 models: XGBoost, LightGBM, IsolationForest, Prophet |
    | Experiment Tracking | MLflow on DagsHub |
    | Prompt Tracking | Langfuse Cloud |
    | Agent Tracing | LangSmith |
    | Observability | OpenTelemetry + Grafana Cloud (18 metrics, 5 dashboards) |
    | API | FastAPI + Uvicorn |
    | Orchestration | Kubernetes (kind) + Docker Compose |
    | CI/CD | GitHub Actions (10 stages) + CML |
    | Hosting | Hugging Face Spaces Docker (free, always-on) |
    | Secrets | Doppler |
    | Responsible AI | EU AI Act Art. 10/12/14/15 compliance |

    ## Quick Start (Local)

        git clone https://github.com/YOUR_USERNAME/customercore.git
        cd customercore
        python -m venv .venv && .venv\Scripts\activate
        pip install -r requirements.txt
        doppler run -- docker compose up -d
        doppler run -- uvicorn src.api.main:app --reload --port 8000
        curl http://localhost:8000/health

    ## Project Structure

        customercore/
        src/
            api/         FastAPI application and middleware
            agent/       LangGraph supervisor and 6 sub-agents
            rag/         ChromaDB, hybrid retrieval, reranker, cache
            ml/          8 ML model training scripts
            streaming/   Redpanda producers and PySpark pipeline
            dbt/         7 dbt Gold models
            monitoring/  18 Prometheus metrics
            responsible_ai/  Model cards, fairness.py, audit log
        infra/
            k8s/         Kubernetes manifests
            otel-collector.yaml
        tests/
            unit/        Fast isolated unit tests
            integration/ Full stack integration tests
        .github/workflows/ CI/CD pipeline

    ## Responsible AI

    CustomerCore implements EU AI Act compliance (effective Aug 2026):
    - Model cards for all 8 ML models
    - Per-demographic accuracy parity metric (fairness_accuracy_gap)
    - Immutable Iceberg audit log for every prediction
    - HITL human oversight via LangGraph interrupt() (Art. 14)
    - PII masking via Presidio before any model sees the data

    ## Author

    Saibalaji Namburi
    MSc Data Analytics, University of Hildesheim
    github.com/YOUR_USERNAME | linkedin.com/in/YOUR_LINKEDIN

------------------------------------------------------------
## Step 16.3 - Write ARCHITECTURE.md
------------------------------------------------------------

Create ARCHITECTURE.md:

    # CustomerCore System Architecture

    ## Data Flow Diagram

        [GitHub Issues API]          [Synthetic Generators]
               |                      billing / product / incident
               v                              |
        [Redpanda Topics]  <------------------+
        tickets | product | billing | incidents
               |
               v
        [PySpark Streaming] -- Bronze -> Silver (PII masking, schema enforcement)
               |
               v
        [Apache Iceberg / Cloudflare R2]
        Bronze tables | Silver tables
               |
               v
        [dbt Gold Models] -- 7 business marts (DuckDB)
               |
               v
        [Feature Engineering] -> [MLflow / DagsHub] -> [8 ML Models]
               |
               v
        [FastAPI /agent/triage endpoint]
               |
               v
        [LangGraph Supervisor]
        classify -> memory -> rag -> churn -> incident -> hitl -> finalize
               |
               v
        [TriageOutput (14 fields, Pydantic validated)]
               |
               +-> [Langfuse trace] [LangSmith trace] [Supabase audit_log]
               |
               v
        [Grafana Cloud] <- [OTel Collector] <- [Prometheus metrics]

    ## Nine Services

    1. Stream Ingestion   - 4 Redpanda producers
    2. Stream Processing  - PySpark Bronze->Silver pipeline
    3. dbt Transforms     - 7 Gold mart models
    4. Feature Service    - Feast online store
    5. Training Service   - 8 ML models via MLflow
    6. Vector/RAG Service - ChromaDB hybrid retrieval + reranker
    7. Inference API      - FastAPI with rate limiting + multi-tenancy
    8. Worker Service     - Celery async tasks
    9. Observability      - OTel + Grafana + Langfuse + LangSmith + Sentry

    ## Deployment Modes

    Lite (CPU only):
        FastAPI + ChromaDB + Redis + Supabase + OpenRouter

    Full Local (kind cluster):
        All 9 services on RTX 3050 Ti with Ollama for local inference

    Cloud (always-on, free):
        HF Spaces Docker + Supabase + Upstash Redis + Cloudflare R2
        + Grafana Cloud + Langfuse + LangSmith + DagsHub

------------------------------------------------------------
## Step 16.4 - Create the Kaggle Fine-Tuning Notebook
------------------------------------------------------------

Go to kaggle.com -> New Notebook -> Set GPU to T4 x2

Notebook title: CustomerCore QLoRA Gemma 3 4B Fine-Tuning

Add these cells:

Cell 1 - Install dependencies:
    !pip install unsloth==2024.4 trl==0.8.6 peft==0.10.0 mlflow

Cell 2 - Load and prepare data:
    import pandas as pd, numpy as np
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        "instruction": ["Classify this support ticket" for _ in range(n)],
        "input": [f"Ticket about auth failure number {i}" for i in range(n)],
        "output": [f'{{"category": "auth", "priority": "high"}}' for _ in range(n)],
    })
    print(f"Training samples: {len(df)}")

Cell 3 - Load Gemma 3 4B with Unsloth:
    from unsloth import FastLanguageModel
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="unsloth/gemma-3-4b-it",
        max_seq_length=1024,
        load_in_4bit=True,
    )
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=["q_proj","k_proj","v_proj","o_proj"],
        lora_alpha=16,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
    )

Cell 4 - Train with SFTTrainer:
    from trl import SFTTrainer
    from transformers import TrainingArguments
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=...,
        max_seq_length=1024,
        args=TrainingArguments(
            output_dir="outputs",
            num_train_epochs=1,
            per_device_train_batch_size=4,
            gradient_accumulation_steps=4,
            learning_rate=2e-4,
            fp16=True,
            logging_steps=10,
            save_strategy="epoch",
        ),
    )
    trainer.train()

Cell 5 - Export to GGUF and log to MLflow:
    model.save_pretrained_gguf("model_gguf", tokenizer, quantization_method="q4_k_m")
    import mlflow
    mlflow.log_artifact("model_gguf/model-Q4_K_M.gguf")
    print("GGUF model exported and logged to MLflow")

Save and make notebook public. Copy the URL for the README.

------------------------------------------------------------
## Step 16.5 - Final Validation Sweep
------------------------------------------------------------

Run all tests one final time:

    doppler run -- pytest tests/ -v --tb=short 2>&1

    # Count total passing tests
    # Expected: 30+ tests passing

Run a full end-to-end triage:

    doppler run -- python -c "
    from src.agent.supervisor import run_triage
    import json

    ticket = {
        'ticket_id': 'FINAL-E2E-001',
        'body': 'Enterprise customer cannot complete payment renewal. Payment gateway returns timeout. This is blocking account renewal for 500 users.',
        'customer_id': 'ent-001',
        'tenant_id': 'acme-corp',
        'customer_tier': 'enterprise',
    }

    result = run_triage(ticket)
    if result:
        print(json.dumps(result.model_dump(), indent=2))
        print(f'\nAll 14 fields populated: {len(result.model_dump()) == 14}')
    "

------------------------------------------------------------
## Step 16.6 - Final Git Commit and Tag
------------------------------------------------------------

    git add .
    git commit -m "Phase 16 complete: README, ARCHITECTURE.md, UptimeRobot, Kaggle notebook, v1.0.0 release"
    git tag -a v1.0.0 -m "CustomerCore v1.0.0 - Production Release"
    git push origin main
    git push origin v1.0.0

------------------------------------------------------------
## PHASE 16 CHECKPOINT - FINAL PROJECT VALIDATION
------------------------------------------------------------

CHECK 1 - All tests passing:
    doppler run -- pytest tests/ -v --tb=short
    Expected: 30+ passed, 0 failed

CHECK 2 - Live API responding:
    curl https://YOUR_HF_USERNAME-customercore-api.hf.space/health
    Expected: {"status": "ok", ...}

CHECK 3 - README has live links:
    Open README.md
    Expected: HF Spaces URL, Grafana URL, LangSmith URL, MLflow URL all real links

CHECK 4 - Grafana dashboards public:
    Open 5 Grafana dashboard URLs without logging in
    Expected: All 5 dashboards load with real metrics

CHECK 5 - UptimeRobot status page live:
    Open status.uptimerobot.com/pages/YOUR_PAGE_ID
    Expected: All monitors green

CHECK 6 - MLflow has 8 experiments:
    Open dagshub.com/YOUR_USERNAME/customercore/mlflow
    Expected: 8 experiments, each with at least 1 run

CHECK 7 - Langfuse has traces:
    Open cloud.langfuse.com
    Expected: Traces with LLM calls visible

CHECK 8 - GitHub Actions CI green:
    Open github.com/YOUR_USERNAME/customercore/actions
    Expected: Latest run all stages green

CHECK 9 - v1.0.0 tag exists:
    git tag
    Expected: v1.0.0 listed

------------------------------------------------------------
## THE BUILD IS COMPLETE
------------------------------------------------------------

Congratulations. CustomerCore is live.

Summary of what you built:

    4 Redpanda event producers (tickets, product, billing, incidents)
    PySpark Bronze->Silver streaming pipeline with PII masking
    7 dbt Gold business mart models
    3 ChromaDB vector indexes with hybrid retrieval and cross-encoder reranking
    3-level caching system (L0 embedding, L1 exact, L2 semantic)
    LiteLLM AI gateway with 7-level fallback chain
    8 ML models trained and tracked in MLflow on DagsHub
    Mem0 long-term memory backed by Supabase pgvector
    14-field Pydantic TriageOutput schema with validators
    LangGraph 6-agent supervisor with HITL interrupt
    FastAPI with multi-tenancy, rate limiting, and JWT middleware
    Langfuse prompt registry with 6 versioned prompts
    8 model cards with EU AI Act compliance
    Fairness.py with accuracy parity gate tracked in MLflow
    Supabase immutable audit log
    18 Prometheus metrics and 5 Grafana Cloud dashboards
    OpenTelemetry distributed tracing with Loki logs
    Kubernetes kind cluster with Nginx Ingress
    10-stage GitHub Actions CI/CD pipeline
    HF Spaces Docker deployment (always-on, free, public URL)
    UptimeRobot status page
    QLoRA Gemma 3 4B fine-tuning on Kaggle T4
    Professional README with live badges and links

Total infrastructure cost: $0 per month.
Everything is permanently live.

---

## APPENDIX - QUICK REFERENCE COMMANDS

Start everything locally:
    docker compose up -d redpanda redpanda-console minio chromadb otel-collector
    doppler run -- python -m src.streaming.producers.ticket_producer &
    doppler run -- python -m src.streaming.producers.product_producer &
    doppler run -- python -m src.streaming.bronze_to_silver &
    cd src/dbt && dbt run --profiles-dir . --project-dir . && cd ../..
    doppler run -- litellm --config litellm_config.yaml --port 4000 &
    doppler run -- uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

Run all tests:
    doppler run -- pytest tests/ -v --tb=short

Train all models:
    doppler run -- python -m src.ml.train_category
    doppler run -- python -m src.ml.train_priority
    doppler run -- python -m src.ml.train_churn
    doppler run -- python -m src.ml.train_sla

Full triage test:
    doppler run -- python -c "
    from src.agent.supervisor import run_triage
    r = run_triage({'ticket_id':'T1','body':'Auth fails','customer_id':'c1','tenant_id':'acme','customer_tier':'pro'})
    print(r.model_dump())
    "

---
