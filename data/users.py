import sqlalchemy
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True, nullable=False)
    tid = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, unique=True)
    sex = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    doing = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    searching_for = sqlalchemy.Column(sqlalchemy.Integer)
    room = sqlalchemy.Column(sqlalchemy.Integer)
