from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.graph import invoke
from app.logging_config import configure_logging
from app.observability import setup_observability
from app.security import InMemoryRateLimiter, looks_like_prompt_injection
from app.state import AskRequest, AskResponse

settings = get_settings()
configure_logging(settings.log_level)
setup_observability(settings.app_name)

app = FastAPI(title=settings.app_name, version="0.1.0")
rate_limiter = InMemoryRateLimiter(settings.rate_limit_per_minute)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    await rate_limiter.check(request)
    return await call_next(request)


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal server error", "error": str(exc)})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse("app/static/index.html")


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    if looks_like_prompt_injection(request.query):
        raise HTTPException(status_code=400, detail="Request failed prompt-injection validation")
    state = invoke(request.user_id, request.query)
    return AskResponse(
        answer=state.get("final_answer", ""),
        plan=state.get("plan", []),
        approval_required=state.get("approval_required", False),
        trace_id=state.get("metadata", {}).get("trace_id"),
        execution_trace=state.get("metadata", {}).get("execution_trace", []),
    )
