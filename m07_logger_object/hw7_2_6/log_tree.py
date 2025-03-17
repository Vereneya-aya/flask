import logging
import logging_tree
import logger_config  # Импортируем конфигурацию логирования


def save_logging_tree():
    """Выводит и сохраняет структуру логгеров в logging_tree.txt."""

    # Настроим логирование перед получением дерева логгеров
    logger_config.configure_logging()

    tree_output = logging_tree.format.build_description()  # Получаем строку с деревом логгеров
    with open("logging_tree.txt", "w", encoding="utf-8") as file:
        file.write(tree_output)

    print("Дерево логгеров сохранено в logging_tree.txt")


if __name__ == "__main__":
    save_logging_tree()