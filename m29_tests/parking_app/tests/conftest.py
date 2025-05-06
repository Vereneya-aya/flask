# tests/conftest.py

import pytest
from datetime import datetime, timedelta
from app import create_app, db as _db
from app.models import Client, Parking, ClientParking

@pytest.fixture(scope='session')
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def db(app):
    return _db

@pytest.fixture()
def setup_data(db):
    client = Client(name="Anna", surname="Ivanova", credit_card="123456789", car_number="A123AA")
    parking = Parking(address="Main Street", opened=True, count_places=10, count_available_places=9)

    db.session.add(client)
    db.session.add(parking)
    db.session.commit()

    parking_log = ClientParking(client_id=client.id, parking_id=parking.id, time_in=datetime.utcnow())
    db.session.add(parking_log)
    db.session.commit()

    return {
        "client": client,
        "parking": parking,
        "parking_log": parking_log
    }