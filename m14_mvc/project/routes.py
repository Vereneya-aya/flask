from flask import Blueprint, request, render_template, redirect
from models import books, get_books_by_author, get_total_books, add_book, get_book_by_id
from forms import BookForm  # импортируй форму

book_routes = Blueprint('book_routes', __name__)


@book_routes.route('/books')
def show_books():
    total = get_total_books()
    return render_template("index.html", books=books, total=total)

@book_routes.route('/search')
def search_books():
    author = request.args.get('author', '')
    results = get_books_by_author(author)
    return render_template('author_books.html', books=results, author=author)

@book_routes.route("/books/form", methods=["GET", "POST"])
def add_book_form():
    form = BookForm()
    if form.validate_on_submit():
        add_book(form.title.data, form.author.data)
        return redirect("/books")
    return render_template("add_book.html", form=form)

@book_routes.route("/books/<int:book_id>")
def book_detail(book_id):
    book = get_book_by_id(book_id)
    if book:
        return render_template("book_detail.html", book=book)
    return "<p>Book not found</p>"