import factory
import factory.fuzzy as fuzzy
import random
from string import ascii_letters


from module_29_testing.hw.main import db
from module_29_testing.hw.main.models import Client, Parking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = factory.LazyAttribute(
        lambda x: random.choice((None,
                                 ''.join((random.choice(ascii_letters)
                                          for _ in range(random.randint(1, 50))))))
    )
    car_number = factory.Faker('text', max_nb_chars=50)


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker('address')
    surname = factory.LazyAttribute(lambda x: random.choice([True, False]))
    count_places = factory.LazyAttribute(lambda x: random.randint(0, 100))
    count_available_places = factory.LazyAttribute(lambda x: random.randint(0, x.count_places))
