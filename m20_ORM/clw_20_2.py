# from requests import Session
#
# if __name__=='__main__':
#     from sqlalchemy import create_engine, text
#
#     engine = create_engine("sqlite:///python.db")
#     with engine.connect() as connection:
#         sql = text(
#             """
#             CREATE TABLE IF not EXISTS users (
#             id integer PRIMARY KEY,
#             name text NOT NULL)"""
#         )
#
#         connection.execute(sql)
#
#         insert_sql = text("""INSERT INTO users(name) values('Nikita')""")
#         connection.execute(insert_sql)
#
#         filter_query = text("SELECT * FROM users WHERE id=:user_id")
#         cursor = connection.execute(filter_query, dict(user_id=1))
#
#         result = cursor.fetchone()
#         print(result)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///python.db")

Session = sessionmaker(bind=engine)
session = Session