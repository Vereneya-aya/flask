class BlockErrors:
    def __init__(self, error_types):
        self.error_types = tuple(error_types)  # Преобразуем множество в кортеж

    def __enter__(self):
        pass  # Вход в блок, ничего не делаем

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type and issubclass(exc_type, self.error_types):
            return True  # Ошибку подавляем (игнорируем)
        return False  # Ошибку не подавляем (она прокидывается выше)

# err_types = {ZeroDivisionError}
# with BlockErrors(err_types):
#     a = 1 / 0
# print("Выполнено без ошибок")

# err_types = {ZeroDivisionError}
#
# with BlockErrors(err_types):
#     a = 1 / "0"  # TypeError
#
# print("Выполнено без ошибок")

# outer_err_types = {TypeError}
# with BlockErrors(outer_err_types):
#     inner_err_types = {ZeroDivisionError}
#     with BlockErrors(inner_err_types):
#         a = 1 / "0"  # TypeError не игнорируется внутренним блоком
#     print("Внутренний блок: выполнено без ошибок")
# print("Внешний блок: выполнено без ошибок")

err_types = {Exception}
with BlockErrors(err_types):
    a = 1 / "0"  # TypeError тоже игнорируется
print("Выполнено без ошибок")