import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data.db_models.ratings import Rating
from data.db_models.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone_number = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_access = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    is_executor = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    rating_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('ratings.id'))
    rating = sqlalchemy.orm.relationship("Rating", back_populates="user", uselist=False, foreign_keys=[rating_id])

    def __init__(self, name, **kwargs):
        super().__init__(name=name, **kwargs)
        self.rating = Rating()

    def __repr__(self):
        return f'<User> {self.id} {self.username if self.username else self.name}'
