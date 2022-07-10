import logging
from pythonjsonlogger import jsonlogger
import sys


def setup_logging():
    logger = logging.getLogger(__name__)

    logHandler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    return logger
