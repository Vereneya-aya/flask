from flask_restful import Resource
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, use_kwargs, doc
from schemas import BookSchema

BOOKS = []

class BookListResource(MethodResource, Resource):

    @doc(description="Получить список книг", tags=["Books"])
    @marshal_with(BookSchema(many=True))
    def get(self):
        return BOOKS, 200

    @doc(description="Добавить книгу", tags=["Books"])
    @use_kwargs(BookSchema)
    @marshal_with(BookSchema)
    def post(self, **kwargs):
        BOOKS.append(kwargs)
        return kwargs, 201