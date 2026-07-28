from uuid import uuid4


def create_ticket(user_id: str, summary: str, priority: str = "normal") -> dict[str, str]:
    ticket_id = f"HD-{uuid4().hex[:8].upper()}"
    return {"ticket_id": ticket_id, "user_id": user_id, "summary": summary, "priority": priority}

