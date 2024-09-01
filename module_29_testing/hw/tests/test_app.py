import pytest

from module_29_testing.hw.main.models import Parking


@pytest.mark.parametrize('route', ['/clients', '/clients/1', '/parkings', '/client_parkings'])
def test_get_requests(client, route):
    """Тест проверяет, что все get запросы возвращают 200"""
    test_app, _ = client
    rv = test_app.get(route)
    assert rv.status_code == 200


def test_create_client(client):
    """Тест для проверки создания клиента. Ендпоинт должен вернуть 201 код и созданного клиента"""
    test_client = dict(name='test_name_2',
                       surname='test_surname_2',
                       credit_card='test_credit_card_2',
                       car_number='test_car_number_2')
    test_app, _ = client
    rv = test_app.post('/clients', json=test_client)
    assert rv.status_code == 201
    result = rv.json['new_client']
    result.pop('id')
    assert result == test_client


def test_create_parking(client):
    """Тест для проверки создания парковки. Ендпоинт должен вернуть 201 код и созданную парковку"""
    test_parking = dict(
        address='test_address_2',
        opened=True,
        count_places=10,
        count_available_places=5)
    test_app, _ = client
    rv = test_app.post('/parkings', json=test_parking)
    assert rv.status_code == 201
    result = rv.json['parking']
    result.pop('id')
    assert result == test_parking


@pytest.mark.parking
def test_check_in_to_parking_lot(client):
    """Тест для проверки заезда на парковку. Ендпоинт должен вернуть 201 код и инфу о лоте.
    Также поле time_in не должно быть None, а поле time_out должен быть None. Количество свободных мест
    уменьшается на одно"""
    test_app, test_db = client
    # Добавим еще одного пользователя
    test_client = dict(name='test_name_2',
                       surname='test_surname_2',
                       credit_card='test_credit_card_2',
                       car_number='test_car_number_2')
    test_app.post('/clients', json=test_client)
    # Теперь добавим лот
    q_count_available_places = test_db.session.query(Parking.count_available_places)
    before_count: int = q_count_available_places.scalar()

    test_client_parking = dict(
        client_id=2,
        parking_id=1
    )
    rv = test_app.post('/client_parkings', json=test_client_parking)
    assert rv.status_code == 201

    result = rv.json['client_parking']

    assert result['client_id'] == test_client_parking['client_id']
    assert result['parking_id'] == test_client_parking['parking_id']
    assert result['time_in'] is not None
    assert result['time_out'] is None
    assert before_count - 1 == q_count_available_places.scalar()


@pytest.mark.parking
def test_check_out_to_parking_lot(client):
    """Тест для проверки выезда с парковки. Ендпоинт должен вернуть 202 код и инфу о лоте.
    Также поле time_in и time_out не должны быть None, причем time_out > time_in.
    Количество свободных мест увеличивается на одно"""
    test_app, test_db = client
    # Добавим еще одного пользователя
    test_client = dict(name='test_name_2',
                       surname='test_surname_2',
                       credit_card='test_credit_card_2',
                       car_number='test_car_number_2')
    test_app.post('/clients', json=test_client)

    # Теперь добавим лот
    test_client_parking = dict(
        client_id=2,
        parking_id=1
    )
    test_app.post('/client_parkings', json=test_client_parking)

    q_count_available_places = test_db.session.query(Parking.count_available_places)
    before_count: int = q_count_available_places.scalar()

    # Теперь закроем этот лот
    rv = test_app.delete('/client_parkings', json=test_client_parking)

    assert rv.status_code == 202

    result = rv.json['client_parking']

    assert result['client_id'] == test_client_parking['client_id']
    assert result['parking_id'] == test_client_parking['parking_id']
    assert result['time_in'] is not None
    assert result['time_out'] is not None
    assert result['time_out'] >= result['time_in']
    assert before_count + 1 == q_count_available_places.scalar()
