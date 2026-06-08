"""Alert delivery service placeholder."""


class AlertService:
    """Sends alerts to configured notification channels."""

    def send_alert(self, message: str) -> dict[str, str]:
        """Send a security alert."""
        return {
            "status": "queued",
            "message": message,
        }
