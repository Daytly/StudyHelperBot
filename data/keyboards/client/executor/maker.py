from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from data.constants.callbacks import access_task_callback, cancel_task_callback, expand_order_list_callback, \
    previous_task_callback, confirm_task_callback, next_task_callback, collapse_task_list_callback, \
    expand_task_list_callback
from data.db_functions.generalis.user import get_user_tasks_list


def create_access_task_keyboard(task_id):
    access_button = InlineKeyboardButton("Взять", callback_data=access_task_callback.format(task_id))
    access_keyboard = InlineKeyboardMarkup([[access_button]])
    return access_keyboard


def create_cancel_task_keyboard(task_id):
    cancel_button = InlineKeyboardButton("Отказаться", callback_data=cancel_task_callback.format(task_id))
    cancel_keyboard = InlineKeyboardMarkup([[cancel_button]])
    return cancel_keyboard


def create_executor_menu_keyboard(telegram_id):
    orders = get_user_tasks_list(telegram_id)
    if orders is None:
        return None
    elif len(orders) == 0:
        return ReplyKeyboardRemove()

    expand_user_tasks_list_button = InlineKeyboardButton("Открыть список заказов",
                                                         callback_data=expand_task_list_callback)
    keyboard = InlineKeyboardMarkup([
        [expand_user_tasks_list_button]])
    return keyboard


def create_choice_task_keyboard(telegram_id, index, confirm):
    tasks = get_user_tasks_list(telegram_id)
    if tasks is None:
        return None
    if 0 <= index < len(tasks):
        buttons = []
        if index >= 1:
            buttons.append(InlineKeyboardButton("←", callback_data=previous_task_callback.format(
                index - 1
            )))
        buttons.append(
            InlineKeyboardButton("Выполнено" if confirm else "Подтвердить", callback_data=confirm_task_callback.format(
                index
            )))
        if index < len(tasks) - 1:
            buttons.append(InlineKeyboardButton("→", callback_data=next_task_callback.format(
                index + 1
            )))
        keyboard = InlineKeyboardMarkup(
            [buttons, [InlineKeyboardButton("Назад", callback_data=collapse_task_list_callback)]])
        return keyboard
    return None
