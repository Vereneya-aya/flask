## 1. Берем базовый образ с Python
#FROM python:3.9
#
## 3. Копируем файлы проекта
#COPY requirements.txt .
#COPY app.py .
#
## 4. Устанавливаем зависимости
#RUN pip install --no-cache-dir -r requirements.txt
#
## 5. Определяем переменные окружения (по умолчанию)
#ENV SERVICE_NAME="MyService"
#ENV ADMIN_NAME="DefaultAdmin"
#
## 6. Открываем порт
#EXPOSE 5000
#
## 7. Определяем точку входа
#ENTRYPOINT ["python", "app.py"]

FROM python:3.9
WORKDIR /app
COPY --from=base /app /app
COPY app.py .
EXPOSE 5000
ENTRYPOINT ["python", "app.py"]