from flask_restful import Resource
from flask import request, jsonify
from models import db, Book, Author
from schemas import BookSchema, AuthorSchema

book_schema = BookSchema()
author_schema = AuthorSchema()
books_schema = BookSchema(many=True)
authors_schema = AuthorSchema(many=True)

# Книга
class BookResource(Resource):
    def get(self, id):
        book = Book.query.get_or_404(id)
        return book_schema.dump(book), 200

    def put(self, id):
        book = Book.query.get_or_404(id)
        data = request.get_json()
        errors = book_schema.validate(data)
        if errors:
            return errors, 400
        book.title = data["title"]
        book.year = data.get("year")
        book.author_id = data["author_id"]
        db.session.commit()
        return book_schema.dump(book), 200

    def delete(self, id):
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return '', 204

class BookListResource(Resource):
    def get(self):
        books = Book.query.all()
        return books_schema.dump(books), 200

    def post(self):
        data = request.get_json()
        errors = book_schema.validate(data)
        if errors:
            return errors, 400
        new_book = Book(
            title=data["title"],
            year=data.get("year"),
            author_id=data["author_id"]
        )
        db.session.add(new_book)
        db.session.commit()
        return book_schema.dump(new_book), 201

# Автор
class AuthorResource(Resource):
    def get(self, id):
        author = Author.query.get_or_404(id)
        return {
            "author": author_schema.dump(author),
            "books": books_schema.dump(author.books)
        }, 200

    def delete(self, id):
        author = Author.query.get_or_404(id)
        db.session.delete(author)
        db.session.commit()
        return '', 204

class AuthorListResource(Resource):
    def get(self):
        authors = Author.query.all()
        return authors_schema.dump(authors), 200

    def post(self):
        data = request.get_json()
        errors = author_schema.validate(data)
        if errors:
            return errors, 400
        new_author = Author(
            first_name=data["first_name"],
            last_name=data["last_name"],
            middle_name=data.get("middle_name")
        )
        db.session.add(new_author)
        db.session.commit()
        return author_schema.dump(new_author), 201