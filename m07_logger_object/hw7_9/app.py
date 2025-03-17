import logging.config

from m07_logger_object.hw7_9.logging_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("exampleLogger")

logger.info("This is an info message.")  # Запишется в `app.log`
logger.warning("This is a warning.")  # Не запишется
logger.error("This is an error.")  # Запишется в `app.log`