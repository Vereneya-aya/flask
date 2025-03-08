import sys
import traceback


class Redirect:
    def __init__(self, *, stdout=None, stderr=None):
        self.new_stdout = stdout
        self.new_stderr = stderr
        self.old_stdout = None
        self.old_stderr = None

    def __enter__(self):
        if self.new_stdout:
            self.old_stdout = sys.stdout
            sys.stdout = self.new_stdout
        if self.new_stderr:
            self.old_stderr = sys.stderr
            sys.stderr = self.new_stderr

    def __exit__(self, exc_type, exc_value, exc_tb):
        # Восстанавливаем потоки перед обработкой исключения
        if self.old_stdout:
            sys.stdout = self.old_stdout
        if self.old_stderr:
            sys.stderr = self.old_stderr

        # Если произошло исключение, и stderr был перенаправлен, записываем его в stderr
        if exc_type and self.new_stderr:
            self.new_stderr.write(traceback.format_exc())  # Записываем полную ошибку в stderr
            return True  # Подавляем исключение (иначе оно снова поднимется)

        return False  # Если False, исключение прокидывается дальше

with open("stdout.txt", "w") as stdout_file:
    with Redirect(stdout=stdout_file):
        print("Hello stdout.txt")  # Запишется в файл

print("Hello terminal")  # Выведется в терминал

with open("stderr.txt", "w") as stderr_file:
    with Redirect(stderr=stderr_file):
        raise Exception("Hello stderr.txt")  # Ошибка будет записана в файл

with open("stdout.txt", "w") as stdout_file, open("stderr.txt", "w") as stderr_file:
    with Redirect(stdout=stdout_file, stderr=stderr_file):
        print("Hello stdout.txt")
        raise Exception("Hello stderr.txt")