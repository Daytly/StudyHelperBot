import sqlalchemy

from data.db_models.db_session import create_session
from data.db_models.users import User


def registration_user(telegram_id, name, surname, username, phone_number):
    db_session = create_session()
    user = User(
        id=telegram_id,
        name=name,
        surname=surname,
        username=username,
        phone_number=phone_number,
    )
    db_session.add(user)
    try:
        db_session.commit()
    except sqlalchemy.exc.IntegrityError:
        return None
    db_session.close()
    return user

def get_user_orders_list(telegram_id):
    db_session = create_session()
    user = db_session.query(User).get(telegram_id)
    if user is None:
        return None
    return user.orders

def get_user_tasks_list(telegram_id):
    db_session = create_session()
    user = db_session.query(User).get(telegram_id)
    if user is None:
        return None
    return user.tasks

def get_user_task(telegram_id, index):
    orders = get_user_orders_list(telegram_id)
    if orders is None:
        return None

    if 0 <= index < len(orders):
        return orders[index]
    return None

def get_user_by_telegram_id(telegram_id):
    db_session = create_session()
    user = db_session.query(User).get(telegram_id)
    return user

