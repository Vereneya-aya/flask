import subprocess

def count_running_processes():
    # Запуск команды `ps -A` и захват вывода
    result = subprocess.run(['ps', '-A'], capture_output=True, text=True)

    # Подсчёт количества строк (первая строка — заголовок)
    process_count = len(result.stdout.splitlines()) - 1
    print(f"Количество запущенных процессов: {process_count}")

count_running_processes()