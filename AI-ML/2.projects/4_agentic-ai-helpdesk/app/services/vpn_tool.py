def check_vpn_status(user_id: str) -> dict[str, object]:
    return {
        "user_id": user_id,
        "connected": False,
        "error": "MFA timeout",
        "last_successful_connection": "2026-06-20T16:30:00Z",
    }

