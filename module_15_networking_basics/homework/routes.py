from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired
import json
from typing import Optional

import model


app = Flask(__name__)


class RoomForm(FlaskForm):
    floor = IntegerField(validators=[InputRequired()])
    beds = IntegerField(validators=[InputRequired()])
    guestNum = IntegerField(validators=[InputRequired()])
    price = IntegerField(validators=[InputRequired()])


@app.route('/add-room', methods=['POST'])
def get_room() -> tuple[str, int]:
    form = RoomForm()

    if form.validate_on_submit():
        model.add_new_room(form.floor.data, form.beds.data, form.guestNum.data, form.price.data)

        return f'Данные о комнате сохранены!', 200


@app.route('/room', methods=['GET'])
def get_number_rooms() -> tuple[str, int]:
    """Функция возвращает json с количеством комнат (судя по pre-req к add-room)"""
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
            return f'check_in должен быть не больше check_out! check_in = {check_in}, check_out = {check_out}', 400

        room_id = int(data_object['roomId'])
        if not model.id_in_rooms(room_id):
            return f'Такого id нет в бд! room_id = {room_id}', 400

        first_name, second_name = data_object['firstName'], data_object['lastName']
        can_add_new_order: bool = model.booking(check_in, check_out, first_name, second_name, room_id)
        if not can_add_new_order:
            return f'Данная комната на эти даты уже забронирована! room_id = {room_id}', 409
        return 'Комната успешно забронирована!', 200


if __name__ == '__main__':
    model.create_db()
    app.config['WTF_CSRF_ENABLED'] = False
    app.run(debug=True)
