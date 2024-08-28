from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Sequence, Integer, VARCHAR, BOOLEAN, JSON, ForeignKey


Base = declarative_base()


class Coffee(Base):
    __tablename__ = 'coffee'

    id = Column(Integer, Sequence('coffee_id_seq'), primary_key=True)
    title = Column(VARCHAR(200), nullable=False)
    origin = Column(VARCHAR(200))
    intensifier = Column(VARCHAR(200))
    notes = Column(VARCHAR)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(VARCHAR(50), nullable=False)
    has_sale = Column(BOOLEAN)
    address = Column(JSON)
    coffee_id = Column(Integer, ForeignKey('coffee.id'))
    coffee = relationship("Coffee", backref="users")