import logging
import os
import sys


def _format(level):
    if level == logging.INFO:
        return "%(asctime)s | %(levelname)s - %(name)s - %(message)s"
    if level == logging.WARNING:
        return "%(asctime)s | %(levelname)s - %(name)s:%(lineno)d - %(message)s"
    else:
        return "%(asctime)s | %(levelname)s - %(process)d:%(threadName)s - %(name)s:%(lineno)d - %(message)s"


def get_logger(name: str):
    log_level = logging.getLevelName(os.getenv("LOG_LEVEL", logging.WARNING))
    logging.basicConfig(
        stream=sys.stdout,
        level=log_level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s | %(levelname)s - %(process)d:%(threadName)s - %(name)s:%(lineno)d - %(message)s",
    )

    return logging.getLogger(name)
