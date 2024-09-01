from . import db
from typing import Dict, Any


class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))

    client_parking_association = db.relationship(
        'ClientParking', back_populates='client', cascade='all, delete-orphan'
    )
    list_parking = db.relationship('Parking', secondary='client_parking', back_populates='clients')

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}



class Parking(db.Model):
    __tablemname__ = 'parking'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    client_parking_association = db.relationship(
        'ClientParking', back_populates='parking', cascade='all, delete-orphan'
    )
    clients = db.relationship('Client', secondary='client_parking', back_populates='list_parking')

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class ClientParking(db.Model):
    __tablename__ = 'client_parking'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'))
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)
    db.UniqueConstraint('client_id', 'parking_id', name='unique_client_parking')

    client = db.relationship('Client', back_populates='client_parking_association')
    parking = db.relationship('Parking', back_populates='client_parking_association', lazy='joined')

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}
