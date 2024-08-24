from fastapi import FastAPI
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List


app = FastAPI()


class Author(BaseModel):
    name: str
    birthday: str

    @field_validator('birthday')
    def validate_birthday(cls, birthday: str):
        birthday_date: datetime = datetime.strptime(birthday, '%d.%m.%Y')
        print(birthday_date)
        if 500 <= birthday_date.year < 2000:
            raise ValueError('Birth year must be less than 500 and grater than 2000')
        return birthday


AUTHORS: List[Author] = list()


@app.get('/authors')
def get_authors():
    return {'authors': AUTHORS}


@app.post('/authors')
def add_author(author: Author):
    AUTHORS.append(author)
    return {'message': 'OK'}

