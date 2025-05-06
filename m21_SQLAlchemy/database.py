# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///lesson3.db', echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# маленькая подсказка: SessionLocal() открывает тебе сессию