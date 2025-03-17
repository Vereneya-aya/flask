import logging
import custom_file_handler  # подключает твой конфиг с кастомным хэндлером

logger = logging.getLogger("sub_1")
logger.debug("Debug message with extra", extra={"very": "much"})
logger.info("Info message without extra", extra={"very": "some default value"})