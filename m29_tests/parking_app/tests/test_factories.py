# tests/test_factories.py

from .factories import ClientFactory, ParkingFactory

def test_create_client_with_factory(db):
    client = ClientFactory()
    db.session.add(client)
    db.session.commit()
    assert client.id is not None

def test_create_parking_with_factory(db):
    parking = ParkingFactory()
    db.session.add(parking)
    db.session.commit()
    assert parking.id is not None
    assert parking.count_available_places <= parking.count_places