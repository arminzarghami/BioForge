"""Logging configuration for BioForge."""

from __future__ import annotations

import logging
from pathlib import Path


LOGGER_NAME = "bioforge"


def setup_logging(output_directory: Path) -> logging.Logger:
    """Return the project logger writing UTF-8 messages in append mode."""
    output_directory.mkdir(parents=True, exist_ok=True)
    log_path = output_directory / "bioforge.log"

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # Tests and repeated calls in the same interpreter must not duplicate lines.
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

    handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    logger.addHandler(handler)
    return logger
