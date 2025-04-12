# models.py

books = [
    {'id': 1, 'title': '1984', 'author': 'George Orwell', 'views': 0},
    {'id': 2, 'title': 'Animal Farm', 'author': 'George Orwell', 'views': 0},
    {'id': 3, 'title': 'Brave New World', 'author': 'Aldous Huxley', 'views': 0},
]

def get_total_books():
    return len(books)

def get_books_by_author(author_name):
    return [book for book in books if book['author'].lower() == author_name.lower()]

def add_book(title, author):
    new_id = max(book["id"] for book in books) + 1
    books.append({'id': new_id, 'title': title, 'author': author, 'views': 0})

def get_book_by_id(book_id):
    for book in books:
        if book['id'] == book_id:
            book['views'] += 1
            return book
    return None