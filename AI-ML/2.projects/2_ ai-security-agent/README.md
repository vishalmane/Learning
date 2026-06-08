# ai-security-agent

Production-style starter structure for an Agentic AI Face Recognition System built with Python 3.12, FastAPI, OpenCV, DeepFace, LangGraph, and SQLAlchemy.

## Folder Tree

```text
2_ai-security-agent/
├── app/
│   ├── agents/          # Agent workflows for security decisions and notifications
│   ├── api/             # FastAPI route definitions and API wiring
│   ├── config/          # Application settings and environment configuration
│   ├── database/        # Database engine, sessions, and persistence helpers
│   ├── frontend/        # Streamlit or lightweight operator UI entrypoints
│   ├── logs/            # Runtime logs, kept out of git except .gitkeep
│   ├── memory/          # Vector memory and face embedding storage helpers
│   ├── models/          # Domain and database models
│   ├── recognition/     # Face embedding, matching, and identity recognition logic
│   ├── services/        # Application services such as alert delivery
│   ├── tests/           # Automated tests for the application
│   ├── utils/           # Shared utility functions
│   ├── vision/          # Camera capture and face detection pipeline
│   └── main.py          # FastAPI application factory and startup code
├── main.py              # Root Python entrypoint
├── requirements.txt     # Python dependencies
├── Dockerfile           # Python 3.12 container image
├── docker-compose.yml   # Local container orchestration
├── .env.example         # Example environment variables
└── .gitignore           # Project-specific ignored files
```

## Setup

```bash
uv venv --python 3.12
.venv\Scripts\activate
uv pip install -r requirements.txt
Run the FastAPI app:
uvicorn app.main:app --reload


python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python main.py
```

The API starts at `http://localhost:8000`.

## Useful Endpoints

- `GET /` returns the application status.
- `GET /health` returns a health check response.
- `POST /api/security-events` accepts a placeholder security event payload.

## Docker

```bash
copy .env.example .env
docker compose up --build
```

## Tests

```bash
pytest
```
