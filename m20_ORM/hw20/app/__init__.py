from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from m20_ORM.hw20.app.models import Base

engine = create_engine('sqlite:///library.db')
Session = scoped_session(sessionmaker(bind=engine))

def create_app():
    app = Flask(__name__)

    # создаём БД, если нет
    Base.metadata.create_all(engine)

    # импортируем роуты
    from .routes import register_routes
    register_routes(app)

    return app