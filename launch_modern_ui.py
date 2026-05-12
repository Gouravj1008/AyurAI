"""Launcher for the React-based Jarvis Ayurveda UI."""

import logging

from run_jarvis_improved import launch_web_ui


def main():
    """Launch the React frontend and API server."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting React-based Jarvis Ayurveda UI")
    launch_web_ui()


if __name__ == "__main__":
    main()
