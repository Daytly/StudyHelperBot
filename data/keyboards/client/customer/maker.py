from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from data.constants.callbacks import create_new_task_callback, expand_tasks_list_callback
from data.db_functions.generalis.user import get_user_tasks_list


def create_main_menu_keyboard(telegram_id):
    orders = get_user_tasks_list(telegram_id)
    if orders is None:
        return None
    elif len(orders) == 0:
        return ReplyKeyboardRemove()

    expand_user_tasks_list_button = InlineKeyboardButton("Открыть список заказов",
                                                         callback_data=expand_tasks_list_callback)
    keyboard = InlineKeyboardMarkup([
        [expand_user_tasks_list_button]])
    return keyboard
