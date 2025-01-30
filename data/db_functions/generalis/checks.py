from data.db_models.db_session import create_session
from data.db_models.users import User


def check_is_admin(telegram_id):
    db_session = create_session()
    user = db_session.query(User).get(telegram_id)
    if user is None:
        return False
    return user.is_admin

def check_is_register(telegram_id):
    db_session = create_session()
    user = db_session.query(User).get(telegram_id)
    if user is None:
        return False
    return True