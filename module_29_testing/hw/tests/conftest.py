import pytest
from datetime import datetime

from module_29_testing.hw.main.app import create_app
from module_29_testing.hw.main import db as _db
from module_29_testing.hw.main.models import Client, Parking, ClientParking


@pytest.fixture
def app():
    _app = create_app()
    _app.config.from_mapping(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite://"
    )

    with _app.app_context():
        _db.create_all()
        client = Client(id=1,
                        name='test_name',
                        surname='test_surname',
                        credit_card='test_credit_card',
                        car_number='test_car_number')
        parking = Parking(id=1,
                          address='test_address',
                          opened=True,
                          count_places=10,
                          count_available_places=5)
        client_parking = ClientParking(id=1,
                                       client_id=1,
                                       parking_id=1,
                                       time_in=datetime.now(),
                                       time_out=datetime.now())

        _db.session.add(client)
        _db.session.add(parking)
        _db.session.add(client_parking)

        yield _app, _db

        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    test_app, test_db = app
    client = test_app.test_client()
    yield client, test_db


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
