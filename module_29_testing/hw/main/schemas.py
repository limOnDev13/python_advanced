from marshmallow import Schema, fields, post_load, validates_schema, validates
from marshmallow.exceptions import ValidationError

from .models import Client, Parking, ClientParking
from . import db


class ClientSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    surname = fields.Str(required=True)
    credit_card = fields.Str()
    car_number = fields.Str()

    @post_load
    def create_client(self, data, **kwargs):
        return Client(**data)


class ParkingSchema(Schema):
    id = fields.Int(dump_only=True)
    address = fields.Str(required=True)
    opened = fields.Boolean()
    count_places = fields.Int(required=True)
    count_available_places = fields.Int(required=True)

    @validates_schema(skip_on_field_errors=False)
    def validate_count_places(self, data, **kwargs):
        if data['count_places'] < data['count_available_places']:
            raise ValidationError(f'Количество свободных мест должно быть не больше количества всех мест на парковке')

    @post_load
    def create_parking(self, data, **kwargs):
        return Parking(**data)


class ClientParkingSchema(Schema):
    id = fields.Int(dump_only=True)
    client_id = fields.Int(required=True)
    parking_id = fields.Int(required=True)
    time_in = fields.DateTime()
    time_out = fields.DateTime()

    @post_load
    def create_client_parking(self, data, **kwargs):
        return ClientParking(**data)

    @validates('parking_id')
    def validate_parking_is_opened(self, parking_id: int):
        """Валидатор проверяет, что парковка существует, она открыта, и на ней есть свободные места"""
        result = db.session.query(Parking.opened, Parking.count_available_places) \
            .where(Parking.id == parking_id).first()
        if not result:
            raise ValidationError('Парковки нет в бд')
        opened, available_places = result
        if not opened:
            raise ValidationError('Парковка закрыта')
        if not available_places:
            raise ValidationError('На парковке не осталось свободных мест')

    @validates('client_id')
    def validate_client_exists(self, client_id: int):
        """Валидатор проверяет, что клиент есть в базе"""
        if not db.session.query(Client).where(Client.id == client_id).first():
            raise ValidationError('Такого клиента нет в бд')

    @validates_schema
    def validate_unique_pair_of_client_and_parking_ids(self, data, **kwargs):
        """Валидатор проверяет, что полученная пара client и parking ids уникальна и ее нет в бд
        (как указано в схеме таблицы в задании)"""
        if db.session.query(ClientParking)\
                .where(ClientParking.client_id == data['client_id'] and
                       ClientParking.parking_id == data['parking_id']).first():
            raise ValidationError("Пара client_id и parking_id уже есть в бд")


class DeleteClientParkingSchema(ClientParkingSchema):
    @validates_schema
    def validate_unique_pair_of_client_and_parking_ids(self, data, **kwargs):
        """Валидатор проверяет, что полученная пара client и parking ids есть в бд и нет времени выезда"""
        client_parking = db.session.query(ClientParking)\
            .where(ClientParking.client_id == data['client_id'] and
                   ClientParking.parking_id == data['parking_id']).first()
        if not client_parking or client_parking.time_out is not None:
            raise ValidationError("Пары client_id и parking_id нет в бд либо клиент уже отъехал")

    @post_load
    def create_client_parking(self, data, **kwargs):
        return db.session.query(ClientParking).where(
            ClientParking.client_id == data['client_id'] and
            ClientParking.parking_id == data['parking_id']).first()
