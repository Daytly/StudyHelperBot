from telegram import Update
from telegram.ext import CallbackContext

from data.constants.CONSTANTS import admin_group_id
from data.constants.callbacks import access_task_callback, cancel_task_callback
from data.db_functions.generalis.task import get_task_by_id, update_task_executor, delete_task_executor, \
    get_tasks_no_executor
from data.decorators import executor_command
from data.keyboards.client.executor.maker import create_access_task_keyboard, create_cancel_task_keyboard
from data.messages.client.executor import new_task_message, no_tasks_message


async def notice_executors(update: Update, context: CallbackContext, task_id) -> None:
    task = get_task_by_id(task_id)
    if task is None:
        return

    await update.get_bot().send_message(admin_group_id, new_task_message.format(
        task.customer.phone_number,
        task.text,
        task.award,
        task.death_line,
        "Не определён" if task.executor is None else task.executor.phone_number,
    ), reply_markup=create_access_task_keyboard(task_id) if task.executor is None else create_cancel_task_keyboard(
        task_id))


async def notice_executors_callback_handler(update: Update, context: CallbackContext, task_id) -> None:
    task = get_task_by_id(task_id)
    if task is None:
        return

    await update.callback_query.edit_message_text(new_task_message.format(
        task.customer.phone_number,
        task.text,
        task.award,
        task.death_line,
        "Не определён" if task.executor is None else task.executor.phone_number,
    ), reply_markup=create_access_task_keyboard(task_id) if task.executor is None else create_cancel_task_keyboard(
        task_id))


@executor_command
async def executor_group_callback_handler(update: Update, context: CallbackContext) -> None:
    callback = update.callback_query.data
    await update.callback_query.answer()
    if access_task_callback.format("") in callback:
        task_id = int(callback.replace(access_task_callback.format(""), ""))
        update_task_executor(task_id, update.effective_user.id)
        await notice_executors_callback_handler(update, context, task_id)
    elif cancel_task_callback.format("") in callback:
        task_id = int(callback.replace(cancel_task_callback.format(""), ""))
        task = get_task_by_id(task_id)
        if task.executor_id == update.effective_user.id:
            delete_task_executor(task_id)
            await notice_executors_callback_handler(update, context, task_id)


@executor_command
async def update_tasks_handler(update: Update, context: CallbackContext) -> None:
    tasks = get_tasks_no_executor()
    for task in tasks:
        await notice_executors(update, context, task.id)
    if not tasks:
        await update.message.reply_html(no_tasks_message)
