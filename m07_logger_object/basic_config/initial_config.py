import logging.config
from logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger("sub_1")
logger.info("Привет из sub_1!")