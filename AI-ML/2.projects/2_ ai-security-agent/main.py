"""Root entrypoint for running the AI Security Agent dashboard."""

import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Start the Streamlit frontend."""
    dashboard_path = Path(__file__).parent / "app" / "frontend" / "dashboard.py"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(dashboard_path),
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
