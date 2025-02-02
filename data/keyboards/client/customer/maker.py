from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

from data.constants.callbacks import create_new_order_callback, expand_order_list_callback, next_order_callback, \
    previous_order_callback, collapse_order_list_callback, edit_order_callback, edit_task_text_callback, \
    edit_order_exit_callback, edit_task_award_callback, edit_task_death_line_callback, edit_task_delete_callback, \
    edit_task_confirm_callback
from data.db_functions.generalis.user import get_user_orders_list


def create_main_menu_keyboard(telegram_id):
    orders = get_user_orders_list(telegram_id)
    if orders is None:
        return None
    elif len(orders) == 0:
        return ReplyKeyboardRemove()

    expand_user_tasks_list_button = InlineKeyboardButton("Открыть список заказов",
                                                         callback_data=expand_order_list_callback)
    keyboard = InlineKeyboardMarkup([
        [expand_user_tasks_list_button]])
    return keyboard


def create_choice_order_keyboard(telegram_id, index):
    orders = get_user_orders_list(telegram_id)
    if orders is None:
        return None
    if 0 <= index < len(orders):
        buttons = []
        if index >= 1:
            buttons.append(InlineKeyboardButton("←", callback_data=previous_order_callback.format(
                index - 1
            )))
        buttons.append(InlineKeyboardButton("Изменить", callback_data=edit_order_callback.format(
            orders[index].id
        )))
        if index < len(orders) - 1:
            buttons.append(InlineKeyboardButton("→", callback_data=next_order_callback.format(
                index + 1
            )))
        keyboard = InlineKeyboardMarkup(
            [buttons, [InlineKeyboardButton("Назад", callback_data=collapse_order_list_callback)]])
        return keyboard
    return None


def create_task_menu_keyboard(index, confirm, confirm_delete, is_completed_tack):
    buttons = []
    if not is_completed_tack:
        buttons += [[InlineKeyboardButton("Изменить текст", callback_data=edit_task_text_callback.format(index))]]
        buttons += [[InlineKeyboardButton("Изменить вознаграждение", callback_data=edit_task_award_callback.format(index))]]
        buttons += [[InlineKeyboardButton("Изменить срок", callback_data=edit_task_death_line_callback.format(index))]]
    if confirm:
        buttons += [[InlineKeyboardButton("Подтвердить выполнение", callback_data=edit_task_confirm_callback.format(index))]]
    if confirm_delete:
        buttons += [[InlineKeyboardButton("Удалить", callback_data=edit_task_delete_callback.format(index))]]
    buttons += [[InlineKeyboardButton("Назад", callback_data=edit_order_exit_callback)]]

    keyboard = InlineKeyboardMarkup(buttons)
    return keyboard
