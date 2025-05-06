FROM python:3.8

# Устанавливаем нужные пакеты
RUN apt-get update && apt-get install -y nginx python3-dev supervisor \
    && rm -rf /var/lib/apt/lists/*

# Создаем директорию для приложения
WORKDIR /app

# Копируем всё внутрь контейнера
COPY requirements.txt /app/requirements.txt
COPY src/ /app/src/
COPY nginx.conf /etc/nginx/nginx.conf
COPY uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY supervisord.ini /etc/supervisor/conf.d/supervisord.ini

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Открываем порт 80
EXPOSE 80

# Запускаем Supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.ini"]