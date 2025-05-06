
docker-compose up -d
docker exec -it pg_container psql -U postgres
\c skillbox_db

CREATE TABLE test_psql_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

\dt

alembic init migrations
alembic.ini:
sqlalchemy.url = postgresql+psycopg2://postgres:postgres@db:5432/skillbox_db

migrations/env.py
from app.models import db
target_metadata = db.metadata

alembic revision --autogenerate -m "init"
migrations/versions/.
alembic upgrade head

models.py:
# has_sale = db.Column(db.Boolean)  ← удалить
alembic revision --autogenerate -m "remove has_sale"
alembic upgrade head

alembic history
alembic downgrade -1

models.py:
surname = db.Column(db.String(50))

alembic revision --autogenerate -m "add surname"
alembic upgrade head

patronymic = db.Column(db.String(50))
alembic revision --autogenerate -m "add patronymic"
down_revision = 'xxxxxx'  ← замени на ревизию из "remove has_sale"

alembic upgrade head

У тебя будет конфликт миграций — Alembic предупредит. Чтобы решить:
	•	Объедини изменения в одной миграции;
	•	Или укажи merge heads.