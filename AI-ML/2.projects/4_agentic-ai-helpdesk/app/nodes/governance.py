import re

from app.config import get_settings
from app.security import detect_pii, looks_like_prompt_injection
from app.services.llm import LLMClient
from app.state import HelpdeskState
from app.nodes.tracing import append_trace

SENSITIVE_PATTERNS = [
    re.compile(r"\bpassword\s+reset\b", re.I),
    re.compile(r"\bdelete\s+(?:my\s+)?account\b", re.I),
    re.compile(r"\bdisable\s+(?:my\s+)?account\b", re.I),
    re.compile(r"\b(access\s+removal|remove\s+access|revoke\s+access)\b", re.I),
    re.compile(r"\bsensitive\s+operation\b", re.I),
]


def governance_node(state: HelpdeskState) -> HelpdeskState:
    query = state["user_query"]
    rule_hit = any(pattern.search(query) for pattern in SENSITIVE_PATTERNS)
    llm_hit = LLMClient().classify_governance(query) if get_settings().enable_llm_governance else False
    governance = {
        "rule_hit": rule_hit,
        "llm_hit": llm_hit,
        "pii_detected": detect_pii(query),
        "prompt_injection_detected": looks_like_prompt_injection(query),
    }
    metadata = {
        **state.get("metadata", {}),
        "governance": governance,
    }
    approval_required = bool(rule_hit or llm_hit)
    traced_state = {**state, "metadata": metadata}
    metadata = append_trace(
        traced_state,
        "governance",
        {"user_query": query, "plan": state.get("plan", [])},
        "Applies deterministic sensitive-operation rules and optional LLM classification. Rule hits always take precedence.",
        {
            "approval_required": approval_required,
            "route": "human_review" if approval_required else "retriever",
            "checks": governance,
        },
    )
    return {**state, "approval_required": approval_required, "metadata": metadata}


def route_after_governance(state: HelpdeskState) -> str:
    return "human_review" if state.get("approval_required") else "retriever"
