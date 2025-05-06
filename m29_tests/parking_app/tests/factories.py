# tests/factories.py

import factory
from factory.fuzzy import FuzzyInteger, FuzzyText, FuzzyChoice
from faker import Faker
from app.models import Client, Parking

fake = Faker()

class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session_persistence = 'flush'

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = factory.Faker('credit_card_number')
    car_number = FuzzyText(length=6, prefix='A')

class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session_persistence = 'flush'

    address = fake.address()
    opened = FuzzyChoice([True, False])
    count_places = FuzzyInteger(5, 20)
    count_available_places = factory.LazyAttribute(lambda o: o.count_places)