import logging
import utils
import logger_config

logger = logging.getLogger(__name__)

def main():
    logger.info("Запуск калькулятора")

    x = 10
    y = 5

    result_add = utils.add(x, y)
    result_sub = utils.subtract(x, y)
    result_mul = utils.multiply(x, y)
    result_div = utils.divide(x, y)

    logger.debug(f"Результаты: {result_add=}, {result_sub=}, {result_mul=}, {result_div=}")

if __name__ == "__main__":
    main()