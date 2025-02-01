from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from data.constants.callbacks import create_new_task_callback, expand_tasks_list_callback, next_task_callback, \
    previous_task_callback, collapse_task_list_callback, edit_task_callback, edit_task_text_callback, \
    edit_task_exit_callback, edit_task_award_callback, edit_task_death_line_callback, edit_task_delete_callback, \
    edit_task_confirm_callback
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


def create_choice_task_keyboard(telegram_id, index):
    orders = get_user_tasks_list(telegram_id)
    if orders is None:
        return None
    if 0 <= index < len(orders):
        buttons = []
        if index >= 1:
            buttons.append(InlineKeyboardButton("←", callback_data=previous_task_callback.format(
                index - 1
            )))
        buttons.append(InlineKeyboardButton("Изменить", callback_data=edit_task_callback.format(
            orders[index].id
        )))
        if index < len(orders) - 1:
            buttons.append(InlineKeyboardButton("→", callback_data=next_task_callback.format(
                index + 1
            )))
        keyboard = InlineKeyboardMarkup(
            [buttons, [InlineKeyboardButton("Назад", callback_data=collapse_task_list_callback)]])
        return keyboard
    return None


def create_task_menu_keyboard(index, confirm, confirm_delete):
    buttons = []
    buttons += [[InlineKeyboardButton("Изменить текст", callback_data=edit_task_text_callback.format(index))]]
    buttons += [[InlineKeyboardButton("Изменить вознаграждение", callback_data=edit_task_award_callback.format(index))]]
    buttons += [[InlineKeyboardButton("Изменить срок", callback_data=edit_task_death_line_callback.format(index))]]
    if confirm:
        buttons += [[InlineKeyboardButton("Подтвердить выполнение", callback_data=edit_task_confirm_callback.format(index))]]
    if confirm_delete:
        buttons += [[InlineKeyboardButton("Удалить", callback_data=edit_task_delete_callback.format(index))]]
    buttons += [[InlineKeyboardButton("Назад", callback_data=edit_task_exit_callback)]]

    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
