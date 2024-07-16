from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import InputRequired
import json
from typing import Optional

import model
from model import REF_GET_ROOMS


app = Flask(__name__)


class RoomForm(FlaskForm):
    floor = IntegerField(validators=[InputRequired()])
    beds = IntegerField(validators=[InputRequired()])
    guestNum = IntegerField(validators=[InputRequired()])
    price = IntegerField(validators=[InputRequired()])


@app.route('/add_new_room', methods=['POST'])
def add_new_room() -> tuple[str, int]:
    form = RoomForm()

    if form.validate_on_submit():
        model.add_new_room(form.floor.data, form.beds.data, form.guestNum.data, form.price.data)
        json_response: dict = {
            'status': 'Данные о комнате сохранены!',
            'refs': [REF_GET_ROOMS]
        }

        return json.dumps(json_response), 200
    else:
        json_response: dict = {
            'status': 'Не получилось добавить новую комнату',
            'refs': [REF_GET_ROOMS]
        }
        return json.dumps(json_response), 400


@app.route('/rooms', methods=['GET'])
def rooms() -> tuple[str, int]:
    """Функция возвращает json c информацией о комнатах"""
    check_in: Optional[int] = request.args.get('checkIn', default=None, type=int)
    check_out: Optional[int] = request.args.get('checkOut', default=None, type=int)
    guests_num: Optional[int] = request.args.get('guestsNum', default=None, type=int)
    if check_in and check_out and guests_num:
        return (json.dumps(model.get_info_about_rooms_between_dates_with_guests_num(check_in, check_out, guests_num)),
                200)
    return json.dumps(model.get_info_about_all_rooms()), 200


@app.route('/booking', methods=['POST'])
def booking() -> tuple[str, int]:
    form_data = request.get_data(as_text=True)
    data_object = json.loads(form_data)

    if request.method == 'POST':
        check_in, check_out = data_object['bookingDates']['checkIn'], data_object['bookingDates']['checkOut'],
        if int(check_in) > int(check_out):
            json_response: dict = {
                'status': 'Забронировать не получилось',
                'description': f'check_in должен быть не больше check_out!'
                               f' check_in = {check_in}, check_out = {check_out}',
                'refs': [REF_GET_ROOMS]
            }
            return json.dumps(json_response), 400

        room_id = int(data_object['roomId'])
        if not model.id_in_rooms(room_id):
            json_response: dict = {
                'status': 'Забронировать не получилось',
                'description': f'Такого id нет в бд! room_id = {room_id}',
                'refs': [REF_GET_ROOMS]
            }
            return json.dumps(json_response), 400

        first_name, second_name = data_object['firstName'], data_object['lastName']
        can_add_new_order: bool = model.booking(check_in, check_out, first_name, second_name, room_id)
        if not can_add_new_order:
            json_response: dict = {
                'status': 'Забронировать не получилось',
                'description': f'Данная комната на эти даты уже забронирована! room_id = {room_id}',
                'refs': [REF_GET_ROOMS]
            }
            return json.dumps(json_response), 409
        json_response: dict = {
            'status': 'Комната успешно забронирована!',
            'description': f'OK',
            'refs': [REF_GET_ROOMS]
        }
        return json.dumps(json_response), 200


if __name__ == '__main__':
    model.create_db()
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
