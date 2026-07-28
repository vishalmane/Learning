from typing import Any, TypedDict

from pydantic import BaseModel, Field


class HelpdeskState(TypedDict, total=False):
    user_id: str
    user_query: str
    plan: list[str]
    retrieved_docs: list[dict[str, Any]]
    tool_output: list[dict[str, Any]]
    reasoning_output: dict[str, Any]
    approval_required: bool
    final_answer: str
    conversation_history: list[dict[str, Any]]
    metadata: dict[str, Any]


class AskRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=128)
    query: str = Field(min_length=1, max_length=4_000)


class AskResponse(BaseModel):
    answer: str
    plan: list[str]
    approval_required: bool
    trace_id: str | None = None
    execution_trace: list[dict[str, Any]] = Field(default_factory=list)


class ReasoningResult(BaseModel):
    confidence: float = Field(ge=0, le=1)
    summary: str
    recommended_action: str
    escalation_required: bool = False


class ToolResult(BaseModel):
    tool_name: str
    success: bool
    data: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
