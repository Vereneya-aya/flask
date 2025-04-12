import subprocess


def process_count(username: str) -> int:
    """
    Возвращает количество процессов, запущенных пользователем username.
    """
    try:
        result = subprocess.run(["pgrep", "-u", username], capture_output=True, text=True)
        return len(result.stdout.strip().split("\n")) if result.stdout else 0
    except Exception as e:
        print(f"Ошибка: {e}")
        return 0


def total_memory_usage(root_pid: int) -> float:
    """
    Возвращает суммарное потребление памяти всеми процессами, порождёнными root_pid.
    """
    try:
        result = subprocess.run(["ps", "-o", "%mem", "--ppid", str(root_pid)], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")[1:]  # Пропускаем заголовок
        return sum(float(line) for line in lines if line)
    except Exception as e:
        print(f"Ошибка: {e}")
        return 0.0


if __name__ == "__main__":
    username = "your_username_here"  # Замените на нужное имя пользователя
    print(f"Количество процессов у {username}: {process_count(username)}")

    root_pid = 1  # Например, PID системного процесса
    print(f"Суммарное использование памяти процессами с корнем {root_pid}: {total_memory_usage(root_pid):.2f}%")
