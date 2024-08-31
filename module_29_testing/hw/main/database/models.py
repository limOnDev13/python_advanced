from module_29_testing.hw.main import db


class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))

    client_parking_associations = db.relationship(
        'ClientParking', back_populates='client', cascade='all, delete-orphan'
    )
    list_parking = db.association_proxy('client_parking_associations', 'parking')


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
    clients = db.association_proxy('client_parking_association', 'client')



class ClientParking(db.Model):
    __tablename__ = 'client_parking'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'))
    time_in = db.Column(db.DateTime)
    timr_out = db.Column(db.DateTime)
    db.UniqueConstraint('client_id', 'parking_id', name='unique_client_parking')

    client = db.relationship('Client', back_populates='client_parking_association')
    parking = db.relationship('Parking', back_populates='client_parking_association')
