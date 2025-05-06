from sqlalchemy import Column, Integer, Float, String, Boolean, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(100), nullable=False)

    books = relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan",
        lazy="selectin"  # Жадная подгрузка
    )

    def __repr__(self):
        return f'{self.name} {self.surname}'


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    count = Column(Integer, default=1)
    release_date = Column(Date, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    author = relationship(
        "Author",
        back_populates="books",
        lazy="joined"  # Жадная подгрузка через JOIN
    )

    students = relationship(
        'ReceivingBook',
        back_populates='book',
        cascade="all, delete-orphan",
        lazy="selectin"
    )


class Student(Base):
    __tablename__ = 'students'


    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(100), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    average_score = Column(Float, nullable=False)
    scholarship = Column(Boolean, nullable=False)

    books = relationship(
        'ReceivingBook',
        back_populates='student',
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    # Прокси для доступа к книгам напрямую
    borrowed_books = association_proxy('books', 'book')


class ReceivingBook(Base):
    __tablename__ = 'receiving_books'

    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), primary_key=True)

    date_of_issue = Column(DateTime, default=datetime.now)
    date_of_finish = Column(DateTime, nullable=True)

    student = relationship("Student", back_populates="books", lazy="joined")
    book = relationship("Book", back_populates="students", lazy="joined")

# models.py (в самом низу можно добавить это)

from sqlalchemy import event
import re

# Регулярка для проверки телефона
phone_pattern = re.compile(r'^\+7\(9\d{2}\)-\d{3}-\d{2}-\d{2}$')

@event.listens_for(Student, 'before_insert')
def validate_phone(mapper, connect, target):
    if not phone_pattern.match(target.phone):
        raise ValueError(f"Неверный формат телефона: {target.phone}")