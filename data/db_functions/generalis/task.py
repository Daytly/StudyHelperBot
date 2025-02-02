from data.db_models.db_session import create_session
from data.db_models.tasks import Task
from data.db_models.users import User


def create_task(text, death_line, award, customer_id):
    db_session = create_session()
    task = Task(text=text, death_line=death_line, award=award, customer_id=customer_id)
    db_session.add(task)
    try:
        db_session.commit()
    except Exception as error:
        return None
    return task.id


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

def update_task_executor(task_id, executor):
    db_session = create_session()
    if type(executor) is not User:
        executor = db_session.query(User).get(executor)
    task = db_session.query(Task).get(task_id)
    if task:
        if task.executor is None:
            task.executor = executor
            db_session.commit()

def delete_task_executor(task_id):
    db_session = create_session()
    task = db_session.query(Task).get(task_id)
    if task:
        task.executor = None
        db_session.commit()



def update_task_confirm_customer(task_id):
    db_session = create_session()
    task = db_session.query(Task).get(task_id)
    if task:
        task.is_completed_customer = True
        db_session.commit()
    db_session.close()


def switch_task_confirm_executor(task_id):
    db_session = create_session()
    task = db_session.query(Task).get(task_id)
    if task:
        value = not task.is_completed_executor
        task.is_completed_executor = value
        db_session.commit()
        db_session.close()
    db_session.close()
    return

def get_tasks_no_executor():
    db_session = create_session()
    tasks = db_session.query(Task).filter(Task.executor_id==None).all()
    return tasks