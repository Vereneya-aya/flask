# app.py
from flask import Flask
from models import Base
from database import engine
from routes import register_routes

app = Flask(__name__)

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Регистрация всех роутов
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)