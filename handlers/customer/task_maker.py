from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler, MessageHandler, filters, \
    CallbackQueryHandler
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from data.constants.commands import create_task_command, stop_command
from data.constants.user_data_keys import DEATH_LINE_TASK, TEXT_TASK, AWARD_TASK
from data.db_functions.generalis.task import create_task
from data.keyboards.client.customer.keyboards import input_award_keyboard
from data.messages.client.customer import input_award_task_message, \
    input_death_line_task_message, final_create_task_message, input_award_task_emission_message, \
    stop_create_task_message, input_text_task_message
from handlers.executor.notice import notice_executors

INPUT_TEXT_TASK_STATE, INPUT_DEATH_LINE_TASK_STATE, INPUT_AWARD_TASK_STATE = range(3)


async def input_text_task_handler(update: Update, context: CallbackContext):
    text = update.message.text
    context.user_data[TEXT_TASK] = text
    await update.message.reply_html(input_death_line_task_message)
    calendar, step = DetailedTelegramCalendar().build()
    await update.message.reply_text(f"Выберите {LSTEP[step]}", reply_markup=calendar)
    return INPUT_DEATH_LINE_TASK_STATE


async def input_death_line_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    result, key, step = DetailedTelegramCalendar().process(query.data)
    if not result and key:
        await query.edit_message_text(f"Выберите {LSTEP[step]}", reply_markup=key)
        return INPUT_DEATH_LINE_TASK_STATE
    elif result:
        await query.edit_message_text(f"Вы выбрали дату: {result}")
        context.user_data[DEATH_LINE_TASK] = result
        await update.get_bot().send_message(query.message.chat.id, input_award_task_message, reply_markup=input_award_keyboard)
        return INPUT_AWARD_TASK_STATE


async def input_award_task_handler(update: Update, context: CallbackContext):
    input_award = update.message.text
    if input_award.isdigit() or input_award[:-1].isdigit():
        context.user_data[AWARD_TASK] = int(input_award) if input_award.isdigit() else int(input_award[:-1])
        text = context.user_data[TEXT_TASK]
        death_line = context.user_data[DEATH_LINE_TASK]
        award = context.user_data[AWARD_TASK]
        task_id = create_task(text, death_line, award, update.effective_user.id)
        await notice_executors(update, context, task_id)
        await update.message.reply_html(final_create_task_message, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        await  update.message.reply_html(input_award_task_emission_message)
        return INPUT_AWARD_TASK_STATE


async def stop_create_task_handler(update: Update, context: CallbackContext):
    await update.message.reply_html(stop_create_task_message)
    return ConversationHandler.END


async def create_new_task(update: Update, context: CallbackContext):
    await update.message.reply_html(input_text_task_message)
    return INPUT_TEXT_TASK_STATE


task_maker_conv_handler = ConversationHandler(
    entry_points=[CommandHandler(create_task_command, create_new_task)],
    states={
        INPUT_TEXT_TASK_STATE: [MessageHandler(filters.TEXT, input_text_task_handler)],
        INPUT_DEATH_LINE_TASK_STATE: [CallbackQueryHandler(input_death_line_handler)],
        INPUT_AWARD_TASK_STATE: [MessageHandler(filters.TEXT, input_award_task_handler)],
    },
    fallbacks=[CommandHandler(stop_command, stop_create_task_handler)],
)

