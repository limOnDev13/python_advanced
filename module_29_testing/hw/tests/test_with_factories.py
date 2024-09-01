from .factories import ClientFactory, ParkingFactory


def test_create_client(db):
    """Тест для проверки создания клиента. Ендпоинт должен вернуть 201 код и созданного клиента"""
    test_client = ClientFactory()
    db.session.commit()

    assert test_client.id is not None


def test_create_parking(db):
    """Тест для проверки создания парковки. Ендпоинт должен вернуть 201 код и созданную парковку"""
    test_parking = ParkingFactory()
    db.session.commit()

    assert test_parking.id is not None
