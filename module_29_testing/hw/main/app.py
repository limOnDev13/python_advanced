from flask import Flask, jsonify, request
from marshmallow.exceptions import ValidationError
from typing import List, Optional
from datetime import datetime

from . import db
from .schemas import ClientSchema, ParkingSchema, ClientParkingSchema, DeleteClientParkingSchema
from .models import Client, Parking, ClientParking


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:///prod.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    db.init_app(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route('/clients', methods=['GET'])
    def get_clients():
        """Эндпоинт возвращает список всех клиентов"""
        clients: List[Client] = db.session.query(Client).all()
        return jsonify(clients=[client.to_json() for client in clients]), 200

    @app.route('/clients/<int:client_id>', methods=['GET'])
    def get_client_by_id(client_id: int):
        """Эндпоинт возвращает клиента по его id"""
        client: Optional[Client] = db.session.query(Client).where(Client.id == client_id).first()
        if not client:
            return jsonify(client="Not Found"), 404
        else:
            return jsonify(client=client.to_json()), 200

    @app.route('/clients', methods=['POST'])
    def create_client():
        """Эндпоинт создает нового клиента"""
        data = request.json
        schema = ClientSchema()

        try:
            client: Client = schema.load(data)
            db.session.add(client)
            db.session.commit()
        except ValidationError as exc:
            return jsonify(message='Validation error', exc_info=exc.messages), 422
        except Exception as exc:
            return jsonify(message='Exception', exc_info=exc), 500
        else:
            return jsonify(message='OK', new_client=client.to_json()), 201

    @app.route('/parkings', methods=['POST'])
    def add_parking():
        """Эндпоинт создает новое парковочное место"""
        data = request.json
        schema = ParkingSchema()

        try:
            parking: Parking = schema.load(data)
            db.session.add(parking)
            db.session.commit()
        except ValidationError as exc:
            return jsonify(message='Validation Error', exc_info=exc.messages), 422
        except Exception as exc:
            return jsonify(message='Exception', exc_info=exc), 500
        else:
            return jsonify(message='OK', parking=parking.to_json()), 201

    @app.route('/parkings', methods=['GET'])
    def get_parkings():
        """Эндпоинт возвращает список парковок"""
        list_parking: List[Parking] = db.session.query(Parking).all()
        return jsonify(list_parking=[parking.to_json() for parking in list_parking]), 200

    @app.route('/client_parkings', methods=['POST'])
    def add_client_parking():
        """Эндпоинт создает запись о заезде клиента на парковку"""
        data = request.json
        schema = ClientParkingSchema()

        try:
            client_parking: ClientParking = schema.load(data)
            # Поставим время заезда
            client_parking.time_in = datetime.now()
            db.session.add(client_parking)
            # уменьшим количество свободных мест на парковке
            # далее не работает - пишет NoneType
            # client_parking.parking.count_available_places -= 1
            parking = db.session.query(Parking).where(Parking.id == client_parking.parking_id).first()
            parking.count_available_places -= 1
            db.session.commit()
        except ValidationError as exc:
            return jsonify(message='Validation Error', exc_info=exc.messages), 422
        except Exception as exc:
            return jsonify(message='Exception', exc_info=exc), 500
        else:
            return jsonify(message='OK', client_parking=client_parking.to_json()), 201

    @app.route('/client_parkings', methods=['GET'])
    def get_clients_parkings():
        list_client_parking: List[ClientParking] = db.session.query(ClientParking).all()
        return jsonify(clients_parkings=[client_parking.to_json() for client_parking in list_client_parking]), 200

    @app.route('/client_parkings', methods=['DELETE'])
    def delete_client_parkings():
        """Эндпоинт удаляет запись client-parkings (клиент выехал с парковки)"""
        data = request.json
        schema = DeleteClientParkingSchema()

        try:
            client_parking: ClientParking = schema.load(data)
            # Установим время выезда
            client_parking.time_out = datetime.now()
            parking = db.session.query(Parking).where(Parking.id == client_parking.parking_id).first()
            # Увеличим количество свободных мест на данной парковке
            parking.count_available_places += 1
            db.session.commit()
        except ValidationError as exc:
            return jsonify(message='Validation Error', exc_info=exc.messages), 422
        except Exception as exc:
            return jsonify(message='Exception', exc_info=exc), 500
        else:
            return jsonify(message='OK', client_parking=client_parking.to_json()), 202

    return app
