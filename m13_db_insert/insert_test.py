import sqlite3

conn = sqlite3.connect("practise.db")
cur = conn.cursor()

print("Содержимое table_warehouse:")
for row in cur.execute("SELECT * FROM table_warehouse"):
    print(row)

print("\nСодержимое book_list:")
for row in cur.execute("SELECT * FROM book_list"):
    print(row)

conn.close()