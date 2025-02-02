from telegram import Update
from telegram.ext import CallbackContext

from data.constants.callbacks import expand_task_list_callback, \
    next_task_callback, previous_task_callback, confirm_task_callback, collapse_task_list_callback
from data.db_functions.generalis.task import switch_task_confirm_executor, get_task_by_id
from data.db_functions.generalis.user import get_user_tasks_list
from data.decorators import executor_command
from data.keyboards.client.executor.maker import create_executor_menu_keyboard, create_choice_task_keyboard
from data.messages.client.customer import task_message
from data.messages.client.executor import executor_menu_message
from data.messages.generalis import no_registration_emission_message, no_task_emission_message, confirm_message, \
    work_message


@executor_command
async def open_executor_menu(update: Update, context: CallbackContext):
    keyboard = create_executor_menu_keyboard(update.effective_user.id)
    if keyboard is None:
        await update.message.reply_html(no_registration_emission_message)
        return
    return await update.message.reply_text(executor_menu_message, reply_markup=keyboard)


async def open_executor_menu_callback(update: Update, context: CallbackContext):
    keyboard = create_executor_menu_keyboard(update.effective_user.id)
    if keyboard is None:
        await update.message.reply_html(no_registration_emission_message)
        return
    await update.callback_query.edit_message_text(executor_menu_message,
                                                  reply_markup=keyboard)


@executor_command
async def executor_menu_callback_handler(update: Update, context: CallbackContext) -> None:
    callback = update.callback_query.data
    await update.callback_query.answer()
    if callback == expand_task_list_callback:
        await task_preview(update, context, 0)
    elif next_task_callback.format("") in callback:
        index = int(callback.replace(next_task_callback.format(""), ""))
        await task_preview(update, context, index)
    elif previous_task_callback.format("") in callback:
        index = int(callback.replace(previous_task_callback.format(""), ""))
        await task_preview(update, context, index)
    elif confirm_task_callback.format("") in callback:
        index = int(callback.replace(confirm_task_callback.format(""), ""))
        tasks = get_user_tasks_list(update.effective_user.id)
        switch_task_confirm_executor(tasks[index].id)
        await task_preview(update, context, index)
    elif callback == collapse_task_list_callback:
        await open_executor_menu_callback(update, context)


async def task_preview(update: Update, context: CallbackContext, index) -> None:
    task = show_task(update.effective_user.id, index)
    if task is None:
        await update.message.reply_html(no_task_emission_message)
        return
    await update.callback_query.edit_message_text(task[0], reply_markup=task[1])
    return


def show_task(telegram_id, index):
    tasks = get_user_tasks_list(telegram_id)
    if tasks is None:
        return
    task = tasks[index]
    keyboard = create_choice_task_keyboard(telegram_id, index, task.is_completed_executor)
    return task_message.format(
        task.text,
        task.award,
        task.death_line.strftime("%Y-%m-%d"),
        confirm_message if task.is_completed_tack else work_message
    ), keyboard
