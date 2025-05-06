from flask import request, jsonify
from datetime import datetime, timedelta

from m20_ORM.hw20.app import Session
from m20_ORM.hw20.app.models import Book, Student, ReceivingBook


def register_routes(app):
    @app.route("/books", methods=["GET"])
    def get_books():
        session = Session()
        books = session.query(Book).all()
        return jsonify([{"id": b.id, "name": b.name} for b in books])

    @app.route("/debtors", methods=["GET"])
    def get_debtors():
        session = Session()
        overdue = datetime.now() - timedelta(days=14)
        debtors = session.query(ReceivingBook).filter(
            ReceivingBook.date_of_return == None,
            ReceivingBook.date_of_issue < overdue
        ).all()
        return jsonify([
            {"student_id": d.student_id, "book_id": d.book_id, "days_with_book": d.count_date_with_book}
            for d in debtors
        ])

    @app.route("/give_book", methods=["POST"])
    def give_book():
        session = Session()
        data = request.json
        new_issue = ReceivingBook(
            book_id=data["book_id"],
            student_id=data["student_id"],
            date_of_issue=datetime.now()
        )
        session.add(new_issue)
        session.commit()
        return jsonify({"status": "book issued"})

    @app.route("/return_book", methods=["POST"])
    def return_book():
        session = Session()
        data = request.json
        record = session.query(ReceivingBook).filter_by(
            book_id=data["book_id"],
            student_id=data["student_id"],
            date_of_return=None
        ).first()
        if not record:
            return jsonify({"error": "No such book found"}), 404
        record.date_of_return = datetime.now()
        session.commit()
        return jsonify({"status": "book returned"})

    @app.route("/search_book", methods=["GET"])
    def search_book():
        session = Session()
        q = request.args.get("q", "")
        books = session.query(Book).filter(Book.name.ilike(f"%{q}%")).all()
        return jsonify([{"id": b.id, "name": b.name} for b in books])