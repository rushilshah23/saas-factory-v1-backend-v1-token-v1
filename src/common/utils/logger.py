import logging
import sys
import os
from src.common.config import CommonConfig
def get_logger(name: str) -> logging.Logger:
    """
    Production-ready logger for microservices (Kubernetes/Docker).
    Logs to stdout with structured format.
    Log level can be controlled via LOG_LEVEL env var.
    """
    log_level = CommonConfig.LOG_LEVEL

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Avoid duplicate handlers if logger is re-imported
    if logger.hasHandlers():
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
