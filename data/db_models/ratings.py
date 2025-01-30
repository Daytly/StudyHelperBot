import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from data.db_models.db_session import SqlAlchemyBase


class Rating(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'ratings'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    rating_customer = sqlalchemy.Column(sqlalchemy.Float, default=0)
    rating_executor = sqlalchemy.Column(sqlalchemy.Float, default=0)

    user = sqlalchemy.orm.relationship("User", back_populates="rating", uselist=False)

    def __repr__(self):
        return f'<Rating> {self.id} {self.rating_customer} {self.rating_executor}'
