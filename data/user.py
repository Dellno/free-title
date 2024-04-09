import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=login)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    icon_path = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    news = orm.relationship("Game", back_populates='user')
