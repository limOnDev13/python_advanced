from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Sequence, Integer, VARCHAR, BOOLEAN, JSON, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy import literal
import sqlalchemy.dialects.postgresql
from typing import Any


Base = declarative_base()


class Coffee(Base):
    __tablename__ = 'coffee'

    id = Column(Integer, Sequence('coffee_id_seq'), primary_key=True)
    title = Column(VARCHAR(200), nullable=False)
    origin = Column(VARCHAR(200))
    intensifier = Column(VARCHAR(200))
    notes = Column(VARCHAR)

    __table_args__ = (
        Index(
            'title_fts',
            func.to_tsvector(literal('english'), title),
            postgresql_using='gin'
        ),
    )

    def to_json(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(VARCHAR(50), nullable=False)
    surname = Column(VARCHAR(100), nullable=True)
    patronomic = Column(VARCHAR(100), nullable=True)
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey('coffee.id'))
    coffee = relationship("Coffee", backref="users")

    def to_json(self) -> dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}

