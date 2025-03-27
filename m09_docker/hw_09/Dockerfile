# 1. Используем базовый образ Python
FROM python:3.9

# 2. Устанавливаем рабочую директорию
WORKDIR /app

# 3. Копируем файлы проекта
COPY requirements.txt .
COPY app.py .

# 4. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 5. Открываем порт
EXPOSE 5000

# 6. Определяем точку входа
ENTRYPOINT ["python", "app.py"]