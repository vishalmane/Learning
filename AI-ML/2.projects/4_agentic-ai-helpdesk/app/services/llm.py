import json
from typing import Any

from app.config import get_settings
from app.state import ReasoningResult


class LLMClient:
    def __init__(self) -> None:
        self.settings = get_settings()
        self._chat = None
        provider = self.settings.llm_provider

        if provider == "gemini":
            self._chat = self._build_gemini_chat()
        elif provider == "openai":
            self._chat = self._build_openai_chat()

    def _build_gemini_chat(self):
        api_key = self.settings.google_api_key or self.settings.gemini_api_key
        if not api_key:
            return None
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI

            return ChatGoogleGenerativeAI(
                model=self.settings.gemini_model,
                google_api_key=api_key,
                temperature=0.1,
            )
        except Exception:
            return None

    def _build_openai_chat(self):
        if not self.settings.openai_api_key:
            return None
        try:
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=self.settings.openai_model,
                api_key=self.settings.openai_api_key,
                temperature=0.1,
            )
        except Exception:
            return None

    def plan(self, user_query: str) -> list[str]:
        if self._chat:
            prompt = (
                "Create a concise enterprise helpdesk execution plan as a JSON list of strings. "
                f"Request: {user_query}"
            )
            response = self._chat.invoke(prompt)
            return _parse_string_list(response.content)
        return _fallback_plan(user_query)

    def reason(self, payload: dict[str, Any]) -> ReasoningResult:
        if self._chat:
            prompt = (
                "Return JSON with confidence, summary, recommended_action, escalation_required. "
                f"Context: {json.dumps(payload, default=str)}"
            )
            response = self._chat.invoke(prompt)
            try:
                return ReasoningResult.model_validate_json(response.content)
            except Exception:
                pass
        return _fallback_reasoning(payload)

    def classify_governance(self, user_query: str) -> bool:
        if not self._chat:
            return False
        prompt = (
            "Classify whether this helpdesk request requires human approval for sensitive operations. "
            "Answer only true or false. Request: "
            f"{user_query}"
        )
        response = self._chat.invoke(prompt)
        return str(response.content).strip().lower().startswith("true")


def _parse_string_list(raw: str) -> list[str]:
    raw = _extract_text(raw)
    try:
        value = json.loads(raw)
        if isinstance(value, list) and all(isinstance(item, str) for item in value):
            return value
    except Exception:
        pass
    return [line.strip(" -0123456789.") for line in raw.splitlines() if line.strip()]


def _extract_text(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                parts.append(str(item["text"]))
            else:
                parts.append(str(item))
        return "\n".join(parts).strip()
    return str(content).strip()


def _fallback_plan(user_query: str) -> list[str]:
    query = user_query.lower()
    steps = ["Search support knowledge"]
    if "vpn" in query:
        steps.append("Run VPN diagnostics")
    if any(word in query for word in ("ticket", "escalate", "urgent")):
        steps.append("Create or update support ticket")
    steps.extend(["Determine root cause", "Escalate if needed"])
    return steps


def _fallback_reasoning(payload: dict[str, Any]) -> ReasoningResult:
    query = str(payload.get("user_query", "the request"))
    tool_output = payload.get("tool_output") or []
    vpn_error = None
    for result in tool_output:
        data = result.get("data", {})
        if "error" in data:
            vpn_error = data["error"]
    if vpn_error:
        summary = f"The request appears related to a VPN failure caused by {vpn_error}."
        action = "Ask the user to retry MFA, confirm network connectivity, and escalate if MFA continues to time out."
    else:
        summary = f"Reviewed the request: {query}"
        action = "Apply the relevant knowledge-base steps and create a ticket if the issue remains unresolved."
    return ReasoningResult(
        confidence=0.72,
        summary=summary,
        recommended_action=action,
        escalation_required="urgent" in query.lower(),
    )
