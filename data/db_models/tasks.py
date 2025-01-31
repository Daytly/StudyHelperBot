import sqlalchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from data.db_models.db_session import SqlAlchemyBase


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    customer_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    executor_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    text = sqlalchemy.Column(sqlalchemy.Text)
    award = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    is_completed_customer = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_completed_executor = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_completed_tack = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    death_line = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)

    customer = sqlalchemy.orm.relationship("User", back_populates="orders", foreign_keys=[customer_id])

    # Связь с таблицей User через executor_id
    executor = sqlalchemy.orm.relationship("User", back_populates="tasks", foreign_keys=[executor_id])


    def __repr__(self):
        return f'<Task> {self.id} {self.text[:10]}...'

    @validates('is_completed_customer', 'is_completed_executor')
    def update_dependent_field(self, key, value):
        if key == 'is_completed_customer':
            self.is_completed_customer = value
        elif key == 'is_completed_executor':
            self.is_completed_executor = value

        self.is_completed_tack = self.calculate_is_completed_tack()

        return value

    def calculate_is_completed_tack(self):
        return self.is_completed_customer and self.is_completed_executor
