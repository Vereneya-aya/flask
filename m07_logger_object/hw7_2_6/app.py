import logging
import m07_logger_object.hw7_1.utils
import logger_config

# Настроить логирование
logger_config.configure_logging()

logger = logging.getLogger(__name__)

def main():
    logger.info("Запуск калькулятора")

    x = 10
    y = 0

    from m07_logger_object.hw7_1 import utils
    result_add = utils.add(x, y)
    result_sub = utils.subtract(x, y)
    result_mul = utils.multiply(x, y)
    result_div = utils.divide(x, y)

    logger.debug(f"Результаты: {result_add=}, {result_sub=}, {result_mul=}, {result_div=}")

if __name__ == "__main__":
    main()