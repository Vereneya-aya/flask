from flask import Flask
from routes import book_routes

app = Flask(__name__)
app.register_blueprint(book_routes)
app.config['SECRET_KEY'] = 'key'

if __name__ == '__main__':
    app.run(debug=True)


# http://127.0.0.1:5000/search?author=George Orwell