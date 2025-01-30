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


