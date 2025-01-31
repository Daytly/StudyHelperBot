from data.db_models.db_session import create_session
from data.db_models.tasks import Task


def create_task(text, death_line, award, customer_id):
    db_session = create_session()
    task = Task(text=text, death_line=death_line, award=award, customer_id=customer_id)
    db_session.add(task)
    try:
        db_session.commit()
    except Exception as error:
        return None
    return task