import subprocess
import time

def count_running_processes():
    # Используем Popen вместо run
    process = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE, text=True)
    stdout, _ = process.communicate()  # Захватываем вывод

    # Подсчёт количества процессов
    process_count = len(stdout.splitlines()) - 1
    print(f"Количество запущенных процессов: {process_count}")

def run_parallel_processes():
    processes = []
    for _ in range(10):
        proc = subprocess.Popen("sleep 15 && echo 'My mission is done here!'", shell=True)
        processes.append(proc)

    # Ждём завершения всех процессов
    for proc in processes:
        proc.wait()

    print("Все 10 процессов завершены.")

def check_sleep_exit():
    proc = subprocess.Popen("sleep 10 && exit 1", shell=True)

    try:
        proc.wait(timeout=9)
        print("Процесс ещё выполняется через 9 секунд.")
    except subprocess.TimeoutExpired:
        print("Процесс не завершился за 9 секунд, продолжаем ждать...")

    # Дождаться завершения и проверить код возврата
    proc.wait()
    print(f"Код возврата процесса: {proc.returncode}")

# Вызываем функции
count_running_processes()
run_parallel_processes()
check_sleep_exit()