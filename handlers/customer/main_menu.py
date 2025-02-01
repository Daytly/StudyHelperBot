from telegram import Update
from telegram.ext import CallbackContext

from data.constants.callbacks import expand_tasks_list_callback, next_task_callback, previous_task_callback, \
    edit_task_callback, collapse_task_list_callback, edit_task_delete_callback, edit_task_exit_callback, \
    edit_task_confirm_callback
from data.db_functions.generalis.task import delete_task_by_id
from data.db_functions.generalis.user import get_user_tasks_list
from data.decorators import register_command
from data.keyboards.client.customer.maker import create_main_menu_keyboard, create_choice_task_keyboard
from data.messages.client.customer import main_menu_message, task_message
from data.messages.generalis import no_registration_emission_message, no_task_emission_message
from handlers.customer.edit_task import open_edit_task_menu


@register_command
async def open_main_menu(update: Update, context: CallbackContext):
    keyboard = create_main_menu_keyboard(update.effective_user.id)
    if keyboard is None:
        await update.message.reply_html(no_registration_emission_message)
        return
    return await update.message.reply_text(main_menu_message, reply_markup=keyboard)


async def open_main_menu_callback(update: Update, context: CallbackContext):
    keyboard = create_main_menu_keyboard(update.effective_user.id)
    if keyboard is None:
        await update.message.reply_html(no_registration_emission_message)
        return
    await update.callback_query.edit_message_text(main_menu_message,
                                                  reply_markup=keyboard)


@register_command
async def main_menu_callback_handler(update: Update, context: CallbackContext) -> None:
    callback = update.callback_query.data
    await update.callback_query.answer()
    if callback == expand_tasks_list_callback:
        await task_preview(update, context, 0)
    elif next_task_callback.format("") in callback:
        index = int(callback.replace(next_task_callback.format(""), ""))
        await task_preview(update, context, index)
    elif previous_task_callback.format("") in callback:
        index = int(callback.replace(previous_task_callback.format(""), ""))
        await task_preview(update, context, index)
    elif edit_task_callback.format("") in callback:
        task_id = int(callback.replace(edit_task_callback.format(""), ""))
        await open_edit_task_menu(update, context, task_id)
    elif callback == collapse_task_list_callback:
        await open_main_menu_callback(update, context)
    elif callback == edit_task_exit_callback:
        await open_main_menu_callback(update, context)


async def task_preview(update: Update, context: CallbackContext, index) -> None:
    task = show_task(update.effective_user.id, index)
    if task is None:
        await update.message.reply_html(no_task_emission_message)
        return
    await update.callback_query.edit_message_text(task[0], reply_markup=task[1])
    return


def show_task(telegram_id, index):
    orders = get_user_tasks_list(telegram_id)
    if orders is None:
        return
    order = orders[index]
    keyboard = create_choice_task_keyboard(telegram_id, index)
    return task_message.format(
        order.text,
        order.award,
        order.death_line
    ), keyboard


