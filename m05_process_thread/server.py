# server.py
import subprocess


def run_program_in_stderr():
    # Запуск TestProgram.py через subprocess
    result = subprocess.run(
        ['python', 'test_program.py'],  # Список с командой и аргументами
        stderr=subprocess.PIPE,  # Перенаправляем вывод в стандартный поток ошибок
        stdout=subprocess.PIPE,  # Перенаправляем стандартный вывод
        text=True  # Вывод в текстовом формате (а не в байтах)
    )

    # Выводим отдельно stdout и stderr
    print("Вывод в stdout:")
    print(result.stdout)  # Здесь будет текст из print() без file=sys.stderr

    print("\nВывод в stderr:")
    print(result.stderr)  # Здесь будет текст из print(..., file=sys.stderr)


# Запускаем функцию
run_program_in_stderr()