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

Add photoes
python -m app.recognition.face_recognizer enroll "Alice" path\to\alice_1.jpg path\to\alice_2.jpg
python -m app.recognition.face_recognizer list
python -m app.recognition.face_recognizer recognize path\to\camera_face.jpg


Or manually add photos here:
app/data/known_faces/Alice/alice_1.jpg
app/data/known_faces/Alice/alice_2.jpg

python -m app.recognition.face_recognizer rebuild



python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python main.py
```

The API starts at `http://localhost:8000`.

## Camera Performance

The camera preview is capped by `CAMERA_TARGET_FPS` to reduce CPU usage. Face detection is also throttled by `FACE_DETECTION_INTERVAL`, which controls how many preview frames pass between DeepFace detections.

For lower CPU and memory usage, start with:

```env
CAMERA_TARGET_FPS=5
FACE_DETECTION_INTERVAL=20
```

For smoother preview and more frequent detection, increase these values gradually.

## Known Face Enrollment

Known face photos are stored under `app/data/known_faces/`. The actual photos and generated embedding registry are ignored by git because they contain biometric data.

Enroll a person from one or more photos:

```bash
python -m app.recognition.face_recognizer enroll "Alice" path\to\alice_1.jpg path\to\alice_2.jpg
```

Or place photos manually in this structure:

```text
app/data/known_faces/
  Alice/
    alice_1.jpg
    alice_2.jpg
  Bob/
    bob_1.jpg
```

Then rebuild the embedding registry:

```bash
python -m app.recognition.face_recognizer rebuild
```

List enrolled people:

```bash
python -m app.recognition.face_recognizer list
```

Recognize a face image against enrolled people:

```bash
python -m app.recognition.face_recognizer recognize path\to\camera_face.jpg
```

Each enrollment copies photos into `app/data/known_faces/<person-name>/`, extracts DeepFace embeddings using RetinaFace, and saves them to `app/data/known_face_embeddings.json`.

The camera preview draws a green box for detection. It shows an enrolled person's name on that box only after embeddings exist; otherwise the label is `Unknown`.

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
