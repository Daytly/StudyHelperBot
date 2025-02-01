from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, MessageHandler, filters, \
    CallbackContext

from data.constants.callback_patterns import edit_task_menu_pattern
from data.constants.callbacks import edit_task_text_callback, edit_task_award_callback, edit_task_death_line_callback, \
    edit_task_delete_callback, edit_task_confirm_callback
from data.db_functions.generalis.task import update_task_text, update_task_award, update_task_deadline, \
    delete_task_by_id, get_task_by_id, update_task_conform_customer
from data.db_functions.generalis.user import get_user_task
from data.keyboards.client.customer.keyboards import input_award_keyboard
from data.keyboards.client.customer.maker import create_main_menu_keyboard, create_task_menu_keyboard
from data.messages.client.customer import task_message, create_edit_task_message

EDIT_TEXT, EDIT_AWARD, EDIT_DEADLINE, CONFIRM, DELETE = range(5)


async def edit_task_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    callback = query.data

    if edit_task_text_callback.format("") in callback:
        task_id = int(callback.replace(edit_task_text_callback.format(""), ""))
        await query.edit_message_text(text="Введите новый текст задачи:")
        context.user_data['task_id'] = task_id
        return EDIT_TEXT
    elif edit_task_award_callback.format("") in callback:
        task_id = int(callback.replace(edit_task_award_callback.format(""), ""))
        await query.edit_message_text(text="Введите новую награду:")
        context.user_data['task_id'] = task_id
        return EDIT_AWARD
    elif edit_task_death_line_callback.format("") in callback:
        task_id = int(callback.replace(edit_task_death_line_callback.format(""), ""))
        await query.edit_message_text(text="Введите новый дедлайн в формате YYYY-MM-DD")
        context.user_data['task_id'] = task_id
        return EDIT_DEADLINE
    elif edit_task_delete_callback.format("") in callback:
        task_id = int(callback.replace(edit_task_delete_callback.format(""), ""))
        context.user_data['task_id'] = task_id
        task = get_task_by_id(task_id)
        if task.is_completed_executor or task.is_completed_customer:
            await query.edit_message_text(text="Удалить нельзя")
            await open_edit_task_menu(update, context, task_id)
            return ConversationHandler.END
        await query.edit_message_text(text="Введите слово ПОДТВЕРДИТЬ, чтобы отменить любое другое слово")
        return DELETE
    elif edit_task_confirm_callback.format("") in callback:
        task_id = int(callback.replace(edit_task_confirm_callback.format(""), ""))
        context.user_data['task_id'] = task_id
        await query.edit_message_text(text="Введите слово ПОДТВЕРДИТЬ, чтобы отменить любое другое")
        return CONFIRM


async def edit_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    new_text = update.message.text
    task_id = context.user_data['task_id']
    update_task_text(task_id, new_text)
    await update.message.reply_text("Текст задачи изменен.")
    await open_edit_task_menu(update, context, task_id)
    return ConversationHandler.END


async def edit_award(update: Update, context: ContextTypes.DEFAULT_TYPE):
    input_award = update.message.text
    if input_award.isdigit() or input_award[:-1].isdigit():
        new_award = int(input_award) if input_award.isdigit() else int(input_award[:-1])
        task_id = context.user_data['task_id']
        task = get_task_by_id(task_id)
        if task.award > new_award:
            await update.message.reply_text("Награда не может быть меньше предыдущей")
            return EDIT_AWARD
        update_task_award(task_id, new_award)
        await update.message.reply_text("Награда изменена.")
        await open_edit_task_menu(update, context, task_id)
    else:
        await update.message.reply_text("Пожалуйста, введите корректное число.")
        return EDIT_AWARD
    return ConversationHandler.END


async def edit_deadline(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from datetime import datetime
    try:
        new_deadline = datetime.strptime(update.message.text, '%Y-%m-%d')
        task_id = context.user_data['task_id']
        task = get_task_by_id(task_id)
        if task.death_line > new_deadline:
            await update.message.reply_text("Срок не может быть меньше предыдущего")
            return EDIT_DEADLINE
        update_task_deadline(task_id, new_deadline)
        await update.message.reply_text("Дедлайн изменен.")
        await open_edit_task_menu(update, context, task_id)
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите дедлайн в правильном формате (YYYY-MM-DD).")
        return EDIT_DEADLINE
    return ConversationHandler.END


async def confirm_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    task_id = context.user_data['task_id']
    if message == "ПОДТВЕРДИТЬ":
        delete_task_by_id(task_id)
        await update.message.reply_html(text="Задача удалена.",
                                        reply_markup=create_main_menu_keyboard(update.effective_user.id))
        return ConversationHandler.END
    await update.message.reply_html("Не верное слово")
    await open_edit_task_menu(update, context, task_id)
    return ConversationHandler.END


async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    task_id = context.user_data['task_id']
    if message == "ПОДТВЕРДИТЬ":
        await update.message.reply_html(text="Подтверждено")
        update_task_conform_customer(task_id)
        return ConversationHandler.END
    await update.message.reply_html("Не верное слово")
    await open_edit_task_menu(update, context, task_id)
    return ConversationHandler.END


async def open_edit_task_menu(update: Update, context: CallbackContext, task_id) -> None:
    order = get_task_by_id(task_id)
    if order is None:
        return
    keyboard = create_task_menu_keyboard(order.id, not order.is_completed_customer and order.executor is not None,
                                         not (order.is_completed_customer or order.is_completed_executor))
    text = create_edit_task_message(order)

    try:
        await update.callback_query.edit_message_text(text, reply_markup=keyboard)
    except AttributeError:
        await update.message.reply_html(text, reply_markup=keyboard)

edit_task_conv_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit_task_callback, pattern=edit_task_menu_pattern)],
    states={
        EDIT_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_text)],
        EDIT_AWARD: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_award)],
        EDIT_DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_deadline)],
        DELETE: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_delete)],
        CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],

    },
    fallbacks=[]
)
