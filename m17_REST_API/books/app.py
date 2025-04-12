# app.py
from flask import Flask
from flask_restful import Api, Resource
import models

app = Flask(__name__)
api = Api(app)

class AuthorList(Resource):
    def get(self):
        return models.get_all_authors()

class AuthorResource(Resource):
    def get(self, author_id):
        author = models.get_author(author_id)
        if author:
            return author
        return {"error": "Author not found"}, 404

class AuthorBooks(Resource):
    def get(self, author_id):
        return models.get_books_by_author(author_id)

class AuthorBookResource(Resource):
    def get(self, author_id, book_id):
        book = models.get_book(author_id, book_id)
        if book:
            return book
        return {"error": "Book not found"}, 404

api.add_resource(AuthorList, "/authors")
api.add_resource(AuthorResource, "/authors/<int:author_id>")
api.add_resource(AuthorBooks, "/authors/<int:author_id>/books")
api.add_resource(AuthorBookResource, "/authors/<int:author_id>/books/<int:book_id>")

# app.py
from flask import request
from flask_restful import Resource

from m17_REST_API.books import models
from schemas import BookSchema

book_schema = BookSchema()

class AuthorBooks(Resource):
    def get(self, author_id):
        return models.get_books_by_author(author_id)

    def post(self, author_id):
        json_data = request.get_json()
        # Валидация через схему
        errors = book_schema.validate(json_data)
        if errors:
            return {"errors": errors}, 400

        title = json_data["title"]
        new_book = models.add_book(author_id, title)
        return book_schema.dump(new_book), 201

if __name__ == "__main__":
    app.run(debug=True)

