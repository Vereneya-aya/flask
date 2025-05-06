from flask import jsonify, request
from . import create_app, db
from .models import User, Coffee
import requests
import random

app = create_app()

@app.before_first_request
def init_data():
    if not Coffee.query.first():
        for _ in range(10):
            coffee_data = requests.get('https://random-data-api.com/api/coffee/random_coffee').json()
            coffee = Coffee(
                title=coffee_data['blend_name'],
                origin=coffee_data['origin'],
                intensifier=coffee_data['intensifier'],
                notes=coffee_data.get('notes', [])
            )
            db.session.add(coffee)
        db.session.commit()

    if not User.query.first():
        coffees = Coffee.query.all()
        for _ in range(10):
            user_data = requests.get('https://random-data-api.com/api/address/random_address').json()
            user = User(
                name=user_data['first_name'],
                has_sale=random.choice([True, False]),
                address=user_data,
                coffee_id=random.choice(coffees).id
            )
            db.session.add(user)
        db.session.commit()

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    user = User(
        name=data['name'],
        has_sale=data.get('has_sale', False),
        address=data['address'],
        coffee_id=data['coffee_id']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"user": {
        "name": user.name,
        "coffee_id": user.coffee_id
    }})

@app.route('/coffee_search')
def coffee_search():
    query = request.args.get('q')
    result = Coffee.query.filter(Coffee.title.ilike(f'%{query}%')).all()
    return jsonify([c.title for c in result])

@app.route('/unique_notes')
def unique_notes():
    coffees = Coffee.query.all()
    notes = set()
    for coffee in coffees:
        if coffee.notes:
            notes.update(coffee.notes)
    return jsonify(list(notes))

@app.route('/users_by_country')
def users_by_country():
    country = request.args.get('country')
    result = User.query.filter(User.address['country'].astext == country).all()
    return jsonify([u.name for u in result])