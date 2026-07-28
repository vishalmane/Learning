def send_notification(user_id: str, message: str) -> dict[str, object]:
    return {"user_id": user_id, "delivered": True, "message": message}

