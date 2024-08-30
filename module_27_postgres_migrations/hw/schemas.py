from marshmallow import Schema, fields, validates, ValidationError, post_load

from models import Coffee, User
from module_27_postgres_migrations.hw import session


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    # has_sale = fields.Bool(required=True)
    surname = fields.Str()
    patronomic = fields.Str()
    address = fields.Dict(required=True)
    coffee_id = fields.Int(required=True)

    @validates('coffee_id')
    def validate_coffee_id(self, coffee_id: int):
        """Валидатор. Проверяет, что coffee_id есть в бд"""
        if not session.query(Coffee).where(Coffee.id == coffee_id).first():
            raise ValidationError(f'Coffee id {coffee_id} нет в бд')

    @validates('address')
    def validate_address(self, address: dict):
        """Валидатор. Проверяет, что в address есть поле country"""
        if not 'country' in address:
            raise ValidationError('Поле "country" должно быть в address')

    @post_load
    def create_user(self, data, **kwargs):
        return User(**data)