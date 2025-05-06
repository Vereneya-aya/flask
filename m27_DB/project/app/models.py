from . import db
from sqlalchemy.dialects.postgresql import ARRAY, JSON

class Coffee(db.Model):
    __tablename__ = 'coffee'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    origin = db.Column(db.String(200))
    intensifier = db.Column(db.String(100))
    notes = db.Column(ARRAY(db.String))

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    has_sale = db.Column(db.Boolean)
    address = db.Column(JSON)
    coffee_id = db.Column(db.Integer, db.ForeignKey('coffee.id'))