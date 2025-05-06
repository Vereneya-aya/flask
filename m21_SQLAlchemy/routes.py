# routes.py
from flask import request, jsonify
from models import Author, Book, Student, ReceivingBook
from database import SessionLocal
from sqlalchemy import func, desc
from sqlalchemy.orm import joinedload


def register_routes(app):
    @app.route('/books_by_author/<int:author_id>', methods=['GET'])
    def get_books_by_author(author_id):
        session = SessionLocal()
        books = session.query(Book).filter(Book.author_id == author_id).all()
        result = [{"id": book.id, "name": book.name, "count": book.count} for book in books]
        session.close()
        return jsonify(result)

    @app.route('/books_student_not_read/<int:student_id>', methods=['GET'])
    def books_student_not_read(student_id):
        session = SessionLocal()
        student = session.query(Student).options(joinedload(Student.books)).filter_by(id=student_id).first()

        if not student:
            session.close()
            return jsonify({"error": "Student not found"}), 404

        # Получаем ID всех книг, которые студент уже брал
        borrowed_book_ids = [rbook.book_id for rbook in student.books]

        # Теперь находим книги авторов, чьи книги студент уже брал, но сами книги еще не брал
        authors_ids = session.query(Book.author_id).filter(Book.id.in_(borrowed_book_ids)).distinct()
        unread_books = session.query(Book).filter(
            Book.author_id.in_(authors_ids),
            ~Book.id.in_(borrowed_book_ids)
        ).all()

        result = [{"id": book.id, "name": book.name} for book in unread_books]
        session.close()
        return jsonify(result)

    @app.route('/average_books_this_month', methods=['GET'])
    def average_books_this_month():
        session = SessionLocal()
        current_month = func.strftime('%Y-%m', func.current_date())
        avg_books = session.query(func.avg(func.count(ReceivingBook.book_id))) \
            .filter(func.strftime('%Y-%m', ReceivingBook.date_of_issue) == current_month) \
            .scalar()
        session.close()
        return jsonify({"average_books": avg_books})

    @app.route('/popular_book', methods=['GET'])
    def popular_book():
        session = SessionLocal()
        popular = session.query(
            Book.name, func.count(ReceivingBook.book_id).label('total')
        ).join(ReceivingBook).join(Student).filter(Student.average_score > 4.0) \
            .group_by(Book.id).order_by(desc('total')).first()

        session.close()
        if popular:
            return jsonify({"book": popular.name})
        else:
            return jsonify({"message": "No popular books found"})

    @app.route('/top_students', methods=['GET'])
    def top_students():
        session = SessionLocal()
        current_year = func.strftime('%Y', func.current_date())
        top_students = session.query(
            Student.name, Student.surname, func.count(ReceivingBook.book_id).label('books_count')
        ).join(ReceivingBook).filter(func.strftime('%Y', ReceivingBook.date_of_issue) == current_year) \
            .group_by(Student.id).order_by(desc('books_count')).limit(10).all()

        result = [{"name": s.name, "surname": s.surname, "books_taken": s.books_count} for s in top_students]
        session.close()
        return jsonify(result)

# routes.py

from flask import request, jsonify
import csv
from io import StringIO
from models import Student
from sqlalchemy.exc import IntegrityError

from flask import request, jsonify
import csv
import io
from models import Student
import re

# Проверка номера телефона
def is_valid_phone(phone):
    pattern = r'^\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}$'
    return re.match(pattern, phone)

def register_routes(app):
    @app.route('/upload_students', methods=['POST'])
    def upload_students():
        session = SessionLocal()
        try:
            if 'file' not in request.files:
                return jsonify({"error": "Нет файла"}), 400

            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "Файл не выбран"}), 400

            # Читаем CSV
            stream = io.StringIO(file.stream.read().decode("utf-8"))
            reader = csv.DictReader(stream, delimiter=';')

            students = []
            for row in reader:
                phone = row['phone']
                if not is_valid_phone(phone):
                    return jsonify({"error": f"Неверный формат телефона: {phone}"}), 400

                student = {
                    'name': row['name'],
                    'surname': row['surname'],
                    'phone': phone,
                    'email': row['email'],
                    'average_score': float(row['average_score']),
                    'scholarship': row['scholarship'].lower() == 'true'
                }
                students.append(student)

            # Массовая вставка
            session.bulk_insert_mappings(Student, students)
            session.commit()

            return jsonify({"message": f"Успешно загружено {len(students)} студентов."}), 200

        except Exception as e:
            session.rollback()
            return jsonify({"error": str(e)}), 500

        finally:
            session.close()