from telegram import Update
from telegram.ext import CallbackContext

from data.db_functions.generalis.task import get_task_by_id
from data.messages.client.customer import new_executor_message


async def notice_customer(update: Update, context: CallbackContext, task_id):
    task = get_task_by_id(task_id)
    if task is None:
        return
    user_id = task.customer_id
    executor = task.executor
    if executor is None:
        return
    try:
        await update.get_bot().send_message(user_id, new_executor_message.format(task.text, executor.phone_number))
    except Exception as e:
        pass