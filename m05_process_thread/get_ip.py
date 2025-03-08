import subprocess
import shlex
import json


def get_ip_address():
    # Команда в виде строки
    command = 'curl -i -H "Accept: application/json" -X GET https://api.ipify.org?format=json'

    # Токенизация команды с помощью shlex
    args = shlex.split(command)

    # Запуск команды и получение вывода
    result = subprocess.run(args, capture_output=True, text=True)

    # Разбор вывода. Ответ содержит заголовки, ищем строку с JSON
    for line in result.stdout.split('\n'):
        if line.startswith('{'):
            data = json.loads(line)
            return data.get('ip')

print(get_ip_address())