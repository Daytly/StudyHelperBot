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


def get_task_by_id(task_id):
    db_session = create_session()
    task = db_session.query(Task).get(task_id)
    return task

def delete_task_by_id(task_id):
    db_session = create_session()
    task = db_session.query(Task).get(task_id)
    db_session.delete(task)
    db_session.commit()
    return task

def update_task_text(task_id, new_text):
    db_session = create_session()
    task = db_session.query(Task).get(task_id)
    if task:
        task.text = new_text
        db_session.commit()
    db_session.close()

def update_task_award(task_id, new_award):
    db_session = create_session()
    task = db_session.query(Task).get(task_id)
    if task:
        task.award = new_award
        db_session.commit()
    db_session.close()

def update_task_deadline(task_id, new_deadline):
    db_session = create_session()
    task = db_session.query(Task).get(task_id)
    if task:
        task.death_line = new_deadline
        db_session.commit()
    db_session.close()


def update_task_conform_customer(task_id):
    db_session = create_session()
    task = db_session.query(Task).get(task_id)
    if task:
        task.is_conform_customer = True
        db_session.commit()
    db_session.close()