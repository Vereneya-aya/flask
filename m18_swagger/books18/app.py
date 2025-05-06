from flask import Flask
import flask_restful
from models import db
from resources import BookResource, BookListResource, AuthorResource, AuthorListResource
import os
from flask import Flask
from flasgger import Swagger

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'books.db')}"
app.config['SWAGGER'] = {
    'title': 'Library API',
    'uiversion': 3
}

db.init_app(app)
api = flask_restful.Api(app)
swagger = Swagger(app)

with app.app_context():
    db.create_all()

api.add_resource(BookListResource, '/api/books/')
api.add_resource(BookResource, '/api/books/<int:id>')
api.add_resource(AuthorListResource, '/api/authors/')
api.add_resource(AuthorResource, '/api/authors/<int:id>')

@app.route('/')
def index():
    return 'Welcome to Library API!'

if __name__ == '__main__':
    app.run(debug=True)