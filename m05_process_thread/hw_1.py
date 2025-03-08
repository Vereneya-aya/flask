import subprocess
import os
import signal
import time


def find_process_on_port(port):
    """Находит PID процесса, занимающего указанный порт"""
    try:
        result = subprocess.Popen(["lsof", "-i", f":{port}"], stdout=subprocess.PIPE, text=True)
        stdout, _ = result.communicate()

        lines = stdout.splitlines()
        if len(lines) <= 1:  # Если строка одна, значит процесс не найден
            return None

        # Вторая строка содержит PID
        pid = int(lines[1].split()[1])
        return pid
    except Exception as e:
        print(f"Ошибка при поиске процесса: {e}")
        return None


def free_port(port):
    """Завершает процесс, занимающий порт"""
    pid = find_process_on_port(port)
    if pid:
        print(f"Найден процесс {pid}, занимающий порт {port}. Завершаем...")
        # os.kill(pid, signal.SIGTERM)
        os.kill(pid, signal.SIGKILL)  # Более жёсткое завершение
        time.sleep(1)  # Ждём, чтобы процесс полностью завершился
        print(f"Порт {port} освобождён.")
    else:
        print(f"Порт {port} свободен.")


def start_server(port):
    """Пытается запустить сервер на указанном порту"""
    print(f"Пытаемся запустить сервер на порту {port}...")

    # Освобождаем порт, если он занят
    free_port(port)

    # Пробуем запустить сервер (заглушка для примера)
    process = subprocess.Popen(["python", "-m", "http.server", str(port)])
    print(f"Сервер запущен на порту {port}, PID: {process.pid}")


if __name__ == "__main__":
    start_server(8000)  # Пробуем запустить сервер на 5000 порту